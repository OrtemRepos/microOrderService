from uuid import uuid4

import pytest

from src.core.domain.order import OrderAggregate, OrderLine, OrderStatus


@pytest.fixture
def order_line():
    return OrderLine(product_id=1, quantity=2)


@pytest.fixture
def order_aggregate(order_line):
    order_id = uuid4()
    customer_id = uuid4()
    order_lines = [order_line]
    return OrderAggregate(order_id, order_lines, customer_id)


def test_order_aggregate_initialization(order_aggregate, order_line):
    assert order_aggregate.order_id is not None
    assert order_aggregate.order_lines == [order_line]
    assert order_aggregate.customer_id is not None
    assert order_aggregate.order_status == OrderStatus.pending


def test_order_status_transition_from_pending(order_aggregate):
    """Test valid transitions from 'pending' status."""
    assert order_aggregate.order_status == OrderStatus.pending

    order_aggregate.order_status = OrderStatus.consumer_validate
    assert order_aggregate.order_status == OrderStatus.consumer_validate

    order_aggregate.order_status = OrderStatus.order_details_validate
    assert order_aggregate.order_status == OrderStatus.validate


def test_order_status_transition_from_consumer_validate(order_aggregate):
    """Test valid transitions from 'consumer_validate' status."""
    order_aggregate.order_status = OrderStatus.consumer_validate

    order_aggregate.order_status = OrderStatus.order_details_validate
    assert order_aggregate.order_status == OrderStatus.validate

    order_aggregate.order_status = OrderStatus.reject
    assert order_aggregate.order_status == OrderStatus.reject

    with pytest.raises(
        ValueError,
        match=f"Invalid transition from {OrderStatus.reject} "
        f"to {OrderStatus.pending}",
    ):
        order_aggregate.order_status = OrderStatus.pending


def test_order_status_transition_from_order_details_validate(order_aggregate):
    """Test valid transitions from 'order_details_validate' status."""
    order_aggregate.order_status = OrderStatus.order_details_validate

    order_aggregate.order_status = OrderStatus.consumer_validate
    assert order_aggregate.order_status == OrderStatus.validate

    order_aggregate.order_status = OrderStatus.reject
    assert order_aggregate.order_status == OrderStatus.reject

    with pytest.raises(
        ValueError,
        match=f"Invalid transition from {OrderStatus.reject} "
        f"to {OrderStatus.consumer_validate}",
    ):
        order_aggregate.order_status = OrderStatus.consumer_validate


def test_invalid_order_status(order_aggregate):
    """Test that setting an invalid order status raises a ValueError."""
    with pytest.raises(
        ValueError, match="Invalid order status: invalid_status"
    ):
        order_aggregate.order_status = "invalid_status"
