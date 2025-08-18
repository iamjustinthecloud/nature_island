from __future__ import annotations
import os
from attrs import define


def _env(name: str, default: str | None = None) -> str:
    v = os.getenv(name)
    if not v:
        if default is not None:
            return default  # Use the default instead of raising error
        raise RuntimeError(f"Missing env var: {name}")
    return v


AWS_REGION = _env("AWS_REGION", "eu-west-1")


@define(slots=True, frozen=True, kw_only=True)
class AppConfig:
    table_name: str
    aws_region: str

    @staticmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            table_name=os.environ.get("TABLE_NAME", "table_name"),
            aws_region=os.environ.get("AWS_REGION", "aws_region"),
        )
