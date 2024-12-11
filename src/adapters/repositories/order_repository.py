from uuid import UUID

from src.core.domain.order import OrderAggregate
from src.ports.outgoing.order_repository_port import OrderRepositoryPort


class OrderRepository(OrderRepositoryPort):
    def __init__(self):
        pass

    def save(self, order: OrderAggregate):
        pass

    def find_by_id(self, order_id: UUID) -> OrderAggregate:
        pass
