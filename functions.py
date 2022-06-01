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
DOWNLOADS_DIR = '/home/ricardo/Insync/ricardo_rp04@hotmail.com/OneDrive/pgmjud/eProc-TJSC-JFSC-webscraper/processos/'
chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": DOWNLOADS_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    })
print('12')
# service=Service(r'/opt/apps/cn.google.chrome/files/chrome')
driver = webdriver.Chrome(options = chrome_options, service=Service(ChromeDriverManager(version='83.0.4103.14').install()))
print('13')
driver.window_handles
main_window = driver.current_window_handle

def drive_init(tribunal):
    sleep(1)
    if tribunal == 'tjsc':
        driver.get('https://eproc1g.tjsc.jus.br/eproc/')
        # driver.get('www.google.com.br')
    else:
        driver.get('https://eproc.jfsc.jus.br/eprocV2/')

def eproc_login(username, password):
    sleep(1)
    driver.find_element_by_id('txtUsuario').send_keys(username)
    driver.find_element_by_id('pwdSenha').send_keys(password)
    sleep(1)
    driver.find_element_by_id('sbmEntrar').click()
    sleep(3) 

def get_procs():
    with open(sys.argv[1]) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def search(proc):
    ok = False
    driver.find_element_by_name('txtNumProcessoPesquisaRapida').send_keys(proc)
    sleep(0.5)
    driver.find_element_by_name('txtNumProcessoPesquisaRapida').send_keys(Keys.ENTER)
    sleep(1)   
    try:
        driver.find_element_by_link_text('Árvore')          
    except NoSuchElementException:
        error_log(proc)
        print("Processo não encontrado:",proc)
    else:
        # sleep(3)
        ok = True
        # docs = driver.find_elements(By.CLASS_NAME, 'infraLinkDocumento')
        # for doc in docs:
        #     if 'INIC1' in doc.text:
        #         doc.click()
        #         sleep(1)
        #         break
        # driver.switch_to.window(driver.window_handles[-1])
        # driver.switch_to.frame('conteudoIframe')
        # driver.find_element(By.TAG_NAME, 'button').click()
        # driver.close()
        # driver.switch_to.window(driver.window_handles[-1])
    return ok

def download_inicial(proc):
    try:
        driver.execute_script('javascript:alterarPagina(\'ultima\')')
        sleep(4)
    except:
        pass
    # 0307204-50.2018.8.24.0033
    try:
        driver.find_element(By.XPATH, "// a[contains(text(), 'INIC1')]").click()
        print('INIC1')
    except:
        try:
            driver.find_element(By.XPATH, "// a[contains(text(), 'PET1')]").click()
            print('PET1')
        except:
            return False
    driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.frame('conteudoIframe')
    driver.find_element(By.TAG_NAME, 'button').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    return True
