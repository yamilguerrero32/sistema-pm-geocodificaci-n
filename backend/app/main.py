from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.clientes import router as clientes_router
from app.routes.repartos import router as repartos_router
from app.routes.rutas import router as rutas_router


app = FastAPI(
    title="Sistema de Repartos",
    description="API para gestión de clientes, repartos y rutas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(clientes_router)
app.include_router(repartos_router)
app.include_router(rutas_router)