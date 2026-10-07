from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import ClienteCreate, ClienteResponse
from app.services.cliente_service import (
    crear_cliente,
    obtener_clientes,
    obtener_cliente_por_id,
    eliminar_cliente,
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)

## ----------------------- CREAR CLIENTE --------------------------------

@router.post("/", response_model=ClienteResponse)
def crear(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
):
    return crear_cliente(
    db=db,
    nombre=cliente.nombre,
    telefono=cliente.telefono,
    direccion=cliente.direccion,
    )

## ----------------------- OBTENER CLIENTE POR ID -------------------------------------

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_por_id(
    cliente_id: int,
    db: Session = Depends(get_db),
):
    return obtener_cliente_por_id(
        db=db,
        cliente_id=cliente_id,
    )

## ---------------------- OBTENER TODOS LOS CLIENTES -----------------------------------

@router.get("/", response_model=List[ClienteResponse])
def listar(db: Session = Depends(get_db)):
    return obtener_clientes(db)

## ------------------------ ELIMINAR CLIENTE ------------------------------------

@router.delete("/{cliente_id}")
def eliminar(
    cliente_id: int,
    db: Session = Depends(get_db),
):
    return eliminar_cliente(
        db=db,
        cliente_id=cliente_id,
    )