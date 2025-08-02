from typing import Optional, List
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    sku: Optional[str] = Field(None, description="SKU if present")
    description: Optional[str] = None
    qty: Optional[float] = 1.0
    unit_price: Optional[float] = None
    total: Optional[float] = None

class PaymentInfo(BaseModel):
    method: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    tip: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = "USD"

class VendorMetadata(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    website: Optional[str] = None
    invoice_no: Optional[str] = None

class ExtractionResult(BaseModel):
    vendor: VendorMetadata = VendorMetadata()
    items: List[LineItem] = []
    payment: PaymentInfo = PaymentInfo()
    raw_text: str = ""
