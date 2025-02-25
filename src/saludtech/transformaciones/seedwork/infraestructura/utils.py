import time
import requests
import json
import os

from pulsar.schema import *
from fastavro.schema import parse_schema

basedir = os.path.abspath(os.path.dirname(__file__))

def time_millis():
    return int(time.time() * 1000)

def broker_host():
    
    pulsar_env = os.environ["PULSAR_ADDRESS"]
    if not pulsar_env:
        pulsar_env="localhost"
    
    return pulsar_env

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)



