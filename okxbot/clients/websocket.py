"""Async WebSocket client for OKX."""
import json
from typing import Any, AsyncIterator, Dict, Optional

import websockets

from okxbot.config import Settings


class OkxWebSocketClient:
    """Minimal async WebSocket client for OKX."""

    def __init__(self, settings: Settings, private: bool = False) -> None:
        self._settings = settings
        self._private = private
        self._ws: Optional[websockets.WebSocketClientProtocol] = None

    @property
    def url(self) -> str:
        return self._settings.okx_ws_private_url if self._private else self._settings.okx_ws_public_url

    async def connect(self) -> None:
        self._ws = await websockets.connect(self.url)

    async def close(self) -> None:
        if self._ws:
            await self._ws.close()

    async def send(self, payload: Dict[str, Any]) -> None:
        if not self._ws:
            raise RuntimeError("WebSocket is not connected")
        await self._ws.send(json.dumps(payload))

    async def subscribe(self, channel: str, instrument_id: str) -> None:
        await self.send({"op": "subscribe", "args": [{"channel": channel, "instId": instrument_id}]})

    async def messages(self) -> AsyncIterator[Dict[str, Any]]:
        if not self._ws:
            raise RuntimeError("WebSocket is not connected")
        async for message in self._ws:
            yield json.loads(message)
