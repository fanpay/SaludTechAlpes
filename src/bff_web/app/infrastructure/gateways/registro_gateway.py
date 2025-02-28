import httpx

BASE_URL = "http://127.0.0.1:5001/crear/registar-nueva"

def create_registro(data: dict) -> dict:
    response = httpx.post(BASE_URL, json=data)
    response.raise_for_status()
    return response.json()
