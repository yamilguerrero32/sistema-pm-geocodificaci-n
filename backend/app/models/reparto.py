from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Reparto(Base):
    __tablename__ = "repartos"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    estado = Column(String(30), nullable=False, default="pendiente")