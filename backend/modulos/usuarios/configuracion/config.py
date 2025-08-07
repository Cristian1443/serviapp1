
import json

def cargar_configuracion(path="modulos/usuarios/configuracion/config.json"):
    with open(path) as f:
        return json.load(f)
