from abc import ABC, abstractmethod
from app.models.entities import Order, OrderStatus, OrderType


class OrderFactory(ABC):
    @abstractmethod
    def create(self, customer_name, phone, address, payment_method, fee, total):
        raise NotImplementedError


class DeliveryOrderFactory(OrderFactory):
    def create(self, customer_name, phone, address, payment_method, fee, total):
        if not address:
            raise ValueError('Endereço é obrigatório para delivery.')
        return Order(None, customer_name, phone, address, OrderType.DELIVERY,
                     OrderStatus.RECEIVED, payment_method, False, fee, total)


class PickupOrderFactory(OrderFactory):
    def create(self, customer_name, phone, address, payment_method, fee, total):
        return Order(None, customer_name, phone, None, OrderType.PICKUP,
                     OrderStatus.RECEIVED, payment_method, False, fee, total)


def factory_for(order_type: OrderType) -> OrderFactory:
    return DeliveryOrderFactory() if order_type == OrderType.DELIVERY else PickupOrderFactory()
