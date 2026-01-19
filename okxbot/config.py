import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    okx_api_key: str = ""
    okx_api_secret: str = ""
    okx_passphrase: str = ""
    okx_base_url: str = "https://www.okx.com"
    okx_ws_public_url: str = "wss://ws.okx.com:8443/ws/v5/public"
    okx_ws_private_url: str = "wss://ws.okx.com:8443/ws/v5/private"
    trading_symbol: str = "BTC-USDT"
    demo_trading: bool = False

    model_config = SettingsConfigDict(
        env_prefix="OKXBOT_",
        env_file=os.environ.get("OKXBOT_ENV_FILE", ".env"),
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()