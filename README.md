# 📚 Mantenedor de Carreras UDLA - Reemplazo Total

Un sistema simple y efectivo para **reemplazar completamente** las carreras de pregrado o postgrado de la Universidad de Las Américas.

## 🎯 ¿Qué hace este sistema?

Este mantenedor permite:
- ✅ **Reemplazar COMPLETAMENTE** la sección de pregrado o postgrado desde archivos CSV
- ✅ **Usar TODAS las carreras del CSV** como fuente única de verdad
- ✅ **Mantener la estructura JSON** original intacta
- ✅ **Generar archivos actualizados** con fecha automática
- ✅ **Detectar automáticamente** el tipo de CSV (pregrado/postgrado)
- ✅ **Validar datos** y mostrar errores claros

## 🔄 ¿Qué significa "Reemplazo Total"?

**Reemplazo Total** significa que:
- 🗑️ **Se elimina TODA la sección** existente (pregrado o postgrado)
- 🏗️ **Se reconstruye desde cero** usando únicamente los datos del CSV
- 📊 **TODAS las carreras del CSV** se incluyen en el resultado final
- 🧹 **Se limpia cualquier dato** antiguo o inconsistente

**¿Cuándo usar este sistema?**
- ✅ Tienes el listado **completo y actualizado** de todas las carreras
- ✅ Quieres **sincronizar completamente** con una fuente externa
- ✅ Necesitas **limpiar datos antiguos** o inconsistencias
- ✅ Realizas **actualizaciones masivas** periódicas

## 📁 Estructura de archivos requerida

### Archivo JSON base
Debe tener la estructura estándar de carreras UDLA:
```json
{
    "Pregrado": {
        "id": "0",
        "regimes": [...]
    },
    "Postgrado": {
        "id": "1", 
        "regimes": [...]
    }
}
```

### Archivos CSV
**¡IMPORTANTE!** El CSV debe contener **TODAS** las carreras de la sección que quieres actualizar.

Estructura requerida:
```csv
Codigo Banner,Carrera,Código Carrera,Sede,Campus,Código Campus,Régimen,Código Régimen
USC1318,Administración Pública,318,Santiago,Santiago Centro,SC,DIURNO,1
USC1319,Ingeniería Comercial,319,Santiago,Santiago Centro,SC,DIURNO,1
```

**Campos obligatorios:**
- `Codigo Banner`: ID único de la carrera
- `Carrera`: Nombre completo de la carrera
- `Código Carrera`: Código numérico de la carrera
- `Sede`: Ubicación (Santiago, Concepción, Viña del Mar, Online)
- `Campus`: Nombre del campus específico
- `Código Campus`: Código del campus (SC, PR, CO, VL, etc.)
- `Régimen`: Modalidad de estudio
- `Código Régimen`: ID numérico del régimen

## 🚀 Formas de usar el sistema

### Opción 1: Actualizador Interactivo (Recomendado)
La forma más fácil e intuitiva:

```bash
python actualizador.py
```

Este script:
- 🔍 **Busca automáticamente** archivos JSON y CSV
- 📋 **Muestra un menú** con opciones disponibles
- ⚠️ **Solicita confirmación** antes del reemplazo
- 📊 **Muestra el progreso** en tiempo real

### Opción 2: Línea de comandos
Para uso directo desde terminal:

```bash
python mantenedor.py <archivo_json> <archivo_csv>
```

**Ejemplos:**
```bash
python mantenedor.py careers-udla.json pregrado_completo.csv
python mantenedor.py careers-udla.json postgrado_completo.csv
```

## 📝 Convenciones de nombres

### Para CSV:
- **Pregrado**: Debe contener "pregrado" en el nombre
  - ✅ `pregrado.csv`
  - ✅ `carreras_pregrado.csv`
  - ✅ `Pregrado_2024.csv`

- **Postgrado**: Debe contener "postgrado" en el nombre
  - ✅ `postgrado.csv`
  - ✅ `carreras_postgrado.csv`
  - ✅ `Postgrado_2024.csv`

### Para JSON:
- Debe contener "careers" en el nombre
  - ✅ `careers-udla.json`
  - ✅ `careers_base.json`

## 📅 Archivos de salida

Los archivos actualizados se generan automáticamente con el formato:
```
<nombre_original>-<DD-MM-YY>.json
```

**Ejemplo:**
- Archivo base: `careers-udla.json`
- Archivo generado: `careers-udla-16-10-25.json`

