# Renombrador de Archivos Secuencial

Programa para Windows que permite renombrar archivos de forma secuencial con múltiples opciones de personalización.
[![Renombrador]([https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/.github/banner.svg)](https://github.com/fabiomb/renombrador/blob/main/docs/renombrador.png)]


## Características

- ✅ Seleccionar y visualizar archivos de un directorio
- ✅ Vista previa en tiempo real de los nuevos nombres
- ✅ Reordenar archivos manualmente (subir/bajar)
- ✅ Orden aleatorio con un checkbox
- ✅ Numeración secuencial personalizable (inicio y fin)
- ✅ Rellenado con ceros (001, 002, 003, etc.)
- ✅ Agregar prefijo y sufijo a los nombres
- ✅ Interfaz gráfica intuitiva con Tkinter

## Requisitos

- Python 3.8 o superior
- Tkinter (incluido con Python)
- PyInstaller (para crear el .exe)

## Instalación

### Opción 1: Ejecutar desde Python

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el programa:
```bash
python renombrador.py
```

### Opción 2: Crear ejecutable .exe

1. Ejecutar el script de compilación:
```bash
build.bat
```

2. El ejecutable se generará en la carpeta `dist\Renombrador.exe`

3. Puedes copiar el archivo .exe a cualquier ubicación y ejecutarlo sin necesidad de Python

## Uso del Programa

### 1. Seleccionar Directorio
- Haz clic en el botón **"Seleccionar"** para elegir la carpeta con los archivos
- Los archivos se mostrarán en la columna izquierda

### 2. Ordenar Archivos
- **Manualmente**: Selecciona archivos y usa los botones ↑ Subir / ↓ Bajar
- **Aleatorio**: Activa el checkbox "Orden aleatorio" para mezclar los archivos

### 3. Configurar Opciones de Renombrado

#### Prefijo y Sufijo
- **Prefijo**: Texto que se agregará al inicio del nombre (ej: "IMG_")
- **Sufijo**: Texto que se agregará antes de la extensión (ej: "_baja")

#### Numeración
- **Número desde**: Número inicial de la secuencia (ej: 1)
- **Hasta**: Número final indicativo (no se usa en el renombrado, solo referencia)
- **Rellenar con ceros**: Activa para usar 001, 002, etc.
- **Cantidad de dígitos**: Define cuántos dígitos tendrá el número (3 = 001, 4 = 0001)

### 4. Vista Previa
- La columna derecha muestra cómo quedarán los nombres
- Actualiza automáticamente al cambiar las opciones
- También puedes hacer clic en **"Actualizar Vista Previa"**

### 5. Aplicar Cambios
- Haz clic en **"APLICAR RENOMBRADO"** para renombrar los archivos
- Se te pedirá confirmación antes de aplicar los cambios
- ⚠️ Esta acción no se puede deshacer fácilmente

### 6. Recargar
- El botón **"RECARGAR TODO"** reinicia todas las opciones y recarga los archivos del directorio

## Ejemplos de Uso

### Ejemplo 1: Fotos de vacaciones
```
Archivos originales: DSC001.jpg, DSC002.jpg, DSC003.jpg
Prefijo: vacaciones_
Sufijo: (vacío)
Numeración: desde 1, con 3 ceros

Resultado: vacaciones_001.jpg, vacaciones_002.jpg, vacaciones_003.jpg
```

### Ejemplo 2: Capítulos de libro
```
Archivos originales: cap_final.pdf, cap_intro.pdf, cap_medio.pdf
Orden manual: cap_intro.pdf, cap_medio.pdf, cap_final.pdf
Prefijo: libro_capitulo_
Sufijo: _v1
Numeración: desde 1, con 2 ceros

Resultado: libro_capitulo_01_v1.pdf, libro_capitulo_02_v1.pdf, libro_capitulo_03_v1.pdf
```

### Ejemplo 3: Orden aleatorio
```
Archivos originales: imagen1.png, imagen2.png, imagen3.png, imagen4.png
Orden aleatorio: ✓ Activado
Prefijo: random_
Numeración: desde 100, sin ceros

Resultado: random_100.png, random_101.png, random_102.png, random_103.png
(en orden aleatorio)
```

## Notas Importantes

- ⚠️ El programa renombra archivos reales. Asegúrate de revisar la vista previa antes de aplicar
- ✅ El renombrado se hace en dos fases para evitar conflictos de nombres
- ✅ Se verifica que no haya nombres duplicados antes de renombrar
- ✅ Solo se muestran archivos (no carpetas) del directorio seleccionado
- ✅ Se respetan las extensiones originales de los archivos

## Estructura del Proyecto

```
Renombrador/
│
├── renombrador.py       # Código principal del programa
├── requirements.txt     # Dependencias de Python
├── build.bat           # Script para crear el .exe
└── README.md           # Este archivo
```

## Solución de Problemas

### El .exe no se genera
- Asegúrate de tener PyInstaller instalado: `pip install pyinstaller`
- Ejecuta `build.bat` desde la carpeta del proyecto

### Error al renombrar archivos
- Verifica que no haya nombres duplicados en la vista previa
- Asegúrate de tener permisos de escritura en el directorio
- Cierra cualquier programa que esté usando los archivos

### La ventana no se muestra correctamente
- Verifica que Tkinter esté instalado con Python
- En Windows, Tkinter viene incluido con Python

## Licencia

Proyecto de uso libre.

## Autor

Creado con Python + Tkinter para renombrado masivo de archivos.
