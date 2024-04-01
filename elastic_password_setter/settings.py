# pylint:disable=R0903
""" Settings for the application """
import os
from pathlib import Path
from typing import Any

from envyaml import EnvYAML
from pydantic import BaseModel, Field


PROJECT_ROOT_PATH: Path = Path(__file__).parents[1]
_settings_folder = os.environ.get("ELASTIC_PASSWORD_SETTER_SETTINGS_FOLDER", PROJECT_ROOT_PATH)


class ElasticSettings(BaseModel):
    host: str = Field(
        "localhost",
        description="FQDN of the Elastic Service"
    )
    user: str = Field(
        "elastic",
        description="Username of the elastic super user"
    )
    ca_certs: str = Field(
        "",
        description="Path to the CA certificate of the server"
    )


class Settings(BaseModel):
    elastic: ElasticSettings


def load_active_settings() -> dict[str, Any]:
    path = Path(_settings_folder) / "settings.yaml"
    config = EnvYAML(path).export()
    if not isinstance(config, dict):
        raise TypeError(f"Config file has no top-level mapping: {path}")
    return config

# This is visible just for DI or testing purposes.
# Use dependency injection or `settings()` method instead.
unsafe_settings = load_active_settings()

# This is visible just for DI or testing purposes.
# Use dependency injection or `settings()` method instead.
unsafe_typed_settings = Settings(**unsafe_settings)
