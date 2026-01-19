"""Trading workflow scaffold."""
import logging
from typing import Any, Dict

from okxbot.clients.rest import OkxRestClient
from okxbot.clients.websocket import OkxWebSocketClient
from okxbot.config import Settings

logger = logging.getLogger(__name__)


class TradingWorkflow:
    """High-level trading workflow scaffold."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._rest = OkxRestClient(settings)
        self._ws_public = OkxWebSocketClient(settings, private=False)

    async def fetch_market_snapshot(self) -> Dict[str, Any]:
        return await self._rest.get_ticker(self._settings.trading_symbol)

    async def run(self) -> None:
        async with self._rest:
            ticker = await self.fetch_market_snapshot()
            logger.info("Ticker snapshot: %s", ticker)
