from typing import Protocol
from uuid import UUID


class OrderServiceAPI(Protocol):
    def create_order(self, consumer_id: UUID):
        pass

    def cancel_order(self, order_id: UUID):
        pass

    def revise_order(self, order_id: UUID):
        pass
