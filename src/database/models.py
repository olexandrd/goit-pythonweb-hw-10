from datetime import date
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.sqltypes import Date


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50))
    birstday: Mapped[date] = mapped_column("birstday", Date, default=func.now())
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
