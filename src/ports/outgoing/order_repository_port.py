from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.order import OrderAggregate


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: OrderAggregate):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, order_id: UUID) -> OrderAggregate:
        raise NotImplementedError
