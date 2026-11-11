"""Ejercicios integrados de las clases 4, 5 y 6 de FastAPI.
Ejecutar: uvicorn main:app --reload
Documentación: http://127.0.0.1:8000/docs
"""
from fastapi import Body, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Backend TICs: clases 4, 5 y 6")

# CLASE 4: primeras rutas y parámetros de ruta
@app.get("/")
def inicio():
    return {"Hola": "Mundo"}

@app.get("/items/{item}")
def consultar_item(item: str):
    return {"item_id": item}

# CLASE 5: parámetros de ruta, de consulta y del cuerpo
@app.get("/alumnos/{id}")
def consultar_alumno(id: str):
    return {"id": id}

@app.get("/alumnos2/{id}")
def consultar_alumno_bienvenida(id: str, bienvenida: bool):
    # bienvenida es obligatoria porque no tiene valor por defecto.
    return {"id": id, "bienvenida": bienvenida}

@app.get("/alumnos3/{id}")
def consultar_alumno_materias(
    id: str, bienvenida: bool, materias: list = Body(embed=True)
):
    # Ejemplo heredado del curso: GET con body no es recomendable en REST.
    return {"id": id, "bienvenida": bienvenida, "materias": materias}

@app.post("/persona/{id}")
def procesar_persona(
    id: int,
    numeros: list[int] = Body(embed=True),
    numBuscar: int = Body(embed=True),
    nombre: str = Query(),
):
    lista_ordenada = sorted(numeros)
    ocurrencias = sum(1 for numero in numeros if numero == numBuscar)
    nombre_pila = nombre.strip().split()[0] if nombre.strip() else ""
    return {
        "id": id,
        "Num_Buscar": numBuscar,
        "Lista_Numeros_original": numeros,
        "Nombre": nombre_pila,
        "Ocurrencias": ocurrencias,
        "ListaOrdenada": lista_ordenada,
    }

# CLASE 6: respuestas, errores, modelos y validación
# Diccionario en memoria: al reiniciar Uvicorn se restablece.
libros: dict[int, str | None] = {0: "La tabla de Flandez"}


def siguiente_id() -> int:
    # Se evita reutilizar IDs al calcular max + 1 (en vez de len()).
    return max(libros, default=-1) + 1


@app.get("/libro")
def obtener_libro_ejemplo():
    return {"titulo": "La casa de las sombras"}


@app.get("/libro1A", include_in_schema=False)
def simular_error_servidor():
    # Solo para demostrar el error 500. No se ejecuta en las pruebas normales.
    raise RuntimeError("Falla intencional en el servidor para fines didácticos")


@app.get("/libro/{id}")
def consultar_libro(id: int):
    if id not in libros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"id": id, "descripcion": "Libro no encontrado en esta base de datos"},
        )
    return {"titulo": libros[id]}


@app.post("/libro")
def agregar_libro_por_query(titulo: str):
    nuevo_id = siguiente_id()
    libros[nuevo_id] = titulo
    return {"id": nuevo_id, "titulo": titulo}


class RespuestaPostLibro(BaseModel):
    id: int
    titulo: str


@app.post("/libro2", response_model=RespuestaPostLibro, status_code=status.HTTP_201_CREATED)
def agregar_libro_con_respuesta(titulo: str):
    nuevo_id = siguiente_id()
    libros[nuevo_id] = titulo
    return {"id": nuevo_id, "titulo": titulo}


class RespuestaPostLibroOpcional(BaseModel):
    id: int = Field(ge=0)
    titulo: str | None = None


class Libro(BaseModel):
    titulo: str | None  # Acepta None, pero debe estar presente en el body.
    num_paginas: int  # Es obligatorio y debe ser entero.


@app.post(
    "/libro-2",
    response_model=RespuestaPostLibroOpcional,
    status_code=status.HTTP_201_CREATED,
)
def agregar_libro_por_body(libro: Libro):
    nuevo_id = siguiente_id()
    libros[nuevo_id] = libro.titulo
    # No se devuelve titulo: el response_model lo completa con null.
    # Para omitir ese null: añadir response_model_exclude_none=True al decorador.
    return {"id": nuevo_id}
