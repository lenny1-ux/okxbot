"""Entrypoint for okxbot."""
import asyncio
import logging

from okxbot.config import get_settings
from okxbot.env import load_env
from okxbot.trading.workflow import TradingWorkflow


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    load_env()
    settings = get_settings()
    workflow = TradingWorkflow(settings)
    await workflow.run()


if __name__ == "__main__":
    asyncio.run(main())
