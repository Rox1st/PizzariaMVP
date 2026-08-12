from app.models.entities import OrderType
from app.strategies.delivery import FixedDeliveryFeeStrategy


def test_delivery_fee():
    strategy = FixedDeliveryFeeStrategy(5.0)
    assert strategy.calculate(OrderType.DELIVERY) == 5.0
    assert strategy.calculate(OrderType.PICKUP) == 0.0
