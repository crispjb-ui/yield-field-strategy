"""Identify and read newly published contracts (Cornhub, $YIELD pool, $YIELD token) with the bundled ABIs."""
from __future__ import annotations
from .abi import Contract
from .rpc import Rpc

PACKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]


def _try(c: Contract, name: str, *args):
    try:
        return c.call(name, *args)
    except Exception:
        return None


def probe_cornhub(rpc: Rpc, addr: str) -> dict | None:
    c = Contract(rpc, addr, "abi_2")
    farmer = _try(c, "farmerFeeBps")
    market = _try(c, "marketFeeBps")
    if farmer is None or market is None:
        return None
    prices = {}
    for i, name in enumerate(PACKS):
        p = _try(c, "packPrice", i)
        if p is not None:
            prices[name] = p / 1e18
    pig = _try(c, "trufflePigFee")
    flt = _try(c, "floatBalance")
    return {"kind": "cornhub", "address": addr, "farmer_fee_pct": farmer / 100, "market_fee_pct": market / 100,
            "pack_fee_pct": (_try(c, "packFeeBps") or 0) / 100, "pack_prices_eth": prices,
            "truffle_pig_eth": pig / 1e18 if pig is not None else None,
            "float_eth": flt / 1e18 if flt is not None else None, "paused": _try(c, "paused"),
            "owner": _try(c, "owner"), "fee_destination": _try(c, "feeDestination"),
            "swap_router": _try(c, "swapRouter")}


def probe_pool(rpc: Rpc, addr: str) -> dict | None:
    c = Contract(rpc, addr, "abi_3")
    buy = _try(c, "buyFeeBps")
    eth = _try(c, "ethReserve")
    if buy is None or eth is None:
        return None
    return {"kind": "yield_pool", "address": addr, "buy_fee_pct": buy / 100,
            "sell_fee_pct": (_try(c, "sellFeeBps") or 0) / 100,
            "max_sell_fee_pct": (_try(c, "maxSellFeeBps") or 0) / 100,
            "eth_reserve": eth / 1e18, "virtual_eth_reserve": (_try(c, "virtualEthReserve") or 0) / 1e18,
            "yield_reserve": (_try(c, "yieldReserve") or 0) / 1e18, "spot_price_raw": _try(c, "spotPrice"),
            "yield_token": _try(c, "yieldToken")}


def probe_token(rpc: Rpc, addr: str) -> dict | None:
    c = Contract(rpc, addr, "abi_5")
    sup = _try(c, "totalSupply")
    sym = _try(c, "symbol")
    if sup is None or sym is None:
        return None
    return {"kind": "erc20", "address": addr, "symbol": sym, "total_supply": sup / 1e18}


def probe(rpc: Rpc, addr: str) -> dict:
    for fn in (probe_cornhub, probe_pool, probe_token):
        r = fn(rpc, addr)
        if r:
            return r
    code = rpc.call("eth_getCode", [addr, "latest"])
    return {"kind": "unknown", "address": addr, "code_bytes": (len(code) - 2) // 2}


def rake_from_cornhub(c: dict, ev_x: float = 0.995) -> dict:
    """Exact loop economics from the live fees."""
    return {"market_payout_per_eth": ev_x * (1 - c["market_fee_pct"] / 100),
            "farmer_eth_into_swap_per_eth": ev_x * (1 - c["farmer_fee_pct"] / 100),
            "market_rake_pct": (1 - ev_x * (1 - c["market_fee_pct"] / 100)) * 100,
            "farmer_breakeven_buy_tax_pct": (1 - ev_x * (1 - c["farmer_fee_pct"] / 100)) * 100}
