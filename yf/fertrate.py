"""Network Fertilizer rate: /api/fert-rate semantics + throttle timeline projection."""
from __future__ import annotations
import requests
from .roi import network_speed

API = "https://yieldfields.fun/api/fert-rate"


def fetch() -> dict:
    r = requests.get(API, timeout=20, headers={"accept": "application/json"})
    r.raise_for_status()
    return r.json()


def summarize(fr: dict) -> dict:
    """supply = claimedTotal − usedTotal (Bag + exported, minus used). target = targetDays × network
    daily output at full speed. networkBps = current speed."""
    out_day = fr["target"] / fr["targetDays"]
    return {"circulation": fr["supply"], "target": fr["target"], "network_output_per_day": out_day,
            "staked_fertility": out_day / 0.5, "days_in_circulation": fr["supply"] / out_day,
            "network_rate": fr["networkBps"] / 10000, "floor_rate": fr["floorBps"] / 10000,
            "used_total": fr.get("usedTotal", 0), "claimed_total": fr.get("claimedTotal")}


def project(circulation: float, out_day: float, days: int = 45, consumption_per_day: float = 0.0,
            step_hours: int = 1) -> list[dict]:
    """Hour-by-hour projection of circulation and network speed assuming everyone claims and nothing
    is used (consumption_per_day lets you model farming). Returns daily rows."""
    rows = []
    c = circulation
    for h in range(days * 24):
        d = c / out_day
        speed = network_speed(d)
        c += out_day * speed / 24 - consumption_per_day / 24
        c = max(c, 0.0)
        if (h + 1) % 24 == 0:
            rows.append({"day": (h + 1) // 24, "circulation": c, "days_of_output": c / out_day,
                         "speed": network_speed(c / out_day)})
    return rows


def milestones(circulation: float, out_day: float) -> dict:
    """Days until the network first hits 7 / 10 / 14 days of output in circulation."""
    rows = project(circulation, out_day, days=90)
    def first(th):
        for r in rows:
            if r["days_of_output"] >= th:
                return r["day"]
        return None
    return {"to_7d_slowdown_start": first(7), "to_10d_70pct": first(10), "to_14d_50pct": first(14)}
