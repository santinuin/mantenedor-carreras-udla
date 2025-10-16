#!/usr/bin/env python3
"""
Mantenedor de Carreras UDLA - Reemplazo Total
============================================

Este sistema reemplaza COMPLETAMENTE la sección de pregrado o postgrado
con todos los datos del CSV, manteniendo la estructura JSON original.

Características:
- ✅ Reemplazo total de la sección (pregrado o postgrado)
- ✅ Mantiene la estructura JSON exacta
- ✅ Se adapta automáticamente a cualquier cambio
- ✅ No necesita mapeos predefinidos
- ✅ Detección automática de todos los elementos
"""

import json
import csv
import sys
import os
from datetime import datetime
from collections import defaultdict

def detectar_tipo_csv(nombre_archivo):
    """Detecta si el CSV es de pregrado o postgrado."""
    nombre_lower = nombre_archivo.lower()
    if 'pregrado' in nombre_lower:
        return 'pregrado'
    elif 'postgrado' in nombre_lower:
        return 'postgrado'
    else:
        print(f"No se pudo detectar automáticamente el tipo de CSV desde '{nombre_archivo}'")
        while True:
            tipo = input("¿Es un CSV de 'pregrado' o 'postgrado'? ").lower().strip()
            if tipo in ['pregrado', 'postgrado']:
                return tipo
            print("Por favor, ingrese 'pregrado' o 'postgrado'")

def leer_csv_carreras(archivo_csv):
    """Lee el archivo CSV y retorna una lista de carreras."""
    carreras = []
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Limpiar datos
                carrera_limpia = {}
                for key, value in row.items():
                    carrera_limpia[key] = value.strip() if value else ''
                carreras.append(carrera_limpia)
        print(f"✅ CSV leído exitosamente: {len(carreras)} carreras encontradas")
        return carreras
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        sys.exit(1)

def leer_json_base(archivo_json):
    """Lee el archivo JSON base."""
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON base leído exitosamente")
        return data
    except Exception as e:
        print(f"❌ Error al leer el JSON: {e}")
        sys.exit(1)

def analizar_estructura_csv(carreras_csv):
    """Analiza la estructura completa del CSV para generar mapeos automáticos."""
    print("🔍 Analizando estructura del CSV...")
    
    # Extraer todos los elementos únicos
    regimenes = {}  # {nombre_regimen: codigo_regimen}
    sedes = {}      # {nombre_sede: codigo_sede}
    campus = {}     # {nombre_campus: codigo_campus}
    
    for carrera in carreras_csv:
        regimen = carrera['Régimen']
        codigo_regimen = carrera['Código Régimen']
        sede = carrera['Sede'] 
        campus_nombre = carrera['Campus']
        codigo_campus = carrera['Código Campus']
        
        regimenes[regimen] = codigo_regimen
        sedes[sede] = sedes.get(sede, len(sedes))  # Auto-asignar ID de sede
        campus[campus_nombre] = codigo_campus
    
    # Generar mapeo de sedes con IDs
    mapeo_sedes = {
        'Santiago': '0',
        'Concepción': '1', 
        'Viña del Mar': '2',
        'Online': '3',
        'OnLine': '3'
    }
    
    # Para sedes nuevas, asignar IDs automáticamente
    siguiente_id = 4
    for sede in sedes:
        if sede not in mapeo_sedes:
            mapeo_sedes[sede] = str(siguiente_id)
            siguiente_id += 1
    
    print(f"   📋 Regímenes detectados: {len(regimenes)}")
    for regimen, codigo in sorted(regimenes.items(), key=lambda x: int(x[1]) if x[1].isdigit() else 999):
        print(f"      - {regimen} (ID: {codigo})")
    
    print(f"   🏢 Sedes detectadas: {len(sedes)}")
    for sede in sorted(sedes.keys()):
        print(f"      - {sede} (ID: {mapeo_sedes[sede]})")
    
    print(f"   🏫 Campus detectados: {len(campus)}")
    for camp, codigo in sorted(campus.items()):
        print(f"      - {camp} ({codigo})")
    
    return regimenes, mapeo_sedes, campus