## ⚡ Proceso de actualización

1. **Lectura** del archivo JSON base
2. **Análisis** del CSV para detectar estructura
3. **Detección automática** de regímenes, sedes y campus
4. **Construcción completa** de la nueva sección
5. **Reemplazo total** de la sección correspondiente
6. **Generación** del archivo actualizado

## 📊 Ejemplo de ejecución

```
🚀 Mantenedor de Carreras UDLA - Reemplazo Total
==================================================

📁 Archivos disponibles:

�️  Archivos JSON:
   1. careers-udla.json

📊 Archivos CSV:
   1. pregrado_completo.csv (pregrado)

�📋 Seleccione un archivo JSON:
Ingrese el número (1-1): 1

📋 Seleccione un archivo CSV:
Ingrese el número (1-1): 1

⚠️  CONFIRMACIÓN DE REEMPLAZO TOTAL:
   📄 JSON: careers-udla.json
   📊 CSV:  pregrado_completo.csv
   🎯 Sección a reemplazar: PREGRADO

   ⚠️  Se reemplazará COMPLETAMENTE la sección pregrado
   📊 Se usarán TODAS las carreras del CSV como fuente única

¿Continuar con el reemplazo total? (s/n): s

🚀 Ejecutando reemplazo total...
⏳ Por favor espere...

✅ CSV leído exitosamente: 245 carreras encontradas
✅ JSON base leído exitosamente
🔄 Reemplazando sección pregrado completamente...
✅ Sección pregrado reemplazada completamente
   📊 Total de carreras: 245
   📋 Regímenes: 3
   🏢 Sedes: 4
   🏫 Campus: 8
💾 Archivo guardado exitosamente: careers-udla-16-10-25.json
🎉 ¡Reemplazo completado exitosamente!

✅ Reemplazo total completado exitosamente
```

## 🛡️ Validaciones incluidas

- ✅ **Estructura del CSV**: Verifica que tenga todas las columnas requeridas
- ✅ **Archivos existentes**: Confirma que los archivos existen antes de procesar
- ✅ **Confirmación del usuario**: Solicita confirmación antes del reemplazo
- ✅ **Detección automática**: Identifica automáticamente pregrado vs postgrado
- ✅ **Estructura JSON**: Mantiene la estructura original intacta

## 🔧 Características técnicas

- **Lenguaje**: Python 3.6+
- **Dependencias**: Solo librerías estándar (json, csv, os, sys, datetime)
- **Encoding**: UTF-8 para soporte completo de caracteres especiales
- **Estructura**: Preserva exactamente la jerarquía JSON original
- **Rendimiento**: Optimizado para procesar miles de carreras

## 📞 Soporte

Para problemas o dudas sobre el sistema:
1. Verificar que los archivos CSV tengan todas las columnas requeridas
2. Confirmar que los nombres de archivos sigan las convenciones
3. Revisar que el JSON base tenga la estructura correcta

---

**¡Sistema listo para uso en producción!** 🚀

## 📝 Convenciones de nombres

### Para CSV:
- **Pregrado**: Debe contener "pregrado" en el nombre
  - ✅ `pregrado.csv`
  - ✅ `carreras_pregrado.csv`
  - ✅ `Pregrado_2024.csv`

- **Postgrado**: Debe contener "postgrado" en el nombre
  - ✅ `postgrado.csv`
  - ✅ `carreras_postgrado.csv`
  - ✅ `Postgrado_2024.csv`

### Para JSON:
- Debe contener "careers" en el nombre
  - ✅ `careers-udla.json`
  - ✅ `careers_base.json`

## 📅 Archivos de salida

Los archivos actualizados se generan automáticamente con el formato:
```
<nombre_original>-<DD-MM-YY>.json
```

**Ejemplos:**
- `careers-udla.json` → `careers-udla-16-10-25.json`
- `careers_base.json` → `careers_base-16-10-25.json`

## 🔧 Adaptabilidad a Cambios

### ✅ Cambios Automáticamente Soportados:

#### 🆕 **Nuevos Regímenes**
- Se detectan automáticamente desde el CSV
- Se asignan IDs basados en el código del CSV
- Se mantiene compatibilidad con regímenes existentes
- Ejemplo: Si aparece "HÍBRIDO" con código "10", se agrega automáticamente

