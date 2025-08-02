from __future__ import annotations
from typing import Dict, List, Any, Optional

def _num(x: Any) -> Optional[float]:
    try:
        if x is None: return None
        return float(x)
    except Exception:
        return None

def _round2(x: Optional[float]) -> Optional[float]:
    return None if x is None else round(float(x) + 1e-12, 2)

def calc_subtotal_from_items(items: List[Dict[str, Any]]) -> Optional[float]:
    if not items: return None
    total = 0.0
    saw_any = False
    for it in items:
        qty = _num(it.get("qty")) or 0.0
        unit = _num(it.get("unit_price"))
        line_total = _num(it.get("total"))
        if line_total is not None:
            total += float(line_total)
            saw_any = True
        elif unit is not None:
            total += float(qty) * float(unit)
            saw_any = True
    return _round2(total) if saw_any else None

def reconcile_payment(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures subtotal/tax/tip/total are consistent. Fills missing values when
    possible and returns a _math section with status + notes.
    """
    items = parsed.get("items") or []
    pay = parsed.get("payment") or {}
    subtotal = _num(pay.get("subtotal"))
    tax = _num(pay.get("tax")) or 0.0
    tip = _num(pay.get("tip")) or 0.0
    total = _num(pay.get("total"))

    computed_subtotal = calc_subtotal_from_items(items)
    notes = []

    # Fill missing subtotal
    if subtotal is None and computed_subtotal is not None:
        subtotal = computed_subtotal
        pay["subtotal"] = subtotal
        notes.append("subtotal_computed_from_items")

    # Fill missing total
    if total is None and subtotal is not None:
        total = subtotal + tax + tip
        pay["total"] = _round2(total)
        notes.append("total_computed_from_parts")

    # Validate math if we have enough
    status = "unknown"
    if subtotal is not None and total is not None:
        expected = _round2(subtotal + tax + tip)
        if expected == _round2(total):
            status = "ok"
        else:
            status = "mismatch"
            notes.append(f"expected {expected} from subtotal+tax+tip, got {total}")

    parsed["payment"] = pay
    parsed.setdefault("_math", {})
    parsed["_math"].update({
        "status": status,
        "note": ", ".join(notes) if notes else ""
    })
    return parsed
