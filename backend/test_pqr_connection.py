#!/usr/bin/env python3
"""
Script para probar la conexión de PQR independientemente
"""

print("🔍 Probando conexión PQR...")

try:
    from modulos.pqr.acceso_datos.conexion import ConexionDB
    print("✅ Importación de ConexionDB exitosa")
    
    # Probar crear instancia
    conn = ConexionDB()
    print(f"✅ Instancia creada - Motor: {getattr(conn, 'motor', 'N/A')}")
    
    if conn.conexion is not None:
        print("✅ Conexión establecida")
    else:
        print("⚠️ Conexión es None (esperado si no hay BD)")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("🔄 Prueba de factory...")
try:
    from modulos.pqr.acceso_datos.postgres_factory import PostgresFactory
    print("✅ Importación de PostgresFactory exitosa")
    
    factory = PostgresFactory()
    print("✅ Factory creado")
    
except Exception as e:
    print(f"❌ Error con factory: {e}")
    import traceback
    traceback.print_exc()

print("🔄 Prueba completa de PQR...")
try:
    from modulos.pqr import PQRService
    print("✅ Importación de PQRService exitosa")
    
except Exception as e:
    print(f"❌ Error con PQRService: {e}")
    import traceback
    traceback.print_exc()

print("✅ Prueba completa")
