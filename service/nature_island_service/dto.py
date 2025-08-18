from __future__ import annotations
from attrs import define, validators, field
from typing import Optional


@define(slots=True, frozen=True, kw_only=True)
class ItemCreate:
    name: str = field(validator=validators.min_len(1))
    location: str = field(validator=validators.min_len(1))


@define(slots=True, frozen=True, kw_only=True)
class ItemsResponse:
    items: list[dict]


@define(slots=True, frozen=True, kw_only=True)
class ItemUpdate:
    name: Optional[str] = None
    location: Optional[str] = None
