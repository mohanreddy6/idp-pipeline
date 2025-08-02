# src/llm/extract.py

from __future__ import annotations

import os
import json
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic import ValidationError

from src.utils.parser import ExtractionResult, VendorMetadata, LineItem, PaymentInfo

# Load environment variables
load_dotenv()

# DRY_RUN=1 -> return mock data (no OpenAI needed)
DRY_RUN = os.getenv("DRY_RUN", "1") == "1"

def _mock_parse(ocr_text: str) -> Dict[str, Any]:
    return {
        "vendor": {"name": "Mock Store", "invoice_no": "INV-001", "date": None, "time": None,
                   "address": None, "phone": None, "website": None},
        "items": [
            {"sku": "ABC123", "description": "Widget", "qty": 2, "unit_price": 3.5, "total": 7.0}
        ],
        "payment": {"method": "VISA ****1111", "subtotal": 7.0, "tax": 0.63, "tip": 0.0, "total": 7.63, "currency": "USD"},
        "raw_text": ocr_text
    }

def _build_prompt(ocr_text: str) -> str:
    return f"""
You are an expert in parsing noisy retail receipts and invoices.
Extract the following fields in JSON strictly matching this schema:

{{
  "vendor": {{
    "name": string|null,
    "address": string|null,
    "phone": string|null,
    "date": string|null,
    "time": string|null,
    "website": string|null,
    "invoice_no": string|null
  }},
  "items": [
    {{
      "sku": string|null,
      "description": string|null,
      "qty": number|null,
      "unit_price": number|null,
      "total": number|null
    }}
  ],
  "payment": {{
    "method": string|null,
    "subtotal": number|null,
    "tax": number|null,
    "tip": number|null,
    "total": number|null,
    "currency": string|null
  }},
  "raw_text": string
}}

Rules:
- If a field is absent in the text, use null.
- Parse numbers as numbers, not strings.
- Do not invent items; only extract what appears in the text.
- Copy the entire input as raw_text.

INPUT:
\"\"\"{ocr_text}\"\"\"
""".strip()

def _call_openai(prompt: str) -> Dict[str, Any]:
    from openai import OpenAI

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You output only valid JSON. No prose."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    content = resp.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        cleaned = content.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)

def extract_structured(ocr_text: str) -> ExtractionResult:
    if DRY_RUN:
        data = _mock_parse(ocr_text)
    else:
        prompt = _build_prompt(ocr_text)
        data = _call_openai(prompt)

    try:
        return ExtractionResult(**data)
    except ValidationError:
        # minimal repair if shapes drift
        return ExtractionResult(
            vendor=VendorMetadata(**(data.get("vendor") or {})),
            items=[LineItem(**i) for i in (data.get("items") or [])],
            payment=PaymentInfo(**(data.get("payment") or {})),
            raw_text=data.get("raw_text") or ocr_text
        )
