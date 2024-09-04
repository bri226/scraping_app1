from bs4 import BeautifulSoup
import requests
import cv2
from io import BytesIO
from PIL import Image
import pytesseract as ts
import pandas as pd
from config_v0 import *
import time

ts.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def convertir_fecha(fecha_inicial):
    fecha_inicial = str(fecha_inicial)
    fecha_salida = f"{fecha_inicial[:4]}-{fecha_inicial[4:6]}-{fecha_inicial[6:]}"
    return fecha_salida

def resolver_captcha(nombre_captcha):
    img = Image.open(nombre_captcha).convert('LA')
    img.save(nombre_captcha)
    img = cv2.imread(nombre_captcha)
    img = cv2.fastNlMeansDenoisingColored(img,None,16,10,7,30)
    cv2.imwrite(nombre_captcha, img)
    ocr_result=ts.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKMNLOPQRSTUVWXYZ')
    ocr_result=ocr_result.replace(" ", "").strip()
    return(ocr_result)

def extract_table_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    return df

if __name__ == '__main__':

    # Lectura de datos
    input_data = pd.read_csv('dnivalidacion.csv', sep='|')
    # input_data = input_data.head(10)

    # Definición de URLs
    url_form = URL_FORM
    url_post = URL_POST
    captcha_url = CAPTCHA_URL

    tiempo_acum = 0
    count_founded = 0
    all_dataframes = []

    # Iteración por DNI
    for index, row in input_data.iterrows():
        inicio = time.time()
        session = requests.Session()
        DNI = row['CODDOC']
        fecha_nacimiento = convertir_fecha(row['FECHANACIMIENTO'])
        errores_captcha = 0
        # Iteración por cada error de captcha
        for i in range(10):
            # Solicitudes
            captcha_response = session.get(captcha_url)
            captcha_image = Image.open(BytesIO(captcha_response.content))
            captcha_image.save('captcha.png')
            captcha_text = resolver_captcha('captcha.png')
      
            # Data
            data = {
                'cboPais': 'PER',
                'cboTDoc': '1',
                'txtNroDoc': DNI,
                'txtFechaNac': fecha_nacimiento,
                'txtCaptcha': captcha_text
            }

            response = session.post(url_post, data=data)

            if response.status_code == 200:
                if(response.text.find('</table>') != -1):
                    df = extract_table_from_html(response.text)
                    df['DNI'] = DNI
                    all_dataframes.append(df)
                    count_founded += 1
                    time.sleep(1)
                    break
                elif(response.text.find('No existe información de esta persona en el Registro') != -1):
                    # print(response.text)
                    break
                else:
                    errores_captcha += 1
                    # print(response.text)
            else:
                print(f"Error al enviar la solicitud: {response.status_code}")

        fin = time.time()
        tiempo = fin - inicio
        tiempo_acum = tiempo_acum + tiempo
        tiempo_prom = tiempo_acum / (index + 1)

        print(f"DNI: {DNI} | Errores captcha: {errores_captcha} Tiempo: {round(tiempo,2)}s | Tiempo prom: {round(tiempo_prom,2)}s")
    
    final_dataframe = pd.concat(all_dataframes, ignore_index=True)
    final_dataframe.to_csv('output.csv', index=False, sep='|')
    print(f"Cantidad de registros encontrados: {count_founded} de {len(input_data)}")

