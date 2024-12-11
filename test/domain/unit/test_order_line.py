import pytest

from src.core.domain.order import OrderLine
from src.generated import order_pb2


def test_check_valid_data():
    assert OrderLine._check_data(1, 10)


def test_check_data_invalid_quantity_type():
    with pytest.raises(
        ValueError, match="Quantity must be int, not <class 'str'>"
    ):
        OrderLine._check_data(1, "10")


def test_check_data_invalid_quantity_value():
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        OrderLine._check_data(1, 0)


def test_check_data_invalid_product_id_type():
    with pytest.raises(
        ValueError, match="product_id must be int, not <class 'str'>"
    ):
        OrderLine._check_data("1", 10)


def test_check_data_invalid_product_id_value():
    with pytest.raises(ValueError, match="product_id must be non-negative"):
        OrderLine._check_data(-1, 10)


def test_to_proto():
    order_line = OrderLine(product_id=1, quantity=2)
    proto_order_line = order_line.to_proto()
    assert proto_order_line.product_id == 1
    assert proto_order_line.quantity == 2


def test_to_proto_invalid():
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        OrderLine(0, 0).to_proto()


def test_from_proto():
    proto_order_line = order_pb2.OrderLine(product_id=1, quantity=2)
    order_line = OrderLine.from_proto(proto_order_line)
    assert order_line.product_id == 1
    assert order_line.quantity == 2


def test_from_proto_invalid():
    proto_order_line = order_pb2.OrderLine(product_id=1, quantity=0)
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        OrderLine.from_proto(proto_order_line)
