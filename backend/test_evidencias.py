#!/usr/bin/env python3
"""
Script para probar la conexión con el endpoint de evidencias
"""

import requests
import json

def test_evidencias():
    base_url = "http://localhost:8000"
    
    print("🔍 Probando GET /evidencias/...")
    try:
        response = requests.get(f"{base_url}/evidencias/")
        print(f"Status: {response.status_code}")
        
        # Verificar headers CORS
        cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
        print(f"CORS headers: {cors_headers}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Datos recibidos: {len(data)} evidencias")
                if len(data) > 0:
                    print(f"Primera evidencia: {str(data[0])[:100]}...")
            else:
                print(f"✅ Respuesta: {data}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor en http://localhost:8000")
        print("Asegúrate de que el backend esté corriendo con: python main.py")
        return
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return
    
    print("\n🔍 Probando POST /evidencias/...")
    try:
        # Datos de prueba para crear evidencia
        evidencia_data = {
            "id_solicitud": 13,
            "id_usuario": 1,
            "id_profesional": 1,
            "tipo_actor": "usuario",
            "descripcion": "Evidencia de prueba desde script",
            "estado": "satisfactorio",
            "archivo_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        }
        
        response = requests.post(
            f"{base_url}/evidencias/",
            json=evidencia_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"POST Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ POST Response: {response.json()}")
        else:
            print(f"❌ POST Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en POST: {e}")

if __name__ == "__main__":
    test_evidencias()
