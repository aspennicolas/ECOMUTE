from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Base is the parent class for all SQLAlchemy ORM models.
# Every table class below must inherit from it so SQLAlchemy can track them.
class Base(DeclarativeBase):
    pass


# Each class below maps directly to a database table.
# 'Mapped[type]' + 'mapped_column(...)' is the modern SQLAlchemy 2.x way
# to define columns with full type information.

class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=10)


class Bike(Base):
    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    battery: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)  # "available", "rented", or "maintenance"
    station_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # NULL if not docked

    # One bike can have many rentals over its lifetime.
    # 'back_populates' links this side to Rental.bike so both sides stay in sync.
    rentals: Mapped[List["Rental"]] = relationship(back_populates="bike")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False, default="rider")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # One user can have many rentals.
    rentals: Mapped[List["Rental"]] = relationship(back_populates="user")


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Keep rentals for history if bike/user is deleted: FK can become NULL
    # ondelete="SET NULL" means the DB sets these to NULL instead of deleting the rental row.
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

    # These give us easy access to the full Bike/User object from a Rental instance.
    bike: Mapped[Optional["Bike"]] = relationship(back_populates="rentals")
    user: Mapped[Optional["User"]] = relationship(back_populates="rentals")
