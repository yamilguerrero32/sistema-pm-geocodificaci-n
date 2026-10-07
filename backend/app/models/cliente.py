# ------------------------------ Este modulo es donde se crea la tabla cliente. ------------------------------------

from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(255), nullable=False)
    ubicacion = Column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
            dimension=2,
            spatial_index=True,
        ),
        nullable=False,
    )