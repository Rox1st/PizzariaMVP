from app.factories.orders import factory_for
from app.models.entities import OrderType
from app.observers.status import OrderSubject, StatusHistoryObserver


class OrderService:
    def __init__(self, order_repository, product_repository, fee_strategy):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.fee_strategy = fee_strategy
        self.subject = OrderSubject()
        self.subject.attach(StatusHistoryObserver(order_repository))

    def create_order(self, data):
        customer = data.get('customer_name', '').strip()
        phone = data.get('phone', '').strip()
        if not customer or not phone:
            raise ValueError('Nome e telefone são obrigatórios.')

        order_type = OrderType(data.get('order_type', 'DELIVERY'))
        raw_items = data.get('items', [])
        if not raw_items:
            raise ValueError('O pedido precisa ter pelo menos um item.')

        items = []
        subtotal = 0.0
        for raw in raw_items:
            product = self.product_repository.find(int(raw['product_id']))
            quantity = int(raw['quantity'])
            if not product or not product['available']:
                raise ValueError('Produto indisponível.')
            if quantity <= 0:
                raise ValueError('Quantidade deve ser maior que zero.')
            price = float(product['price'])
            subtotal += price * quantity
            from app.models.entities import OrderItem
            items.append(OrderItem(product['id'], quantity, price))

        fee = self.fee_strategy.calculate(order_type)
        total = round(subtotal + fee, 2)
        factory = factory_for(order_type)
        order = factory.create(customer, phone, data.get('address', '').strip(),
                               data.get('payment_method', 'PIX'), fee, total)
        order_id = self.order_repository.create(order, items)
        return self.order_repository.find(order_id)

    def change_status(self, order_id, new_status):
        old_status = self.order_repository.update_status(order_id, new_status)
        if old_status is None:
            raise ValueError('Pedido não encontrado.')
        self.subject.notify(order_id, old_status, new_status)
        return self.order_repository.find(order_id)

    def mark_paid(self, order_id):
        if not self.order_repository.mark_paid(order_id):
            raise ValueError('Pedido não encontrado.')
        return self.order_repository.find(order_id)
