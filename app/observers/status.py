from abc import ABC, abstractmethod


class OrderObserver(ABC):
    @abstractmethod
    def update(self, order_id, old_status, new_status):
        raise NotImplementedError


class StatusHistoryObserver(OrderObserver):
    def __init__(self, repository):
        self.repository = repository

    def update(self, order_id, old_status, new_status):
        self.repository.add_status_history(order_id, old_status, new_status)


class OrderSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: OrderObserver):
        self._observers.append(observer)

    def notify(self, order_id, old_status, new_status):
        for observer in self._observers:
            observer.update(order_id, old_status, new_status)
