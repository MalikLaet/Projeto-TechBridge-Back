from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_tech.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone: Mapped[str]


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    cnpj: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone: Mapped[str]

    cursos: Mapped[List['Curso']] = relationship(
        'Curso', back_populates='empresa'
    )


class Curso(Base):
    __tablename__ = 'cursos'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    youtube_link: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))

    empresa = relationship('Company', back_populates='cursos')
