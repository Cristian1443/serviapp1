# configuracion/config.py

import json

def cargar_configuracion(path="modulos/pqr/configuracion/config.json"):
    with open(path) as f:
        return json.load(f)
