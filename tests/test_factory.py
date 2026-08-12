from app.factories.orders import DeliveryOrderFactory, PickupOrderFactory
from app.models.entities import OrderType


def test_delivery_factory():
    order = DeliveryOrderFactory().create('Ana', '999', 'Rua A', 'PIX', 5, 50)
    assert order.order_type == OrderType.DELIVERY
    assert order.address == 'Rua A'


def test_pickup_factory():
    order = PickupOrderFactory().create('Ana', '999', 'ignorado', 'PIX', 0, 45)
    assert order.order_type == OrderType.PICKUP
    assert order.address is None
