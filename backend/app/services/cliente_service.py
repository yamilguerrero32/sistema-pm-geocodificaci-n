from fastapi import HTTPException

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.zonas_service import obtener_zona_cliente
from app.services.geocoding_service import geocodificar_direccion

## ------------------------------- CREAR CLIENTES -----------------------------
def crear_cliente(
    db: Session,
    nombre: str,
    telefono: str,
    direccion: str,
):
    coordenadas = geocodificar_direccion(direccion)

    if coordenadas is None:
        raise HTTPException(
            status_code=404,
            detail="No se pudo encontrar la dirección",
        )

    latitud = coordenadas["latitud"]
    longitud = coordenadas["longitud"]

    consulta = text("""
        INSERT INTO clientes (
            nombre,
            telefono,
            direccion,
            ubicacion
        )
        VALUES (
            :nombre,
            :telefono,
            :direccion,
            ST_SetSRID(
                ST_MakePoint(:longitud, :latitud),
                4326
            )
        )
        RETURNING
            id,
            nombre,
            telefono,
            direccion,
            ST_Y(ubicacion) AS latitud,
            ST_X(ubicacion) AS longitud
    """)

    resultado = db.execute(
        consulta,
        {
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
            "latitud": latitud,
            "longitud": longitud,
        },
    )

    cliente = resultado.mappings().first()
    db.commit()

    zona = obtener_zona_cliente(
        db=db,
        cliente_id=cliente["id"],
    )

    return {
        **cliente,
        "zona": zona,
    }

## ------------------------------- CONSULTAR CLIENTES -----------------------------

def obtener_clientes(db: Session):
    consulta = text("""
        SELECT
            id,
            nombre,
            telefono,
            direccion,
            ST_Y(ubicacion) AS latitud,
            ST_X(ubicacion) AS longitud
        FROM clientes
        ORDER BY id
    """)

    resultados = db.execute(consulta).mappings().all()

    clientes = []

    for cliente in resultados:
        zona = obtener_zona_cliente(
            db=db,
            cliente_id=cliente["id"],
        )

        clientes.append({
            **cliente,
            "zona": zona,
        })

    return clientes

## -------------------------------- OBTENER CLIENTE POR SU ID -------------------------------

def obtener_cliente_por_id(
    db: Session,
    cliente_id: int,
):
    consulta = text("""
        SELECT
            id,
            nombre,
            telefono,
            direccion,
            ST_Y(ubicacion) AS latitud,
            ST_X(ubicacion) AS longitud
        FROM clientes
        WHERE id = :cliente_id
    """)

    cliente = db.execute(
        consulta,
        {"cliente_id": cliente_id},
    ).mappings().first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado",
        )

    zona = obtener_zona_cliente(
        db=db,
        cliente_id=cliente_id,
    )

    return {
        **cliente,
        "zona": zona,
    }

## ------------------------------- ELIMINAR CLIENTE -----------------------------

def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.execute(
        text("""
            SELECT id
            FROM clientes
            WHERE id = :cliente_id
        """),
        {"cliente_id": cliente_id},
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado",
        )

    db.execute(
        text("""
            DELETE FROM clientes
            WHERE id = :cliente_id
        """),
        {"cliente_id": cliente_id},
    )

    db.commit()

    return {
        "mensaje": "Cliente eliminado correctamente",
        "id": cliente_id,
    }