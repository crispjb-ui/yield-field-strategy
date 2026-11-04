"""Minimal ABI encode/decode over yf.rpc for the extracted contract ABIs (static types + strings)."""
from __future__ import annotations
import json
from pathlib import Path
from .rpc import Rpc, selector, enc_uint, enc_addr

ABI_DIR = Path(__file__).resolve().parent.parent / "abi"
STATIC = {"uint256", "uint128", "uint64", "uint32", "uint16", "uint8", "int256", "address", "bool", "bytes32", "bytes4"}


def _canon(t: str) -> str:
    return {"uint": "uint256", "int": "int256"}.get(t, t)


def _enc(t: str, v) -> str:
    t = _canon(t)
    if t.startswith("uint") or t.startswith("int"):
        return enc_uint(int(v) & (2**256 - 1))
    if t == "address":
        return enc_addr(v)
    if t == "bool":
        return enc_uint(1 if v else 0)
    if t == "bytes32":
        return v.replace("0x", "").ljust(64, "0")
    raise ValueError(f"unsupported input type {t}")


def _dec_word(t: str, w: str):
    t = _canon(t)
    if t.startswith("uint"):
        return int(w, 16)
    if t.startswith("int"):
        x = int(w, 16); return x - 2**256 if x >= 2**255 else x
    if t == "address":
        return "0x" + w[-40:]
    if t == "bool":
        return int(w, 16) != 0
    return "0x" + w


def _decode(outputs: list, data: str):
    d = data[2:] if data.startswith("0x") else data
    words = [d[i:i + 64] for i in range(0, len(d), 64)]
    res = []
    for i, o in enumerate(outputs):
        t = _canon(o["type"])
        if t in STATIC or t.startswith("uint") or t.startswith("int"):
            res.append(_dec_word(t, words[i]))
        elif t == "string" or t == "bytes":
            off = int(words[i], 16) // 32
            ln = int(words[off], 16)
            raw = bytes.fromhex(d[(off + 1) * 64:(off + 1) * 64 + ln * 2])
            res.append(raw.decode(errors="replace") if t == "string" else "0x" + raw.hex())
        elif t.endswith("[]"):
            base = t[:-2]
            off = int(words[i], 16) // 32
            ln = int(words[off], 16)
            res.append([_dec_word(base, words[off + 1 + k]) for k in range(ln)])
        else:
            res.append(("<undecoded " + t + ">", words[i]))
    return res[0] if len(res) == 1 else res


class Contract:
    def __init__(self, rpc: Rpc, address: str, abi_name: str):
        self.rpc, self.address = rpc, address
        self.abi = json.load(open(ABI_DIR / f"{abi_name}.json"))
        self.fns = {f["name"]: f for f in self.abi if f.get("type") == "function"}

    def call(self, name: str, *args):
        f = self.fns[name]
        sig = f"{name}({','.join(_canon(i['type']) for i in f['inputs'])})"
        data = selector(sig) + "".join(_enc(i["type"], a) for i, a in zip(f["inputs"], args))
        return _decode(f["outputs"], self.rpc.eth_call(self.address, data))

    def views(self) -> list[str]:
        return [n for n, f in self.fns.items() if f.get("stateMutability") in ("view", "pure")]

    def dump(self, only_no_args: bool = True) -> dict:
        out = {}
        for n in self.views():
            f = self.fns[n]
            if f["inputs"] and only_no_args:
                continue
            try:
                out[n] = self.call(n)
            except Exception as e:
                out[n] = f"ERR {str(e)[:60]}"
        return out
