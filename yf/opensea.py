"""OpenSea v2 REST client scoped to the deeds collection."""
from __future__ import annotations
import requests

BASE = "https://api.opensea.io/api/v2"


class OpenSea:
    def __init__(self, api_key: str, slug: str = "yield-field-deeds", timeout: int = 20):
        self.s = requests.Session()
        self.s.headers.update({"accept": "application/json", "x-api-key": api_key or ""})
        self.slug, self.timeout = slug, timeout

    def _get(self, path: str, **params):
        r = self.s.get(f"{BASE}{path}", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def chains(self):
        """Use once to learn the Robinhood chain slug (unverified as of 2026-10-30)."""
        return self._get("/chains")

    def collection(self):
        return self._get(f"/collections/{self.slug}")

    def stats(self):
        return self._get(f"/collections/{self.slug}/stats")

    def listings(self, limit: int = 50, cursor: str | None = None):
        return self._get(f"/listings/collection/{self.slug}/all", limit=limit, next=cursor)

    def best_listings(self, limit: int = 20):
        return self._get(f"/listings/collection/{self.slug}/best", limit=limit)

    def best_offers(self, limit: int = 20):
        return self._get(f"/offers/collection/{self.slug}/all", limit=limit)

    def events(self, event_type: str = "sale", limit: int = 50, after: int | None = None):
        return self._get(f"/events/collection/{self.slug}", event_type=event_type,
                         limit=limit, after=after)

    def nft(self, chain_slug: str, contract: str, token_id: int):
        return self._get(f"/chain/{chain_slug}/contract/{contract}/nfts/{token_id}")

    def snapshot(self) -> dict:
        """Floor / best offer / volumes in one dict. Field names follow v2 stats."""
        st = self.stats()
        total = st.get("total", {})
        day = next((i for i in st.get("intervals", []) if i.get("interval") == "one_day"), {})
        out = {
            "floor_eth": total.get("floor_price"),
            "floor_symbol": total.get("floor_price_symbol"),
            "volume_total": total.get("volume"),
            "owners": total.get("num_owners"),
            "sales_total": total.get("sales"),
            "volume_24h": day.get("volume"),
            "sales_24h": day.get("sales"),
        }
        try:
            offers = self.best_offers(limit=1).get("offers", [])
            if offers:
                p = offers[0].get("price", {}).get("value")
                dec = offers[0].get("price", {}).get("decimals", 18)
                out["best_offer_eth"] = int(p) / 10 ** int(dec) if p else None
        except requests.HTTPError:
            out["best_offer_eth"] = None
        return out
