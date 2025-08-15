from __future__ import annotations
from attrs import define
from typing import Optional


@define(slots=True, frozen=True, kw_only=True)
class ItemCreate:
    name: str
    location: Optional[str] = None


@define(slots=True, frozen=True, kw_only=True)
class ItemsResponse:
    items: list[dict]

