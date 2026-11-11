"""Cliente de las clases 4, 5 y 6. Primero ejecutar el servidor main.py.
Puedes cambiar BASE_URL por la URL pública de Render (sin barra final).
"""
import requests

BASE_URL = "http://127.0.0.1:8000"


def mostrar(nombre: str, respuesta: requests.Response) -> None:
    """Muestra estado y contenido sin fallar si el servidor devuelve texto."""
    print(f"\n--- {nombre} ---")
    print("Estado HTTP:", respuesta.status_code)
    if "application/json" in respuesta.headers.get("content-type", ""):
        print("Respuesta:", respuesta.json())
    else:
        print("Respuesta (texto):", respuesta.text)


# CLASE 4

def probar_clase4():
    mostrar("GET /", requests.get(f"{BASE_URL}/", timeout=15))
    mostrar("GET /items/LOQUESEA", requests.get(f"{BASE_URL}/items/LOQUESEA", timeout=15))


# CLASE 5

def probar_clase5():
    mostrar("GET alumno", requests.get(f"{BASE_URL}/alumnos/1", timeout=15))
    mostrar(
        "GET alumno + query bienvenida",
        requests.get(f"{BASE_URL}/alumnos2/1", params={"bienvenida": False}, timeout=15),
    )
    # Ejemplo del curso con GET y body; se mantiene solo para comparación.
    mostrar(
        "GET alumno + query + body (solo demostración)",
        requests.get(
            f"{BASE_URL}/alumnos3/1",
            params={"bienvenida": False},
            json={"materias": [1, 2, 3, 4]},
            timeout=15,
        ),
    )
    mostrar(
        "POST persona (ruta + query + body)",
        requests.post(
            f"{BASE_URL}/persona/1",
            params={"nombre": "Janet Pech"},
            json={"numeros": [8, 5, 7, 3, 4, 5, 7, 90], "numBuscar": 5},
            timeout=15,
        ),
    )


# CLASE 6

def probar_clase6():
    mostrar("GET libro de ejemplo", requests.get(f"{BASE_URL}/libro", timeout=15))
    mostrar("GET libro existente", requests.get(f"{BASE_URL}/libro/0", timeout=15))

    respuesta = requests.get(f"{BASE_URL}/libro/999", timeout=15)
    mostrar("GET libro inexistente (404)", respuesta)
    if respuesta.status_code == 404:
        detalle = respuesta.json()["detail"]
        print(f"Mensaje del cliente: ID {detalle['id']} — {detalle['descripcion']}")

    mostrar(
        "POST libro con query",
        requests.post(f"{BASE_URL}/libro", params={"titulo": "El atentado"}, timeout=15),
    )
    mostrar(
        "POST libro2 con response_model",
        requests.post(f"{BASE_URL}/libro2", params={"titulo": "El atentado2"}, timeout=15),
    )
    mostrar(
        "POST libro-2 con JSON body",
        requests.post(
            f"{BASE_URL}/libro-2",
            json={"titulo": "Hola Amigos", "num_paginas": 10},
            timeout=15,
        ),
    )


def main():
    print("PRUEBAS DE FASTAPI: CLASES 4, 5 Y 6")
    try:
        probar_clase4()
        probar_clase5()
        probar_clase6()
    except requests.exceptions.RequestException as error:
        print("No se pudo completar la comunicación con el servidor:", error)
        print("Verifica que Uvicorn esté ejecutándose y que BASE_URL sea correcta.")


if __name__ == "__main__":
    main()
