from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import json

app = FastAPI()

ARCHIVO = "videojuegos.json"


class Videojuego(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    genero: str = Field(min_length=1, max_length=50)
    plataforma: str = Field(min_length=1, max_length=50)
    anio: int = Field(ge=1950, le=2030)


def leer():
    with open(ARCHIVO, encoding="utf-8") as f:
        return json.load(f)


def guardar(videojuegos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(videojuegos, f, indent=2, ensure_ascii=False)


def normalizar(texto: str) -> str:
    return texto.strip().casefold()


@app.get("/")
def inicio():
    return {"mensaje": "Hola, API de videojuegos"}


@app.get("/videojuegos")
def listar(genero: str | None = None, plataforma: str | None = None):
    videojuegos = leer()
    if genero is not None:
        videojuegos = [
            v for v in videojuegos if normalizar(v["genero"]) == normalizar(genero)
        ]
    if plataforma is not None:
        videojuegos = [
            v for v in videojuegos if normalizar(v["plataforma"]) == normalizar(plataforma)
        ]
    return videojuegos


@app.get("/videojuegos/{id}")
def buscar(id: int):
    for videojuego in leer():
        if videojuego["id"] == id:
            return videojuego
    raise HTTPException(status_code=404, detail="Ese videojuego no existe")


@app.post("/videojuegos", status_code=201)
def agregar(videojuego: Videojuego):
    videojuegos = leer()
    if any(normalizar(v["titulo"]) == normalizar(videojuego.titulo) for v in videojuegos):
        raise HTTPException(status_code=409, detail="Ese videojuego ya existe")

    id_mas_alto = 0
    for v in videojuegos:
        if v["id"] > id_mas_alto:
            id_mas_alto = v["id"]

    nuevo = {
        "id": id_mas_alto + 1,
        "titulo": videojuego.titulo,
        "genero": videojuego.genero,
        "plataforma": videojuego.plataforma,
        "anio": videojuego.anio,
    }
    videojuegos.append(nuevo)
    guardar(videojuegos)
    return nuevo


@app.put("/videojuegos/{id}")
def editar(id: int, datos: Videojuego):
    videojuegos = leer()
    for videojuego in videojuegos:
        if videojuego["id"] == id:
            if any(
                v["id"] != id and normalizar(v["titulo"]) == normalizar(datos.titulo)
                for v in videojuegos
            ):
                raise HTTPException(status_code=409, detail="Ese videojuego ya existe")
            videojuego["titulo"] = datos.titulo
            videojuego["genero"] = datos.genero
            videojuego["plataforma"] = datos.plataforma
            videojuego["anio"] = datos.anio
            guardar(videojuegos)
            return videojuego
    raise HTTPException(status_code=404, detail="Ese videojuego no existe")


@app.delete("/videojuegos/{id}")
def borrar(id: int):
    videojuegos = leer()
    for videojuego in videojuegos:
        if videojuego["id"] == id:
            videojuegos.remove(videojuego)
            guardar(videojuegos)
            return {"mensaje": "Videojuego borrado"}
    raise HTTPException(status_code=404, detail="Ese videojuego no existe")
