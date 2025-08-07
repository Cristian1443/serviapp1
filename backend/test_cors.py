#!/usr/bin/env python3
import requests
import json

def test_pqr_endpoint():
    """Prueba el endpoint de PQR desde un origen externo"""
    try:
        # Simular una request del frontend
        headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json',
            'Access-Control-Request-Method': 'GET'
        }
        
        # Test GET /pqr/
        print("🔍 Probando GET /pqr/...")
        response = requests.get('http://localhost:8000/pqr/', headers=headers)
        print(f"Status: {response.status_code}")
        print(f"CORS headers: {dict((k, v) for k, v in response.headers.items() if 'access-control' in k.lower())}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Datos recibidos: {len(data)} PQRs")
            if data:
                print(f"Primer PQR: {data[0]}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
        # Test POST /pqr/
        print("\n🔍 Probando POST /pqr/...")
        test_data = {
            "id_solicitud": 999,
            "id_usuario": 1,
            "id_profesional": 1,
            "tipo": "peticion",
            "descripcion": "Test desde script",
            "estado": "pendiente"
        }
        
        post_response = requests.post(
            'http://localhost:8000/pqr/', 
            json=test_data,
            headers=headers
        )
        print(f"POST Status: {post_response.status_code}")
        print(f"POST Response: {post_response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor en http://localhost:8000")
        print("Asegúrate de que el backend esté corriendo con: python main.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_pqr_endpoint()

