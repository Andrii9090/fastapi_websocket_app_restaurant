from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import Base


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default='true')

    def __repr__(self):
        return f'<Product {self.name}>'

    def __str__(self):
        return f'{self.id} - {self.name}'

    def __eq__(self, other):
        return self.id == other.id
