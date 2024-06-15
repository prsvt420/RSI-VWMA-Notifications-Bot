from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    ...


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    is_notifications_enabled: Mapped[bool]
    is_superuser: Mapped[bool]

    def __str__(self) -> str:
        return f'{self.telegram_id}'


class Subscriptions(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    subscription_end_datetime: Mapped[datetime]

    def __str__(self) -> str:
        return f"{self.user_id} - {self.subscription_end_datetime}"


class NotificationsUser(Base):
    __tablename__ = 'notifications_user'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    notification_id: Mapped[int] = mapped_column(ForeignKey('notifications.id'))
    is_active: Mapped[bool]

    def __str__(self) -> str:
        return f'{self.user_id} - {self.notification_id}'


class Notifications(Base):
    __tablename__ = 'notifications'

    id: Mapped[int_pk]
    symbol: Mapped[str]
    interval: Mapped[str]
    rsi_period: Mapped[int] = mapped_column(default=7)
    ma_period: Mapped[int] = mapped_column(default=7)

    def __str__(self) -> str:
        return f'{self.symbol} - {self.interval} - {self.rsi_period} - {self.ma_period}'
