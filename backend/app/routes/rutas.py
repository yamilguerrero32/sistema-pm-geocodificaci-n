from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import RutaOptimizadaRequest
from app.services.routing_service import (
    obtener_ruta_entre_clientes,
    obtener_clientes_para_ruta,
    optimizar_ruta_osrm,
)


router = APIRouter(
    prefix="/rutas",
    tags=["Rutas"],
)


@router.get("/{cliente_origen_id}/{cliente_destino_id}")
def obtener_ruta(
    cliente_origen_id: int,
    cliente_destino_id: int,
    db: Session = Depends(get_db),
):
    return obtener_ruta_entre_clientes(
        db=db,
        cliente_origen_id=cliente_origen_id,
        cliente_destino_id=cliente_destino_id,
    )


@router.post("/optimizar")
def optimizar_ruta(
    datos: RutaOptimizadaRequest,
    db: Session = Depends(get_db),
):
    clientes = obtener_clientes_para_ruta(
        db=db,
        clientes_ids=datos.clientes,
    )

    ruta = optimizar_ruta_osrm(clientes)

    return ruta

