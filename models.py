from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from uuid import uuid4

@dataclass
class InventoryItem:
    product_name: str
    id: str = field(default_factory=lambda: str(uuid4()))
    brands: Optional[str] = None
    ingredients_text: Optional[str] = None
    stock: int = 0
    price: float = 0.0
    barcode: Optional[str] = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if self.stock < 0:
            raise ValueError("Stock cannot be negative")
        if self.price < 0:
            raise ValueError("Price cannot be negative")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'product_name': self.product_name,
            'brands': self.brands,
            'ingredients_text': self.ingredients_text,
            'stock': self.stock,
            'price': self.price,
            'barcode': self.barcode
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        return cls(**data)

