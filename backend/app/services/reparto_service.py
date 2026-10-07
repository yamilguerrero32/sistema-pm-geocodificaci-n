from fastapi import HTTPException

from sqlalchemy import text
from sqlalchemy.orm import Session

## ----------------------------------------------------------------------------------

def crear_reparto(
    db: Session,
    cliente_id: int,
    estado: str,
):
    cliente_existe = db.execute(
        text("""
            SELECT id
            FROM clientes
            WHERE id = :cliente_id
        """),
        {"cliente_id": cliente_id},
    ).first()

    if cliente_existe is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado",
        )

    consulta = text("""
        INSERT INTO repartos (
            cliente_id,
            estado
        )
        VALUES (
            :cliente_id,
            :estado
        )
        RETURNING id, cliente_id, estado
    """)

    resultado = db.execute(
        consulta,
        {
            "cliente_id": cliente_id,
            "estado": estado.value,
        },
    )

    reparto = resultado.mappings().first()
    db.commit()

    consulta_cliente = text("""
        SELECT
            c.nombre AS cliente_nombre,
            c.telefono,
            c.direccion,
            ST_Y(c.ubicacion) AS latitud,
            ST_X(c.ubicacion) AS longitud
        FROM clientes c
        WHERE c.id = :cliente_id
    """)

    cliente = db.execute(
        consulta_cliente,
        {"cliente_id": cliente_id},
    ).mappings().first()

    return {
        **reparto,
        **cliente,
    }

## ----------------------------------------------------------------------------------------

def obtener_repartos(db: Session):
    consulta = text("""
        SELECT
            r.id,
            r.cliente_id,
            c.nombre AS cliente_nombre,
            c.telefono,
            c.direccion,
            ST_Y(c.ubicacion) AS latitud,
            ST_X(c.ubicacion) AS longitud,
            r.estado
        FROM repartos r
        INNER JOIN clientes c
            ON r.cliente_id = c.id
        ORDER BY r.id
    """)

    resultado = db.execute(consulta)

    return resultado.mappings().all()

## -----------------------------------------------------------------------------------------------------------

def actualizar_estado_reparto(
    db: Session,
    reparto_id: int,
    estado: str,
):
    reparto_existe = db.execute(
        text("""
            SELECT id
            FROM repartos
            WHERE id = :reparto_id
        """),
        {"reparto_id": reparto_id},
    ).first()

    if reparto_existe is None:
        raise HTTPException(
            status_code=404,
            detail="Reparto no encontrado",
        )

    estado_actual = db.execute(
        text("""
            SELECT estado
            FROM repartos
            WHERE id = :reparto_id
        """),
        {"reparto_id": reparto_id},
    ).scalar_one()

    transiciones_permitidas = {
        "pendiente": ["en_camino", "cancelado"],
        "en_camino": ["entregado", "cancelado"],
        "entregado": [],
        "cancelado": [],
    }

    if estado.value not in transiciones_permitidas[estado_actual]:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cambiar el estado de '{estado_actual}' a '{estado.value}'",
        )

    consulta = text("""
        UPDATE repartos
        SET estado = :estado
        WHERE id = :reparto_id
        RETURNING id, cliente_id, estado
    """)

    resultado = db.execute(
        consulta,
        {
            "reparto_id": reparto_id,
            "estado": estado.value,
        },
    )

    reparto = resultado.mappings().first()
    db.commit()

    consulta_cliente = text("""
        SELECT
            c.nombre AS cliente_nombre,
            c.telefono,
            c.direccion,
            ST_Y(c.ubicacion) AS latitud,
            ST_X(c.ubicacion) AS longitud
        FROM clientes c
        WHERE c.id = :cliente_id
    """)

    cliente = db.execute(
        consulta_cliente,
        {"cliente_id": reparto["cliente_id"]},
    ).mappings().first()

    return {
        **reparto,
        **cliente,
    }

## ------------------------------------------------------------------

def eliminar_reparto(
    db: Session,
    reparto_id: int,
):
    reparto = db.execute(
        text("""
            SELECT id, estado
            FROM repartos
            WHERE id = :reparto_id
        """),
        {"reparto_id": reparto_id},
    ).mappings().first()

    if reparto is None:
        raise HTTPException(
            status_code=404,
            detail="Reparto no encontrado",
        )

    if reparto["estado"] == "entregado":
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un reparto entregado",
        )

    db.execute(
        text("""
            DELETE FROM repartos
            WHERE id = :reparto_id
        """),
        {"reparto_id": reparto_id},
    )

    db.commit()

    return {
        "mensaje": "Reparto eliminado correctamente",
        "id": reparto_id,
    }

## -----------------------------------------------------------------

def obtener_reparto_por_id(
    db: Session,
    reparto_id: int,
):
    consulta = text("""
        SELECT
            r.id,
            r.cliente_id,
            c.nombre AS cliente_nombre,
            c.telefono,
            c.direccion,
            ST_Y(c.ubicacion) AS latitud,
            ST_X(c.ubicacion) AS longitud,
            r.estado
        FROM repartos r
        INNER JOIN clientes c
            ON r.cliente_id = c.id
        WHERE r.id = :reparto_id
    """)

    reparto = db.execute(
        consulta,
        {"reparto_id": reparto_id},
    ).mappings().first()

    if reparto is None:
        raise HTTPException(
            status_code=404,
            detail="Reparto no encontrado",
        )

    return reparto

## -------------------------------------------------------

