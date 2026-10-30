"""Blockscout (v1-style ?module=...) client for Robinhood Chain explorer."""
from __future__ import annotations
import json
import requests


class Blockscout:
    def __init__(self, api: str, timeout: int = 20):
        self.api, self.timeout = api.rstrip("/"), timeout

    def _get(self, **params):
        r = requests.get(self.api, params=params, timeout=self.timeout)
        r.raise_for_status()
        j = r.json()
        if str(j.get("status")) == "0" and j.get("message") not in ("No transactions found",
                                                                      "No token transfers found"):
            raise RuntimeError(j.get("result") or j.get("message"))
        return j.get("result")

    def abi(self, address: str):
        res = self._get(module="contract", action="getabi", address=address)
        return json.loads(res) if isinstance(res, str) else res

    def is_verified(self, address: str) -> bool:
        try:
            return bool(self.abi(address))
        except Exception:
            return False

    def txlist(self, address: str, start_block: int = 0, page: int = 1, offset: int = 100):
        return self._get(module="account", action="txlist", address=address,
                         startblock=start_block, page=page, offset=offset, sort="desc") or []

    def token_transfers(self, address: str, contract: str | None = None, page: int = 1,
                        offset: int = 100):
        p = dict(module="account", action="tokentx", address=address, page=page,
                 offset=offset, sort="desc")
        if contract:
            p["contractaddress"] = contract
        return self._get(**p) or []

    def token_info(self, contract: str):
        return self._get(module="token", action="getToken", contractaddress=contract)

    def logs(self, address: str, from_block: int, to_block: str | int = "latest",
             topic0: str | None = None):
        p = dict(module="logs", action="getLogs", address=address,
                 fromBlock=from_block, toBlock=to_block)
        if topic0:
            p["topic0"] = topic0
        return self._get(**p) or []
