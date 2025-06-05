"""Utility functions for filtering parsed data."""

from __future__ import annotations

from typing import Any, Dict, List


def filter_by_price(items: List[Dict[str, Any]], min_price: int, max_price: int) -> List[Dict[str, Any]]:
    """Return advertisements with ``Цена`` between ``min_price`` and ``max_price``."""
    result: List[Dict[str, Any]] = []
    for item in items:
        price_text = str(item.get("Цена", "0")).split()[0]
        try:
            price = int(price_text)
        except ValueError:
            continue
        if min_price <= price <= max_price:
            result.append(item)
    return result
