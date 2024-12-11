from dataclasses import dataclass
from enum import StrEnum
from typing import cast
from uuid import UUID

from loguru import logger

import src.generated.order_pb2 as order_pb2


class OrderStatus(StrEnum):
    pending = "PENDING"
    consumer_validate = "CONSUMER_VALIDATE"
    order_details_validate = "ORDER_DETAILS_VALIDATE"
    validate = "VALIDATE"
    reject = "REJECT"


@dataclass
class protoOrderLine:
    product_id: int
    quantity: int


@dataclass
class OrderLine:
    product_id: int
    quantity: int

    @staticmethod
    def _check_data(product_id: int, quantity: int) -> bool:
        errors = []

        if not isinstance(quantity, int):
            errors.append(f"Quantity must be int, not {type(quantity)}")
        elif quantity <= 0:
            errors.append(f"Quantity must be greater than 0\n\t{quantity=}")

        if not isinstance(product_id, int):
            errors.append(f"product_id must be int, not {type(product_id)}")
        elif product_id < 0:
            errors.append(f"product_id must be non-negative\n\t{product_id=}")

        if errors:
            error_message = "\n".join(errors)
            logger.error(error_message, product_id, quantity, __name__)
            raise ValueError(error_message)

        return True

    def to_proto(self) -> protoOrderLine:
        OrderLine._check_data(self.product_id, self.quantity)
        return cast(
            protoOrderLine,
            order_pb2.OrderLine(
                product_id=self.product_id, quantity=self.quantity
            ),
        )

    @classmethod
    def from_proto(self, order_line: order_pb2.OrderLine) -> "OrderLine":
        OrderLine._check_data(order_line.product_id, order_line.quantity)
        return OrderLine(order_line.product_id, order_line.quantity)


class OrderAggregate:
    def __init__(
        self,
        order_id: UUID,
        order_lines: list[OrderLine],
        customer_id: UUID,
        order_status: OrderStatus = OrderStatus.pending,
    ) -> None:
        self._order_id = order_id
        self._order_lines = order_lines
        self._customer_id = customer_id
        self._order_status = order_status

    @property
    def order_id(self):
        return self._order_id

    @property
    def order_lines(self):
        return self._order_lines

    @order_lines.setter
    def order_lines(self, order_lines: list[OrderLine]):
        self._order_lines = order_lines

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def order_status(self):
        return self._order_status

    @order_status.setter
    def order_status(self, order_status: OrderStatus):
        if order_status not in OrderStatus:
            raise ValueError(
                f"Invalid order status: {order_status}. "
                f"Must be in {OrderStatus.__str__}"
            )

        if (
            self._order_status == OrderStatus.pending
            and order_status
            not in (
                OrderStatus.consumer_validate,
                OrderStatus.order_details_validate,
            )
            or self.order_status == OrderStatus.reject
            or order_status == OrderStatus.pending
        ):
            raise ValueError(
                f"Invalid transition from "
                f"{self._order_status} to {order_status}"
            )
        elif (
            self._order_status
            in (
                OrderStatus.consumer_validate,
                OrderStatus.order_details_validate,
            )
            and order_status != self.order_status
        ):
            self._order_status = OrderStatus.validate
        else:
            self._order_status = order_status
