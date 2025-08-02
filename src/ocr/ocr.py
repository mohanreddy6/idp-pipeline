# src/ocr/validate.py
from __future__ import annotations

from typing import Any, Dict, List, Optional


def _num(x: Any) -> Optional[float]:
    """Best-effort numeric parsing. Returns None if not parseable."""
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None


def calc_subtotal_from_items(items: List[Dict[str, Any]]) -> Optional[float]:
    """Sum item totals; returns None if items is empty or totals missing."""
    if not items:
        return None

    total = 0.0
    saw_any = False
    for it in items:
        val = _num(it.get("total"))
        if val is not None:
            total += val
            saw_any = True

    return total if saw_any else None
