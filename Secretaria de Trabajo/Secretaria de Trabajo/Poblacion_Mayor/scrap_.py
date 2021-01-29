import requests
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
#from .read_file import ReadFile


class WebScrap ():

    def __init__(self):
        self.name = 'WebScrap'

    def scrap(self,url_scraping):
        file_path = os.getcwd()+"\\data"
        chromedrive_path = os.getcwd()+"\\chromedrive"
        chrome_options = Options()
        chrome_options.headless = True

        # path to save file
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": file_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        })
        # path where we have the crhomedrive
        browser = webdriver.Chrome(chromedrive_path+'\\chromedriver.exe', options=chrome_options)
        browser.get(url_scraping)
        print('Entró a la pagina')

        # select the option in the form
        inegi = browser.find_element_by_id('Checkbox14').click()
        time.sleep(2)

        # press the buttom to do the consult
        inegi = browser.find_element_by_css_selector(
            'input[value="Ver consulta"]').click()
        time.sleep(2)
        print('accedemos a la consulta')

        # select the federal entity in a dropdown
        inegi = Select(browser.find_element_by_id(
            'C_Where_Entidad Federativa'))
        inegi.select_by_visible_text('  Puebla')

        # select the buttom to update the federal entity
        inegi = browser.find_element_by_name('Actualizar').click()
        time.sleep(2)
        print('Actualizo la busqueda ')

        # sleect the option of download CSV in the dropdown
        inegi = Select(browser.find_element_by_id('Select1'))
        inegi.select_by_visible_text('Texto separado por comas (.csv)')

        inegi = browser.find_element_by_id('Button1').click()
        time.sleep(2)
        print('ya descargo el archivo Poblacion_Mayor')
