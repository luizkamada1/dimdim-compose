from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from db import Base

class Customer(Base):
  __tablename__ = "customers"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(120), nullable=False)
  email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

  def to_dict(self):
    return {"id": self.id, "name": self.name, "email": self.email}
