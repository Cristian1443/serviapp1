import os
import json
import requests

# === 1. Rutas de los config.json de cada módulo ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULOS = {
    "Evidencias": os.path.join(BASE_DIR, "..", "backend", "modulos", "evidencias", "configuracion", "config.json"),
    "PQR": os.path.join(BASE_DIR, "..", "backend", "modulos", "pqr", "configuracion", "config.json"),
    "Profesional": os.path.join(BASE_DIR, "..", "backend", "modulos", "profesional", "configuracion", "config.json"),
    "Solicitudes": os.path.join(BASE_DIR, "..", "backend", "modulos", "solicitudes", "configuracion", "config.json"),
    "Usuarios": os.path.join(BASE_DIR, "..", "backend", "modulos", "usuarios", "configuracion", "config.json")
}

def cargar_config(modulo):
    with open(MODULOS[modulo], encoding="utf-8") as f:
        return json.load(f)

# === 2. Menú Principal ===
def menu_principal():
    print("\n=== Menú Principal ===")
    for i, m in enumerate(MODULOS.keys(), start=1):
        print(f"{i}. {m}")
    print(f"{len(MODULOS)+1}. Salir")

# === 3. CRUD para cada módulo ===
def menu_crud(modulo, config):
    api = config["api_base"]
    endpoints = config["endpoints"]
    campos = list(config.get("campos", []))  # Puedes guardar los campos en cada config.json si quieres

    while True:
        print(f"\n--- Gestión de {modulo} ---")
        print("1. Crear nuevo")
        print("2. Listar todos")
        print("3. Buscar por ID")
        print("4. Actualizar")
        print("5. Eliminar")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            data = {}
            for campo in campos:
                if campo.lower() != "id":
                    data[campo] = input(f"{campo.capitalize()}: ")
            r = requests.post(api + endpoints["create"], json=data)
            print(r.json())

        elif opcion == "2":
            r = requests.get(api + endpoints["read_all"])
            print("\n--- Resultados ---")
            for obj in r.json():
                print(obj)

        elif opcion == "3":
            id = input("ID a buscar: ")
            url = endpoints["read_one"].replace("{id}", id)
            r = requests.get(api + url)
            print(r.json() if r.status_code == 200 else "No encontrado.")

        elif opcion == "4":
            id = input("ID a actualizar: ")
            data = {}
            for campo in campos:
                if campo.lower() != "id":
                    data[campo] = input(f"Nuevo {campo}: ")
            url = endpoints["update"].replace("{id}", id)
            r = requests.put(api + url, json=data)
            print(r.json())

        elif opcion == "5":
            id = input("ID a eliminar: ")
            url = endpoints["delete"].replace("{id}", id)
            r = requests.delete(api + url)
            print(r.json())

        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

# === 4. Main ===
if __name__ == "__main__":
    while True:
        menu_principal()
        opcion = input("Seleccione un módulo: ")
        modulos_list = list(MODULOS.keys())

        if opcion.isdigit():
            i = int(opcion)
            if 1 <= i <= len(modulos_list):
                modulo = modulos_list[i - 1]
                config = cargar_config(modulo)
                menu_crud(modulo, config)
            elif i == len(modulos_list) + 1:
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
        else:
            print("Ingrese un número válido.")
