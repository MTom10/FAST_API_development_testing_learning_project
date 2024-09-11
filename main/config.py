"""
Config which reads from .env
and different configuration values (for development, test, production for example)
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = "dev"

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


# caching for calling the function once, getting config and keeping it saved for next app runs
@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
#    return configs[env_state]()

    if env_state is None:
        raise ValueError("ENV_STATE is not set")

    try:
        return configs[env_state]()
    except KeyError:
        raise ValueError(f"Invalid ENV_STATE: {env_state}. Valid options are 'dev', 'prod', 'test'.")


config = get_config(BaseConfig().ENV_STATE)
