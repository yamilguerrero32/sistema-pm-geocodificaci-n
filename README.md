# Sistema de Repartos

Sistema web para la gestión y optimización de entregas.

## Descripción

Este proyecto permite administrar clientes, visualizar sus ubicaciones
en un mapa y generar rutas optimizadas para realizar entregas.

El sistema está desarrollado utilizando una arquitectura basada en:

- Backend con Python y FastAPI
- Base de datos PostgreSQL
- Extensión espacial PostGIS
- Geocodificación mediante Geocodify
- Optimización de rutas mediante OSRM
- Frontend con HTML, CSS y JavaScript
- Mapas interactivos con Leaflet

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal del backend |
| FastAPI | Desarrollo de la API |
| PostgreSQL | Base de datos |
| PostGIS | Manejo de coordenadas y geometrías |
| SQLAlchemy | Comunicación con PostgreSQL |
| GeoAlchemy2 | Integración de datos espaciales |
| Alembic | Migraciones de la base de datos |
| Geocodify | Conversión de direcciones a coordenadas |
| OSRM | Optimización de rutas |
| Leaflet | Visualización del mapa |
| HTML / CSS / JavaScript | Desarrollo del frontend |

## Estructura del proyecto

```text
sistema-repartos-pm/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
│
├── .gitignore
└── README.md

Estado del proyecto
Actualmente el sistema cuenta con:
- Gestión de clientes
- Geocodificación de direcciones
- Validación de ubicaciones dentro del área de Los Mochis
- Visualización de clientes en el mapa
- Organización de clientes por zonas
- Creación y gestión de repartos
- Optimización de rutas mediante OSRM
- Estados de entrega
- API REST con FastAPI
Instalación
Requisitos
Antes de ejecutar el proyecto es necesario instalar:
- Python
- PostgreSQL
- PostGIS
- Git
Clonar el repositorio
git clone https://github.com/yamilguerrero32/sistema-pm-geocodificaci-n.git
cd sistema-repartos-pm

Configurar el backend
Entrar a la carpeta:
cd backend

Crear el entorno virtual:
python -m venv venv

Activar el entorno virtual en Windows:
.\venv\Scripts\Activate.ps1

Instalar las dependencias:
pip install -r requirements.txt

Variables de entorno
Crear un archivo .env dentro de backend/ con las variables necesarias
para la conexión a PostgreSQL y los servicios externos.
El archivo .env no debe subirse al repositorio.

Ejecutar el backend
Desde la carpeta backend/:
uvicorn app.main:app --reload

La API estará disponible en:
http://127.0.0.1:8000

La documentación interactiva de FastAPI estará disponible en:
http://127.0.0.1:8000/docs

Ejecutar el frontend
El frontend puede ejecutarse utilizando un servidor local como
Live Server desde Visual Studio Code.
Base de datos
El proyecto utiliza PostgreSQL junto con PostGIS para almacenar y
consultar información geográfica.
Las migraciones de la estructura de la base de datos se administran
mediante Alembic.
Control de versiones
El proyecto utiliza Git para controlar las versiones del código.
Para guardar nuevos cambios:
git add .
git commit -m "Descripción del cambio"
git push

Autor
Proyecto desarrollado como parte del aprendizaje y desarrollo de
software.

### Después

**No hagas todavía el commit.**

Primero guarda el archivo y dime **“listo”**.

Después revisamos el README juntos y corregimos lo que sea necesario antes de subir esta versión a GitHub.