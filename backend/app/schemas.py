from pydantic import BaseModel
from enum import Enum


class ClienteCreate(BaseModel):
    nombre: str
    telefono: str
    direccion: str


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    direccion: str
    latitud: float
    longitud: float
    zona: int | None

    class Config:
        from_attributes = True



class EstadoReparto(str, Enum):
    pendiente = "pendiente"
    en_camino = "en_camino"
    entregado = "entregado"
    cancelado = "cancelado"


class RepartoCreate(BaseModel):
    cliente_id: int
    estado: EstadoReparto = EstadoReparto.pendiente


class RepartoResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: str
    telefono: str
    direccion: str
    latitud: float
    longitud: float
    estado: str

    class Config:
        from_attributes = True

class RepartoEstadoUpdate(BaseModel):
    estado: EstadoReparto


class RutaOptimizadaRequest(BaseModel):
    clientes: list[int]