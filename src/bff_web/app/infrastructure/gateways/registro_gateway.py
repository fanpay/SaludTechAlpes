import httpx
import logging

BASE_URL = "http://127.0.0.1:7000/anonimizacion/crear-solicitud"

def create_registro(data: dict) -> dict:
    try:
        response = httpx.post(BASE_URL, json=data)
        response.raise_for_status()
        try:
            # Intentamos parsear la respuesta como JSON
            return response.json()
        except ValueError:
            # Si falla, devolvemos el contenido en texto envuelto en un diccionario
            return {"result": response.text}
    except httpx.HTTPStatusError as exc:
        logging.error(
            f"HTTP error al llamar a {BASE_URL}: {exc.response.status_code} - {exc.response.text}"
        )
    except httpx.RequestError as exc:
        logging.error(
            f"Error en la conexión al servicio de registro: {exc}"
        )
    except Exception as exc:
        logging.error(
            f"Error inesperado al llamar al servicio de registro: {exc}"
        )

    # En caso de error, devolvemos una respuesta controlada
    return {
        "result": None,
        "error": "No se pudo crear la solicitud de anonimizacion. Intente más tarde."
    }
