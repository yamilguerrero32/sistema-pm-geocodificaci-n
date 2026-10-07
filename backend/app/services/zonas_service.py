from sqlalchemy import text
from sqlalchemy.orm import Session

## ------------------ COORDENADAS DE LAS ZONAS -------------------------
ZONAS = {
    1: [
        (-109.000443, 25.772966),
        (-109.004332, 25.784847),
        (-109.038347, 25.804657),
        (-109.029797, 25.817018),
        (-108.981336, 25.843785),
        (-108.965471, 25.823056),
    ],

    2: [
        (-109.000435, 25.772881),
        (-108.969774, 25.755070),
        (-108.943780, 25.801059),
        (-108.965383, 25.823194),
    ],

    3: [
        (-109.000499, 25.772758),
        (-108.972464, 25.756481),
        (-108.993855, 25.725929),
        (-109.021596, 25.741840),
    ],

    4: [
        (-109.000496, 25.772888),
        (-109.005280, 25.785685),
        (-109.038371, 25.804689),
        (-109.048584, 25.788768),
        (-109.041201, 25.747936),
        (-109.023391, 25.740165),
    ],
}

## ------------------ OBTENER LAS ZONAS SEGÚN LOS CLIENTES -------------------------------

def obtener_zona_cliente(
    db: Session,
    cliente_id: int,
):
    puntos_zonas = []

    for zona_id, puntos in ZONAS.items():
        puntos_sql = ", ".join(
            f"{longitud} {latitud}"
            for longitud, latitud in puntos
        )

        puntos_zonas.append(
            f"""
            SELECT
                {zona_id} AS zona,
                ST_GeomFromText(
                    'POLYGON(({puntos_sql}, {puntos[0][0]} {puntos[0][1]}))',
                    4326
                ) AS poligono
            """
        )

    consulta = text(f"""
        WITH zonas AS (
            {" UNION ALL ".join(puntos_zonas)}
        )
        SELECT
            z.zona
        FROM clientes c
        INNER JOIN zonas z
            ON ST_Covers(
                z.poligono,
                c.ubicacion
            )
        WHERE c.id = :cliente_id
        LIMIT 1
    """)

    resultado = db.execute(
        consulta,
        {"cliente_id": cliente_id},
    ).scalar()

    return resultado