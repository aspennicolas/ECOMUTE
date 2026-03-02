from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Bike(Base):
    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    battery: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    rentals: Mapped[List["Rental"]] = relationship(back_populates="bike")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    rentals: Mapped[List["Rental"]] = relationship(back_populates="user")


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Keep rentals for history if bike/user is deleted: FK can become NULL
    bike_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("bikes.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    bike: Mapped[Optional["Bike"]] = relationship(back_populates="rentals")
    user: Mapped[Optional["User"]] = relationship(back_populates="rentals")