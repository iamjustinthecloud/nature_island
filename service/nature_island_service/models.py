from __future__ import annotations
from attrs import define, field, validators
from datetime import datetime, timezone
from typing import Optional
import uuid


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _non_empty(s: str) -> str:
    s = s.strip()
    if not s:
        raise ValueError("must be non-empty")
    return s


@define(slots=True, frozen=True, kw_only=True)
class Item:
    id: str = field(factory=lambda: str(uuid.uuid4()))
    name: str = field(converter=lambda s: s.strip(), validator=validators.min_len(1))
    location: str = field(converter=lambda s: s.strip(), validator=validators.min_len(1))
    created_at: str = field(factory=_iso_now)
