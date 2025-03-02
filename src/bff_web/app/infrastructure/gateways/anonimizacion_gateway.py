import httpx
import logging

BASE_URL = "http://127.0.0.1:5000/anonimizacion/estado-query"

def get_anonimizacion_state(id: str) -> dict:
    url = f"{BASE_URL}/{id}"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        # Captura errores HTTP, por ejemplo, 4xx o 5xx.
        logging.error(f"HTTP error al llamar a {url}: {exc.response.status_code} - {exc.response.text}")
    except httpx.RequestError as exc:
        # Captura errores de conexión, tiempo de espera, etc.
        logging.error(f"Error en la conexión al servicio de anonimizacion: {exc}")

    # En lugar de propagar el error al front, se devuelve un mensaje controlado
    return {
        "estado": "ERROR",
        "error": "No se pudo obtener el estado de anonimización. Intente más tarde."
    }
