# configuracion/config.py
import json

def cargar_configuracion(path="modulos/solicitudes/configuracion/config.json"):
    with open(path) as f:
        config = json.load(f)
    
    motor = config["db_engine"]
    db_config = config.get(motor, {})
    db_config["db_engine"] = motor  # para que lo puedas seguir accediendo si es necesario
    return db_config
