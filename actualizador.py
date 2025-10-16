#!/usr/bin/env python3
"""
Actualizador de Carreras UDLA - Reemplazo Total
==============================================

Sistema interactivo para reemplazar completamente las secciones
de pregrado o postgrado con todos los datos del CSV.
"""

import os
import sys
import json
import importlib.util
from datetime import datetime

def buscar_archivos():
    """Busca archivos JSON y CSV en el directorio actual."""
    archivos_json = []
    archivos_csv = []
    
    for archivo in os.listdir('.'):
        if archivo.endswith('.json') and 'career' in archivo.lower():
            archivos_json.append(archivo)
        elif archivo.endswith('.csv'):
            archivos_csv.append(archivo)
    
    return sorted(archivos_json), sorted(archivos_csv)

def mostrar_archivos_disponibles():
    """Muestra los archivos disponibles en el directorio."""
    archivos_json, archivos_csv = buscar_archivos()
    
    print("📁 Archivos disponibles:")
    print("\n🗂️  Archivos JSON:")
    if archivos_json:
        for i, archivo in enumerate(archivos_json, 1):
            print(f"   {i}. {archivo}")
    else:
        print("   ❌ No se encontraron archivos JSON")
    
    print("\n📊 Archivos CSV:")
    if archivos_csv:
        for i, archivo in enumerate(archivos_csv, 1):
            tipo = "pregrado" if "pregrado" in archivo.lower() else \
                   "postgrado" if "postgrado" in archivo.lower() else "tipo no detectado"
            print(f"   {i}. {archivo} ({tipo})")
    else:
        print("   ❌ No se encontraron archivos CSV")
    
    return archivos_json, archivos_csv

def seleccionar_archivo(archivos, tipo):
    """Permite al usuario seleccionar un archivo de la lista."""
    if not archivos:
        print(f"❌ No hay archivos {tipo} disponibles")
        return None
    
    while True:
        try:
            print(f"\n📋 Seleccione un archivo {tipo}:")
            for i, archivo in enumerate(archivos, 1):
                print(f"   {i}. {archivo}")
            
            opcion = input(f"Ingrese el número (1-{len(archivos)}): ").strip()
            indice = int(opcion) - 1
            
            if 0 <= indice < len(archivos):
                return archivos[indice]
            else:
                print(f"❌ Número inválido. Debe ser entre 1 y {len(archivos)}")
        except ValueError:
            print("❌ Por favor, ingrese un número válido")

def confirmar_operacion(archivo_json, archivo_csv):
    """Solicita confirmación antes de ejecutar la operación."""
    print(f"\n⚠️  CONFIRMACIÓN DE REEMPLAZO TOTAL:")
    print(f"   📄 JSON: {archivo_json}")
    print(f"   📊 CSV:  {archivo_csv}")
    
    # Detectar tipo de CSV
    tipo_csv = "pregrado" if "pregrado" in archivo_csv.lower() else \
               "postgrado" if "postgrado" in archivo_csv.lower() else "no detectado"
    print(f"   🎯 Sección a reemplazar: {tipo_csv.upper()}")
    
    print(f"\n   ⚠️  Se reemplazará COMPLETAMENTE la sección {tipo_csv}")
    print(f"   📊 Se usarán TODAS las carreras del CSV como fuente única")
    
    print(f"\n¿Continuar con el reemplazo total? (s/n): ", end="")
    respuesta = input().lower().strip()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']

def ejecutar_reemplazo(archivo_json, archivo_csv):
    """Ejecuta el reemplazo total llamando directamente al mantenedor."""
    try:
        print("\n🚀 Ejecutando reemplazo total...")
        print("⏳ Por favor espere...")
        
        # Cargar el módulo mantenedor
        spec = importlib.util.spec_from_file_location("mantenedor", "mantenedor.py")
        mantenedor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mantenedor_module)
        
        # Detectar tipo de CSV
        nombre_lower = archivo_csv.lower()
        if 'pregrado' in nombre_lower:
            tipo_csv = 'pregrado'
        elif 'postgrado' in nombre_lower:
            tipo_csv = 'postgrado'
        else:
            print(f"⚠️  No se pudo detectar el tipo automáticamente desde '{archivo_csv}'")
            return False
        
        print(f"📋 Tipo detectado: {tipo_csv.upper()}")
        
        # Leer archivos
        carreras_csv = mantenedor_module.leer_csv_carreras(archivo_csv)
        json_data = mantenedor_module.leer_json_base(archivo_json)
        
        # Validar estructura del CSV
        es_valido, mensaje = mantenedor_module.validar_estructura_csv(carreras_csv)
        if not es_valido:
            print(f"❌ Error en estructura del CSV: {mensaje}")
            return False
        
        # Reemplazar sección completa
        json_actualizado = mantenedor_module.reemplazar_seccion_completa(
            json_data.copy(), carreras_csv, tipo_csv
        )
        
        # Generar archivo de salida
        archivo_salida = mantenedor_module.generar_nombre_archivo(archivo_json)
        
        # Guardar
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(json_actualizado, f, ensure_ascii=False, indent=4)
        
        print(f"💾 Archivo guardado exitosamente: {archivo_salida}")
        print("🎉 ¡Reemplazo completado exitosamente!")
        print(f"📄 Archivo generado: {archivo_salida}")
        print(f"🔄 Sección {tipo_csv} completamente actualizada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el reemplazo: {e}")
        print(f"   Detalle: {str(e)}")
        return False

def main():
    print("🚀 Mantenedor de Carreras UDLA - Reemplazo Total")
    print("="*50)
    print("Fecha:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print()
    print("💡 Este sistema reemplaza COMPLETAMENTE la sección")
    print("   de pregrado o postgrado con todas las carreras del CSV")
    
    while True:
        print("\n" + "="*50)
        
        # Mostrar archivos disponibles
        archivos_json, archivos_csv = mostrar_archivos_disponibles()
        
        if not archivos_json or not archivos_csv:
            print("\n❌ No se encontraron archivos JSON o CSV necesarios")
            print("   Asegúrese de tener ambos tipos de archivos en el directorio")
            break
        
        # Seleccionar archivos
        archivo_json = seleccionar_archivo(archivos_json, "JSON")
        if not archivo_json:
            continue
        
        archivo_csv = seleccionar_archivo(archivos_csv, "CSV")
        if not archivo_csv:
            continue
        
        # Confirmar operación
        if not confirmar_operacion(archivo_json, archivo_csv):
            print("❌ Operación cancelada")
            
            # Preguntar si desea intentar con otros archivos
            print(f"\n¿Desea seleccionar otros archivos? (s/n): ", end="")
            respuesta = input().lower().strip()
            if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                print("👋 ¡Hasta luego!")
                break
            continue
        
        # Ejecutar reemplazo
        exito = ejecutar_reemplazo(archivo_json, archivo_csv)
        
        if exito:
            print("\n✅ Operación completada exitosamente")
        else:
            print("\n❌ La operación falló")
        
        # Preguntar si desea continuar
        print(f"\n¿Desea realizar otro reemplazo? (s/n): ", end="")
        respuesta = input().lower().strip()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("👋 ¡Hasta luego!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Operación interrumpida por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("   Por favor, intente nuevamente")