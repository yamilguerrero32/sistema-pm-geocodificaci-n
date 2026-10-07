from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import requests

## ------------------- CALCULAR LAS RUTAS --------------------------------

def calcular_ruta(
    longitud_origen: float,
    latitud_origen: float,
    longitud_destino: float,
    latitud_destino: float,
):
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{longitud_origen},{latitud_origen};"
        f"{longitud_destino},{latitud_destino}"
    )

    parametros = {
        "overview": "full",
        "geometries": "geojson",
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=10,
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

    if datos["code"] != "Ok":
        return None

    ruta = datos["routes"][0]

    return {
        "distancia_metros": ruta["distance"],
        "duracion_segundos": ruta["duration"],
        "geometria": ruta["geometry"],
    }

## ----------------- SE OBTIENEN LAS RUTAS DE CLIENTE A CLIENTE ---------------------------------------

def obtener_ruta_entre_clientes(
    db: Session,
    cliente_origen_id: int,
    cliente_destino_id: int,
):
    consulta = text("""
        SELECT
            id,
            ST_Y(ubicacion) AS latitud,
            ST_X(ubicacion) AS longitud
        FROM clientes
        WHERE id IN (:cliente_origen_id, :cliente_destino_id)
    """)

    resultados = db.execute(
        consulta,
        {
            "cliente_origen_id": cliente_origen_id,
            "cliente_destino_id": cliente_destino_id,
        },
    ).mappings().all()

    if len(resultados) != 2:
        raise HTTPException(
            status_code=404,
            detail="Uno o ambos clientes no existen",
        )

    clientes = {
        cliente["id"]: cliente
        for cliente in resultados
    }

    origen = clientes[cliente_origen_id]
    destino = clientes[cliente_destino_id]

    ruta = calcular_ruta(
        longitud_origen=origen["longitud"],
        latitud_origen=origen["latitud"],
        longitud_destino=destino["longitud"],
        latitud_destino=destino["latitud"],
    )

    if ruta is None:
        raise HTTPException(
            status_code=404,
            detail="No se pudo calcular la ruta",
        )

    return {
        "cliente_origen_id": cliente_origen_id,
        "cliente_destino_id": cliente_destino_id,
        **ruta,
    }


## ----------------------- AQUI SE ESCOGEN LOS CLIENTES PARA BUSCAR UNA RUTA ------------------------------------

def obtener_clientes_para_ruta(
    db: Session,
    clientes_ids: list[int],
):
    consulta = text("""
        SELECT
            id,
            nombre,
            ST_Y(ubicacion) AS latitud,
            ST_X(ubicacion) AS longitud
        FROM clientes
        WHERE id = ANY(:ids)
    """)

    resultados = db.execute(
        consulta,
        {"ids": clientes_ids},
    ).mappings().all()

    clientes_por_id = {
        cliente["id"]: cliente
        for cliente in resultados
    }

    if len(clientes_por_id) != len(set(clientes_ids)):
        raise HTTPException(
            status_code=404,
            detail="Uno o más clientes no existen",
        )

    return [
        clientes_por_id[cliente_id]
        for cliente_id in clientes_ids
    ]

## ------------ AQUI ES DONDE SE BUSCA LA RUTA MAS OPTIMA ENTRE PUNTOS ----------------------------------------

def optimizar_ruta_osrm(clientes):
    coordenadas = ";".join(
        [
            "-108.99837,25.774814"
        ]
        + [
            f"{cliente['longitud']},{cliente['latitud']}"
            for cliente in clientes
        ]
    )

    url = (
        "https://router.project-osrm.org/trip/v1/driving/"
        f"{coordenadas}"
    )

    parametros = {
        "overview": "full",
        "geometries": "geojson",
        "source": "first",
        "roundtrip": "true",
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=10,
    )

    respuesta.raise_for_status()

    datos = respuesta.json()

    if datos["code"] != "Ok":
        raise HTTPException(
            status_code=404,
            detail="No se pudo optimizar la ruta",
        )

    ruta = datos["trips"][0]

    orden_indices = sorted(
        range(len(datos["waypoints"])),
        key=lambda i: datos["waypoints"][i]["waypoint_index"]
    )

    orden = []

    for indice in orden_indices:
        if indice == 0:
            continue

        cliente = clientes[indice - 1]

        orden.append({
            "id": cliente["id"],
            "nombre": cliente["nombre"],
            "latitud": cliente["latitud"],
            "longitud": cliente["longitud"],
        })

    return {
        "distancia_metros": ruta["distance"],
        "duracion_segundos": ruta["duration"],
        "geometria": ruta["geometry"],
        "orden": orden,
    }