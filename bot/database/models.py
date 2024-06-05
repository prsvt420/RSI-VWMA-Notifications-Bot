from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    ...


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    is_subscribed: Mapped[bool]
    is_superuser: Mapped[bool]

    def __str__(self):
        return f'{self.telegram_id}'
