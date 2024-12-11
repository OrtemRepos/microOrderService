from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "order"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, default_factory=uuid4, index=True, unique=True
    )
    order_lines: Mapped[list[int]]
    consumer_id: Mapped[UUID]