#### 🏢 **Nuevas Sedes** 
- Se detectan automáticamente
- Se asignan IDs únicos incrementales (10+)
- Ejemplo: Si aparece "Valparaíso", se agrega con ID "10"

#### 🏫 **Nuevos Campus**
- Se detectan automáticamente desde el CSV
- Se usan los códigos de campus del CSV
- Ejemplo: Si aparece campus "Las Condes" con código "LC", se agrega

#### 📋 **Cambios en IDs de Regímenes**
- El sistema usa los códigos del CSV como fuente de verdad
- Si un régimen cambia de ID "1" a "9", se actualiza automáticamente
- Se mantiene la coherencia en toda la estructura

#### 🎓 **Carreras Agregadas/Eliminadas**
- **Agregadas**: Aparecen automáticamente en el nuevo JSON
- **Eliminadas**: Desaparecen automáticamente del nuevo JSON
- Se genera reporte de cambios para seguimiento


## 🛡️ Validaciones incluidas

- ✅ **Estructura del CSV**: Verifica que tenga todas las columnas requeridas
- ✅ **Archivos existentes**: Confirma que los archivos existen antes de procesar
- ✅ **Confirmación del usuario**: Solicita confirmación antes del reemplazo
- ✅ **Detección automática**: Identifica automáticamente pregrado vs postgrado
- ✅ **Estructura JSON**: Mantiene la estructura original intacta

## 🏫 Sedes y Campus soportados

### Santiago (ID: 0)
- Santiago Centro (SC)
- Providencia (PR)
- La Florida (LF)
- Maipú (MP)
- Melipilla (ME)

### Concepción (ID: 1)
- Concepción (CO)

### Viña del Mar (ID: 2)
- Viña del Mar (VL)

### Online (ID: 3)
- Online (OL)

**Nota**: El sistema detecta automáticamente nuevas sedes y campus desde el CSV y les asigna IDs únicos.

## ⚠️ Solución de problemas

### Error: "No se encontró el archivo"
- Verifique que los archivos estén en el directorio correcto
- Verifique los nombres de los archivos

### Error: "CSV tiene errores"
- Verifique que el CSV tenga todas las columnas requeridas
- Verifique que no haya filas vacías o con datos faltantes
- Verifique la codificación del archivo (debe ser UTF-8)

### Error: "JSON no es válido"
- Verifique que el archivo JSON esté bien formateado
- Asegúrese de que tenga la estructura de Pregrado/Postgrado

### El script no detecta el tipo de CSV
- Asegúrese de que el nombre del archivo contenga "pregrado" o "postgrado"
- Si no es posible, el script le preguntará el tipo

## 📊 Ejemplo de uso completo

1. **Preparar archivos:**
   ```
   mantenedor-carreras/
   ├── mantenedor.py
   ├── actualizador.py
   ├── README.md
   ├── careers-udla.json
   ├── pregrado_completo.csv
   └── postgrado_completo.csv
   ```

2. **Ejecutar actualizador:**
   ```bash
   python actualizador.py
   ```

3. **Seleccionar archivos** en el menú interactivo

4. **Confirmar reemplazo** cuando se solicite

5. **Verificar resultado** en el archivo generado con fecha

## 🔧 Características técnicas

- **Lenguaje**: Python 3.6+
- **Dependencias**: Solo librerías estándar (json, csv, os, sys, datetime)
- **Encoding**: UTF-8 para soporte completo de caracteres especiales
- **Estructura**: Preserva exactamente la jerarquía JSON original
- **Rendimiento**: Optimizado para procesar miles de carreras

## 📋 Archivos del sistema

Solo dos archivos principales:

1. **`mantenedor.py`** - Script principal de reemplazo total
2. **`actualizador.py`** - Interfaz interactiva

## 🎯 Casos de uso

### 1. Actualización semestral completa
```bash
python actualizador.py
# Seleccionar careers-udla.json y pregrado_2024_2.csv
```

### 2. Actualización rápida por línea de comandos
```bash
python mantenedor.py careers-udla.json postgrado_nuevos.csv
```

### 3. Migración a nueva estructura
```bash
python mantenedor.py careers-udla.json datos_con_nuevos_regimenes.csv
```

## 📞 Soporte

Para problemas o dudas sobre el sistema:
1. Verificar que los archivos CSV tengan todas las columnas requeridas
2. Confirmar que los nombres de archivos sigan las convenciones
3. Revisar que el JSON base tenga la estructura correcta

---

**¡Sistema listo para uso en producción!** 🚀
