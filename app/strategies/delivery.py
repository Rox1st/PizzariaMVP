from abc import ABC, abstractmethod
from app.models.entities import OrderType


class DeliveryFeeStrategy(ABC):
    @abstractmethod
    def calculate(self, order_type: OrderType) -> float:
        raise NotImplementedError


class FixedDeliveryFeeStrategy(DeliveryFeeStrategy):
    def __init__(self, fee: float = 5.0):
        self.fee = fee

    def calculate(self, order_type: OrderType) -> float:
        return self.fee if order_type == OrderType.DELIVERY else 0.0
