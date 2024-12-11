from uuid import UUID

from src.core.domain.order import OrderAggregate, OrderLine
from src.core.ports.order_serviec import OrderServiceAPI


class OrderService(OrderServiceAPI):
    def __init__(self, order_repository) -> None:
        self.order_repository = order_repository

    def create_order(
        self, consumer_id: UUID, order_lines: list[OrderLine]
    ) -> OrderAggregate:
        order = OrderAggregate(
            order_id=UUID(), order_lines=order_lines, customer_id=consumer_id
        )
        return order

    def cancel_order(self, order_id: UUID):
        pass
