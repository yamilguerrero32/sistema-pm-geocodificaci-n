import requests
from fastapi import HTTPException
from app.config import GEOCODIFY_API_KEY

## ----- COORDEJADAS DE EL AREA DE MOCHIS ESTÁ LIMITADA PARA QUE LA BUSQUEDA NO SALGA DE AQUI -----

LATITUD_MIN = 25.70
LATITUD_MAX = 25.88

LONGITUD_MIN = -109.10
LONGITUD_MAX = -108.90

## --------------- AQUI ESTA EL GEOCODIFICADOR -------------------------

def geocodificar_direccion(direccion: str):
    url = "https://api.geocodify.com/v2/geocode"

    parametros = {
        "api_key": GEOCODIFY_API_KEY,
        "q": direccion,
    }

    try:
        respuesta = requests.get(
            url,
            params=parametros,
            timeout=10,
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con el servicio de geocodificación",
        )

    if respuesta.status_code == 401:
        raise HTTPException(
            status_code=500,
            detail="La API key de Geocodify no es válida",
        )

    if respuesta.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="Se alcanzó el límite de solicitudes de Geocodify",
        )

    if respuesta.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="El servicio de geocodificación no está disponible",
        )

    datos = respuesta.json()

    resultados = datos.get("response", {}).get("features", [])

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="No se pudo encontrar la dirección",
        )

    coordenadas = resultados[0]["geometry"]["coordinates"]

    longitud = float(coordenadas[0])
    latitud = float(coordenadas[1])

    if not (
        LATITUD_MIN <= latitud <= LATITUD_MAX
        and LONGITUD_MIN <= longitud <= LONGITUD_MAX
    ):
        return None

    return {
        "longitud": longitud,
        "latitud": latitud,
    }