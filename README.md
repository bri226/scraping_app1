# Scraping de SUSALUD para Obtención de Información de Seguros de Salud

Este script realiza web scraping en la plataforma de SUSALUD para obtener información sobre los seguros de salud de las personas en Perú. Se utiliza OCR para resolver el captcha y extraer los datos de interés.

## 📌 Descripción
El script permite obtener datos sobre el tipo de seguro de salud que tiene una persona a partir de su número de documento (DNI) y su fecha de nacimiento. La información obtenida puede ser utilizada para generar marcas o flags, por ejemplo, para campañas financieras.

## 🛠 Tecnologías Utilizadas
- **Python**: Lenguaje de programación principal.
- **BeautifulSoup**: Para el parsing de HTML.
- **Requests**: Para realizar solicitudes HTTP.
- **Tesseract-OCR**: Para la resolución del captcha.
- **OpenCV**: Para el procesamiento de imágenes.
- **Pandas**: Para la manipulación y exportación de datos.

## 📂 Estructura del Proyecto
📁 Proyecto 

│── 📄 main.py (Script principal)

│── 📄 requirements.txt (Librerías necesarias)

│── 📄 config.py (Archivo de configuración con URLs)

│── 📄 dnivalidacion.csv (Archivo de entrada)

│── 📄 output.csv (Archivo de salida con los resultados)


## 📥 Instalación

### 1. Clonar el repositorio
```sh
git clone https://github.com/bri226/proyecto-susalud.git
cd proyecto-susalud
```

## 2. Instalar las dependencias
```
pip install -r requirements.txt
```

## 3. Descargar e instalar Tesseract-OCR
- Descargar desde: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/releases)
- Luego de instalarlo, configurar la ruta en el código:

```python
ts.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
```

## 📊 Entrada y Salida

### Entrada: dnivalidacion.csv
Archivo CSV con dos columnas separadas por |:

```csv
CODDOC|FECHANACIMIENTO
18173735|19880707
```

### Salida: output.csv
Archivo CSV con la siguiente estructura:

```csv
NOMBRE DE IAFAS|REGIMEN|FECHA DE INICIO|FECHA DE FIN|TIPO DE PLAN DE SALUD|ESTADO|DNI
EsSalud|CONTRIBUTIVO|07/07/2008||PLAN ESPECIFICO|ACTIVO|18173735
FEBAN|CONTRIBUTIVO|06/12/2006||SOLO COMPLEMENTARIO|ACTIVO|18173735 ...
```

## 🚀 Ejecución
El script se ejecuta en local. Para correrlo:

```sh
python main.py
```

## 📝 Notas Adicionales
- El código maneja errores de captcha con intentos repetidos (hasta 10 veces).
- La ejecución del script depende de la estabilidad de la página de SUSALUD.
- Se recomienda ejecutar el script en horarios donde la página no tenga alta demanda.

**Autor**: *Brillitt Arellan*
