from __future__ import annotations
import os
from attrs import define

def _env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env var: {name}")
    return v

@define(slots=True, frozen=True, kw_only=True)
class AppConfig:
    table_name: str

    @staticmethod
    def from_env() -> "AppConfig":
        return AppConfig(table_name=_env("TABLE_NAME"))
