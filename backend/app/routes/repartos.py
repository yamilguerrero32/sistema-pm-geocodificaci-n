## ------------------- Aqui la API Crea y Actualiza los Repartos -----------------------------

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import (
    RepartoCreate,
    RepartoResponse,
    RepartoEstadoUpdate,
)

from app.services.reparto_service import crear_reparto, obtener_repartos
from app.services.reparto_service import (
    crear_reparto,
    obtener_repartos,
    obtener_reparto_por_id,
    actualizar_estado_reparto,
    eliminar_reparto,
)


router = APIRouter(
    prefix="/repartos",
    tags=["Repartos"],
)

## ----------------------- POST -----------------------------------

@router.post("/", response_model=RepartoResponse)
def crear(
    reparto: RepartoCreate,
    db: Session = Depends(get_db),
):
    return crear_reparto(
        db=db,
        cliente_id=reparto.cliente_id,
        estado=reparto.estado,
    )

## ----------------------- GET -----------------------------------

@router.get("/", response_model=List[RepartoResponse])
def listar(db: Session = Depends(get_db)):
    return obtener_repartos(db)

## ----------------------- PUT -----------------------------------

@router.put("/{reparto_id}/estado", response_model=RepartoResponse)
def actualizar_estado(
    reparto_id: int,
    reparto: RepartoEstadoUpdate,
    db: Session = Depends(get_db),
):
    return actualizar_estado_reparto(
        db=db,
        reparto_id=reparto_id,
        estado=reparto.estado,
    )

## ----------------------- GET_id -----------------------------------

@router.get("/{reparto_id}", response_model=RepartoResponse)
def obtener_por_id(
    reparto_id: int,
    db: Session = Depends(get_db),
):
    return obtener_reparto_por_id(
        db=db,
        reparto_id=reparto_id,
    )

## ----------------------- DELETE -----------------------------------

@router.delete("/{reparto_id}")
def eliminar(
    reparto_id: int,
    db: Session = Depends(get_db),
):
    return eliminar_reparto(
        db=db,
        reparto_id=reparto_id,
    )

