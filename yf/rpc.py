"""Minimal JSON-RPC client for Robinhood Chain (EVM). No web3 dependency."""
from __future__ import annotations
import hashlib
import requests


def _keccak(data: bytes) -> bytes:
    # Python's hashlib has sha3_256 (NIST), not keccak-256. Use a tiny pure
    # implementation to avoid a dependency.
    return _Keccak().digest(data)


class _Keccak:
    """Keccak-256 (pre-NIST padding 0x01) — pure Python, adequate for selectors."""
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
        0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
    ]
    ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
           [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]

    @staticmethod
    def _rol(x, n):
        return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

    def _f(self, st):
        for rc in self.RC:
            c = [st[x][0] ^ st[x][1] ^ st[x][2] ^ st[x][3] ^ st[x][4] for x in range(5)]
            d = [c[(x - 1) % 5] ^ self._rol(c[(x + 1) % 5], 1) for x in range(5)]
            st = [[st[x][y] ^ d[x] for y in range(5)] for x in range(5)]
            b = [[0] * 5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    b[y][(2 * x + 3 * y) % 5] = self._rol(st[x][y], self.ROT[x][y])
            st = [[b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) for y in range(5)]
                  for x in range(5)]
            st[0][0] ^= rc
        return st

    def digest(self, data: bytes) -> bytes:
        rate = 136
        data = bytearray(data)
        data.append(0x01)
        while len(data) % rate:
            data.append(0)
        data[-1] |= 0x80
        st = [[0] * 5 for _ in range(5)]
        for off in range(0, len(data), rate):
            blk = data[off:off + rate]
            for i in range(rate // 8):
                st[i % 5][i // 5] ^= int.from_bytes(blk[i * 8:(i + 1) * 8], "little")
            st = self._f(st)
        out = b""
        for i in range(4):
            out += st[i % 5][i // 5].to_bytes(8, "little")
        return out


def selector(sig: str) -> str:
    return "0x" + _keccak(sig.encode()).hex()[:8]


def enc_uint(v: int) -> str:
    return f"{v:064x}"


def enc_addr(a: str) -> str:
    return a.lower().replace("0x", "").rjust(64, "0")


class Rpc:
    def __init__(self, url: str, timeout: int = 20):
        self.url, self.timeout, self._id = url, timeout, 0

    def call(self, method: str, params: list):
        self._id += 1
        r = requests.post(self.url, json={"jsonrpc": "2.0", "id": self._id,
                                          "method": method, "params": params},
                          timeout=self.timeout)
        r.raise_for_status()
        j = r.json()
        if "error" in j:
            raise RuntimeError(j["error"])
        return j["result"]

    def chain_id(self) -> int:
        return int(self.call("eth_chainId", []), 16)

    def block_number(self) -> int:
        return int(self.call("eth_blockNumber", []), 16)

    def balance_eth(self, addr: str) -> float:
        return int(self.call("eth_getBalance", [addr, "latest"]), 16) / 1e18

    def eth_call(self, to: str, data: str) -> str:
        return self.call("eth_call", [{"to": to, "data": data}, "latest"])

    # ERC-721 / ERC-20 helpers
    def balance_of(self, contract: str, owner: str) -> int:
        return int(self.eth_call(contract, selector("balanceOf(address)") + enc_addr(owner)), 16)

    def owner_of(self, contract: str, token_id: int) -> str:
        res = self.eth_call(contract, selector("ownerOf(uint256)") + enc_uint(token_id))
        return "0x" + res[-40:]

    def erc20_decimals(self, contract: str) -> int:
        return int(self.eth_call(contract, selector("decimals()")), 16)