def construir_seccion_completa(carreras_csv, tipo_seccion):
    """Construye la sección completa (pregrado o postgrado) desde cero."""
    print(f"🏗️  Construyendo sección {tipo_seccion} desde cero...")
    
    # Analizar estructura
    regimenes, mapeo_sedes, campus = analizar_estructura_csv(carreras_csv)
    
    # Organizar carreras por estructura
    estructura = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for carrera in carreras_csv:
        regimen = carrera['Régimen']
        sede = carrera['Sede']
        campus_nombre = carrera['Campus']
        
        carrera_obj = {
            "id": carrera['Codigo Banner'],
            "name": carrera['Carrera']
        }
        
        estructura[regimen][sede][campus_nombre].append(carrera_obj)
    
    # Construir JSON
    seccion_id = "0" if tipo_seccion == 'pregrado' else "1"
    seccion_json = {
        "id": seccion_id,
        "regimes": []
    }
    
    # Ordenar regímenes por código
    regimenes_ordenados = sorted(regimenes.items(), key=lambda x: int(x[1]) if x[1].isdigit() else 999)
    
    for regimen_nombre, regimen_codigo in regimenes_ordenados:
        if regimen_nombre not in estructura:
            continue
        
        # Crear objeto de régimen
        regime_obj = {
            regimen_nombre: {
                "id": regimen_codigo,
                "locations": []
            }
        }
        
        # Procesar ubicaciones/sedes
        sedes_del_regimen = estructura[regimen_nombre]
        for sede_nombre in sorted(sedes_del_regimen.keys()):
            
            # Para postgrado online, usar "OnLine" como key
            location_key = sede_nombre
            if tipo_seccion == 'postgrado' and sede_nombre == 'Online':
                location_key = 'OnLine'
            
            location_obj = {
                location_key: {
                    "id": mapeo_sedes[sede_nombre],
                    "campus": []
                }
            }
            
            # Procesar campus de la sede
            campus_de_sede = sedes_del_regimen[sede_nombre]
            for campus_nombre in sorted(campus_de_sede.keys()):
                carreras_del_campus = campus_de_sede[campus_nombre]
                
                if carreras_del_campus:  # Solo si hay carreras
                    campus_obj = {
                        campus_nombre: {
                            "id": campus[campus_nombre],
                            "careers": sorted(carreras_del_campus, key=lambda x: x['name'])
                        }
                    }
                    location_obj[location_key]["campus"].append(campus_obj)
            
            # Solo agregar location si tiene campus
            if location_obj[location_key]["campus"]:
                regime_obj[regimen_nombre]["locations"].append(location_obj)
        
        # Solo agregar régimen si tiene locations
        if regime_obj[regimen_nombre]["locations"]:
            seccion_json["regimes"].append(regime_obj)
    
    return seccion_json

def reemplazar_seccion_completa(json_data, carreras_csv, tipo_seccion):
    """Reemplaza completamente la sección de pregrado o postgrado."""
    print(f"🔄 Reemplazando sección {tipo_seccion} completamente...")
    
    # Construir nueva sección
    nueva_seccion = construir_seccion_completa(carreras_csv, tipo_seccion)
    
    # Reemplazar en el JSON
    seccion_key = tipo_seccion.title()
    json_data[seccion_key] = nueva_seccion
    
    print(f"✅ Sección {tipo_seccion} reemplazada completamente")
    print(f"   📊 Total de carreras: {len(carreras_csv)}")
    
    # Contar regímenes y sedes
    num_regimenes = len(nueva_seccion["regimes"])
    num_sedes = len(set(carrera['Sede'] for carrera in carreras_csv))
    num_campus = len(set(carrera['Campus'] for carrera in carreras_csv))
    
    print(f"   📋 Regímenes: {num_regimenes}")
    print(f"   🏢 Sedes: {num_sedes}")
    print(f"   🏫 Campus: {num_campus}")
    
    return json_data

