#!/usr/bin/env python3
import requests

try:
    # Obtener lista de evidencias
    response = requests.get('http://localhost:8000/evidencias/')
    if response.status_code == 200:
        evidencias = response.json()
        print(f'Evidencias disponibles: {len(evidencias)}')
        
        if len(evidencias) > 0:
            # Mostrar los primeros 3 IDs
            for i, ev in enumerate(evidencias[:3]):
                id_ev = ev.get('id_evidencia')
                print(f'  - ID: {id_ev}')
            
            # Probar con el primer ID
            primer_id = evidencias[0].get('id_evidencia')
            print(f'\nProbando archivo con ID {primer_id}...')
            
            response2 = requests.get(f'http://localhost:8000/evidencias/{primer_id}/archivo')
            print(f'Status: {response2.status_code}')
            
            if response2.status_code == 200:
                content_type = response2.headers.get('Content-Type', 'N/A')
                print(f'Content-Type: {content_type}')
                print(f'Content-Length: {len(response2.content)} bytes')
                print('✅ Archivo obtenido correctamente')
            else:
                print(f'❌ Error: {response2.text}')
        else:
            print('No hay evidencias en la base de datos')
    else:
        print(f'Error obteniendo evidencias: {response.text}')
        
except Exception as e:
    print(f'Error: {e}')

