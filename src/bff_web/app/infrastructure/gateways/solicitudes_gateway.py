import httpx
import logging

BASE_URL = "http://127.0.0.1:7000/anonimizacion/solicitudes"

def get_all_solicitudes(username: str) -> dict:
    url = f"{BASE_URL}/{username}"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error al llamar a {url}: {exc.response.status_code} - {exc.response.text}")
    except httpx.RequestError as exc:
        logging.error(f"Error en la conexión al servicio de solicitudes de anonimizacion: {exc}")
    return {
        "estado": "ERROR",
        "error": "No se pudo obtener el estado de la solicitud de anonimización. Intente más tarde."
    }