def generar_nombre_archivo(archivo_base):
    """Genera el nombre del archivo de salida con la fecha actual."""
    fecha_actual = datetime.now().strftime("%d-%m-%y")
    nombre_base = os.path.splitext(archivo_base)[0]
    return f"{nombre_base}-{fecha_actual}.json"

def validar_estructura_csv(carreras_csv):
    """Valida que el CSV tenga todas las columnas necesarias."""
    columnas_requeridas = [
        'Codigo Banner', 'Carrera', 'Código Carrera', 
        'Sede', 'Campus', 'Código Campus', 
        'Régimen', 'Código Régimen'
    ]
    
    if not carreras_csv:
        return False, "CSV vacío"
    
    primera_fila = carreras_csv[0]
    columnas_faltantes = []
    
    for col in columnas_requeridas:
        if col not in primera_fila:
            columnas_faltantes.append(col)
    
    if columnas_faltantes:
        return False, f"Columnas faltantes: {', '.join(columnas_faltantes)}"
    
    return True, "Estructura válida"

def main():
    if len(sys.argv) != 3:
        print("❌ Uso incorrecto")
        print(f"Uso: python {sys.argv[0]} <archivo_json> <archivo_csv>")
        print("\nEjemplos:")
        print(f"  python {sys.argv[0]} careers-udla.json pregrado_completo.csv")
        print(f"  python {sys.argv[0]} careers-udla.json postgrado_completo.csv")
        print("\nNota: El CSV debe contener TODAS las carreras de la sección a actualizar")
        sys.exit(1)
    
    archivo_json = sys.argv[1]
    archivo_csv = sys.argv[2]
    
    # Verificar archivos
    if not os.path.exists(archivo_json):
        print(f"❌ Error: No se encontró el archivo JSON '{archivo_json}'")
        sys.exit(1)
    
    if not os.path.exists(archivo_csv):
        print(f"❌ Error: No se encontró el archivo CSV '{archivo_csv}'")
        sys.exit(1)
    
    print("🚀 Mantenedor de Carreras UDLA - Reemplazo Total")
    print("="*55)
    
    # Detectar tipo
    tipo_csv = detectar_tipo_csv(archivo_csv)
    print(f"📋 Tipo de CSV detectado: {tipo_csv.upper()}")
    
    # Leer archivos
    carreras_csv = leer_csv_carreras(archivo_csv)
    json_data = leer_json_base(archivo_json)
    
    # Validar estructura del CSV
    es_valido, mensaje = validar_estructura_csv(carreras_csv)
    if not es_valido:
        print(f"❌ Error en estructura del CSV: {mensaje}")
        sys.exit(1)
    
    # Confirmar reemplazo total
    print(f"\n⚠️  CONFIRMACIÓN:")
    print(f"   Se reemplazará COMPLETAMENTE la sección {tipo_csv.upper()}")
    print(f"   con {len(carreras_csv)} carreras del CSV")
    print(f"   ¿Continuar? (s/n): ", end="")
    
    respuesta = input().lower().strip()
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada")
        sys.exit(0)
    
    # Reemplazar sección completa
    json_actualizado = reemplazar_seccion_completa(json_data.copy(), carreras_csv, tipo_csv)
    
    # Generar archivo de salida
    archivo_salida = generar_nombre_archivo(archivo_json)
    
    # Guardar
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(json_actualizado, f, ensure_ascii=False, indent=4)
        print(f"💾 Archivo guardado exitosamente: {archivo_salida}")
    except Exception as e:
        print(f"❌ Error al guardar: {e}")
        sys.exit(1)
    
    print("="*55)
    print("🎉 ¡Reemplazo completado exitosamente!")
    print(f"📄 Archivo generado: {archivo_salida}")
    print(f"🔄 Sección {tipo_csv} completamente actualizada")

if __name__ == "__main__":
    main()