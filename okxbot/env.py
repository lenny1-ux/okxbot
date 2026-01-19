import os

from dotenv import load_dotenv


DEFAULT_ENV_FILE = os.environ.get("OKXBOT_ENV_FILE", ".env")


def load_env(env_file: str = DEFAULT_ENV_FILE) -> None:
    """Load environment variables from a dotenv file."""
    load_dotenv(env_file)
