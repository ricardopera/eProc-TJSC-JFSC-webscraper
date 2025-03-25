from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
from os import walk
from os import listdir
import os
import re
import openpyxl
from systemtools.number import parseNumber

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SHORT_TIMEOUT = 10
LONG_TIMEOUT = 20
VERY_LONG_TIMEOUT = 120
EPROC_TJSC = '0033'
EPROC_JFSC = '7208'
timeout = [SHORT_TIMEOUT,LONG_TIMEOUT,VERY_LONG_TIMEOUT]
DOWNLOADS_DIR = os.getcwd() + '/downloads/'
PROCESSOS_DIR = os.getcwd() + '/processos/'
HEADLESS = False
chrome_options = Options()
if HEADLESS:
    chrome_options.add_argument("--headless")
# chrome_options.add_argument('window-size=1920,1080')
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": DOWNLOADS_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    })
print('12')
# service = Service(ChromeDriverManager(version='83.0.4103.14').install())
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options = chrome_options, service=service)
driver.set_window_size(1920, 1080)
# driver.maximize_window()
print('13')
driver.window_handles
main_window = driver.current_window_handle


def drive_init(tribunal):
    sleep(1)
    if tribunal == 'tjsc':
        driver.get('https://eproc1g.tjsc.jus.br/eproc/')
        # driver.maximize_window()
    else:
        driver.get('https://eproc.jfsc.jus.br/eprocV2/')
        # driver.maximize_window()

def eproc_login(username, password):
    sleep(1)
    driver.find_element(By.ID, 'txtUsuario').send_keys(username)
    driver.find_element(By.ID, 'pwdSenha').send_keys(password)
    sleep(1)
    driver.find_element(By.ID, 'sbmEntrar').click()
    sleep(3) 

def get_procs():
    with open(sys.argv[1]) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def search(proc):
    driver.find_element(By.NAME, 'txtNumProcessoPesquisaRapida').send_keys(proc)
    sleep(0.5)
    driver.find_element(By.NAME, 'txtNumProcessoPesquisaRapida').send_keys(Keys.ENTER)
    WebDriverWait(driver, LONG_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "// a[text()='Árvore']")))
    # sleep(2)   
    try:
        driver.find_element(By.LINK_TEXT, 'Árvore')          
    except NoSuchElementException:
        # error_log(proc)
        print("Processo não encontrado:",proc)
        return False
    else:
        return True

def download_inicial(proc):
    try:
        driver.execute_script('javascript:alterarPagina(\'ultima\')')
        sleep(4)
    except:
        pass
    # 0307204-50.2018.8.24.0033
    try:
        driver.find_element(By.XPATH, "// a[text()='INIC1']").click()
        print('INIC1', proc)
    except:
        try:
            driver.find_element(By.XPATH, "// a[text()='PET1']").click()
            print('PET1', proc)
        except:
            print('Petição inicial não encontrada, processo:',proc)
            return False
    driver.switch_to.window(driver.window_handles[-1])
    # sleep(5)
    driver.switch_to.frame('conteudoIframe')
    if not HEADLESS:
        driver.find_element(By.TAG_NAME, 'button').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    sleep(1)
    i = 0
    while os.listdir(DOWNLOADS_DIR) == []:
        sleep(1)
        i += 1
        if i > 10:
            return False
    while not os.listdir(DOWNLOADS_DIR)[0].endswith('.pdf'):
        sleep(1)
        i += 1
        if i > 20:
            return False
    os.rename(DOWNLOADS_DIR + os.listdir(DOWNLOADS_DIR)[0], PROCESSOS_DIR + proc + '.pdf')
    return True
