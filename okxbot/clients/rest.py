"""Async REST client for OKX."""
import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

import aiohttp

from okxbot.config import Settings


class OkxRestClient:
    """Minimal async REST client for OKX."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "OkxRestClient":
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session:
            await self._session.close()

    def _sign(self, timestamp: str, method: str, path: str, body: str) -> str:
        payload = f"{timestamp}{method.upper()}{path}{body}"
        mac = hmac.new(
            self._settings.okx_api_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return base64.b64encode(mac).decode()

    def _headers(self, method: str, path: str, body: str) -> Dict[str, str]:
        timestamp = str(time.time())
        signature = self._sign(timestamp, method, path, body)
        return {
            "OK-ACCESS-KEY": self._settings.okx_api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self._settings.okx_passphrase,
            "Content-Type": "application/json",
            "x-simulated-trading": "1" if self._settings.demo_trading else "0",
        }

    async def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
        private: bool = False,
    ) -> Dict[str, Any]:
        if not self._session:
            self._session = aiohttp.ClientSession()
        body = json.dumps(payload) if payload else ""
        headers = self._headers(method, path, body) if private else {}
        url = f"{self._settings.okx_base_url}{path}"
        async with self._session.request(method, url, data=body or None, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_ticker(self, instrument_id: str) -> Dict[str, Any]:
        return await self._request("GET", f"/api/v5/market/ticker?instId={instrument_id}")

    async def place_order(self, instrument_id: str, side: str, size: str) -> Dict[str, Any]:
        payload = {
            "instId": instrument_id,
            "tdMode": "cash",
            "side": side,
            "ordType": "market",
            "sz": size,
        }
        return await self._request("POST", "/api/v5/trade/order", payload=payload, private=True)
