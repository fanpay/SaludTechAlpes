import httpx

BASE_URL = "http://127.0.0.1:5000/anonimizacion/estado-query"

def get_anonimizacion_state(id: str) -> dict:
    url = f"{BASE_URL}/{id}"
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()
