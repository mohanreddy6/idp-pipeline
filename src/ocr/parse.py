import re

def _money_to_float(s: str) -> float | None:
    s = s.replace(",", "").replace("O", "0")
    m = re.search(r"(\d+(?:\.\d{1,2})?)", s)
    return float(m.group(1)) if m else None

def parse_invoice(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    data = {
        "merchant": lines[0] if lines else None,
        "invoice_id": None,
        "subtotal": None,
        "tax": None,
        "total": None,
        "payment_method": None,
        "raw_text": text,
    }

    for ln in lines:
        low = ln.lower()

        if data["invoice_id"] is None:
            m = re.search(r"\binvoice\b[:\s\-]*([A-Z0-9.\-]+)", low, re.I)
            if m:
                data["invoice_id"] = m.group(1).upper()

        if data["subtotal"] is None and re.search(r"sub\s*to?t?a?l|subio?tat", low):
            data["subtotal"] = _money_to_float(ln)

        if data["tax"] is None and "tax" in low:
            data["tax"] = _money_to_float(ln)

        if data["total"] is None and "total" in low:
            data["total"] = _money_to_float(ln)

        if data["payment_method"] is None and any(k in low for k in ["visa", "mastercard", "amex", "cash", "upi"]):
            data["payment_method"] = ln.strip()

    return data
