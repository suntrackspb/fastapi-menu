from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app.db.db_base import Base
from sqlalchemy import Column, String, ForeignKey, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import func


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey(
        "submenus.id", ondelete='CASCADE'), nullable=False)
    submenus = relationship('Submenu', back_populates='dishes')
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey(
        'menus.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish', back_populates='submenus',
        cascade="all,delete", passive_deletes=True
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .scalar_subquery()
    )


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)
    submenus = relationship(
        "Submenu",
        cascade="all,delete", passive_deletes=True, back_populates="menu"
    )
    submenus_count = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery()
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .join(Submenu, Submenu.menu_id == id)
        .where(Dish.submenu_id == Submenu.id)
        .correlate_except(Submenu)
        .scalar_subquery()
    )

