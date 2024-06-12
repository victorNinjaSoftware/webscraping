import random
import csv
from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36")
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)
with open('protectoras_miwuki.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre", "Tipo de protectora", "Localización", "Casos en adopción", "Adopción urgente", "Valoración", "Descripción", "Imagen"])
    driver.get("https://petshelter.miwuki.com/protectoras-y-asociaciones-de-animales-de-espana")
    boton_cookies = driver.find_element(By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]')
    boton_carga = driver.find_element(By.XPATH, '//button[@id="loadBtn"]')
    try:
        boton_cookies.click()
    except Exception as e:
        print("Cookies aceptadas")
    sleep(2)
    for i in range(30):
        try:
            boton_carga = WebDriverWait(driver, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, '//button[@id="loadBtn"]')))
            driver.execute_script("arguments[0].scrollIntoView();", boton_carga)
            driver.execute_script("arguments[0].click();", boton_carga)
        except NoSuchElementException:
            print("No se encontró el botón de carga.")
            break
        except Exception as e:
            print("Ocurrió un error:", e)
            break
    urls=driver.find_elements(By.XPATH, '//div[@class="col-md-4"]//a')
    lista_urls=[]
    for url in urls:
        lista_urls.append(url.get_attribute("href"))
    print(len(lista_urls))
    for url in lista_urls:
        driver.get(url)
        nombre = driver.find_element(By.XPATH, '//h1').text
        tipo_protectora = driver.find_element(By.XPATH, '//div[contains(@class, "tipo-protectora")]').text
        localizacion = driver.find_element(By.XPATH, '//div[@class="info-item"]').text
        casos_adopcion = driver.find_element(By.XPATH, '//div[@class="col-6 col-md-3"][1]').text
        adopcion_urgente = driver.find_element(By.XPATH, '//div[@class="col-6 col-md-3"][3]').text
        valoracion = driver.find_element(By.XPATH, '//div[@class="actions"]/span[2]//a[1]/span').text
        try:
            descripcion = driver.find_element(By.XPATH, '//div[@class="mb-4"]/p').text
        except Exception as e:
            descripcion = "No tiene descripción "
        imagen = driver.find_element(By.XPATH, '//img[@class="perfil"]').get_attribute("src")
        writer.writerow([nombre, tipo_protectora, localizacion, casos_adopcion, adopcion_urgente, valoracion,
                         descripcion, imagen])