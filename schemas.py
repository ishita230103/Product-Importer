from pydantic import BaseModel

class ProductInput(BaseModel):
    sku: str
    name: str = ""
    description: str = ""
    price_cents: int = 0
    active: bool = True

class WebhookInput(BaseModel):
    url: str
    event: str
    enabled: bool = True
