from __future__ import annotations
import json
import boto3
from typing import Any, Dict
from cattrs import structure, unstructure
from .config import AppConfig
from .dto import ItemCreate, ItemsResponse
from .models import Item

_cfg = AppConfig.from_env()
_table = boto3.resource("dynamodb", region_name=_cfg.aws_region).Table(_cfg.table_name)


def _resp(code: int, body: dict) -> dict:
    return {"statusCode": code, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}


def handler(event: Dict[str, Any], _: Any) -> dict:
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod", "GET")

    if method == "POST":
        try:
            raw = json.loads(event.get("body") or "{}")
            dto = structure(raw, ItemCreate)
            item = Item(name=dto.name, location=dto.location)
            _table.put_item(Item=unstructure(item))
            return _resp(201, unstructure(item))
        except Exception as e:
            return _resp(400, {"message": f"Invalid payload: {e}"})

    if method == "GET":
        items = _table.scan().get("Items", [])
        return _resp(200, unstructure(ItemsResponse(items=items)))

    return _resp(405, {"message": "Method not allowed"})
