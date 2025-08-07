#!/usr/bin/env python3
import requests

print('🔍 Probando endpoint de archivo...')
try:
    # Probar obtener el archivo de la evidencia 5
    response = requests.get('http://localhost:8000/evidencias/5/archivo')
    print(f'Status: {response.status_code}')
    print(f'Content-Type: {response.headers.get("Content-Type", "N/A")}')
    print(f'Content-Length: {len(response.content)} bytes')
    
    if response.status_code == 200:
        print('✅ Endpoint de archivo funciona correctamente')
        
        # Verificar si es una imagen
        content_type = response.headers.get('Content-Type', '')
        if content_type.startswith('image/'):
            print(f'✅ Es una imagen: {content_type}')
        else:
            print(f'📎 Es otro tipo de archivo: {content_type}')
    else:
        print(f'❌ Error: {response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')

