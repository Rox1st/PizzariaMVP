from dataclasses import dataclass
from enum import Enum


class OrderType(str, Enum):
    DELIVERY = 'DELIVERY'
    PICKUP = 'PICKUP'


class OrderStatus(str, Enum):
    RECEIVED = 'RECEBIDO'
    PREPARING = 'EM_PREPARO'
    READY = 'PRONTO'
    OUT_FOR_DELIVERY = 'SAIU_PARA_ENTREGA'
    DELIVERED = 'ENTREGUE'
    CANCELLED = 'CANCELADO'


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    category: str
    price: float
    available: bool = True


@dataclass(frozen=True)
class OrderItem:
    product_id: int
    quantity: int
    unit_price: float


@dataclass
class Order:
    id: int | None
    customer_name: str
    phone: str
    address: str | None
    order_type: OrderType
    status: OrderStatus
    payment_method: str
    paid: bool
    delivery_fee: float
    total: float
