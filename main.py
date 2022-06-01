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

from functions import *


def main():
    # le argumentos da linha de comando
    arguments = sys.argv
    if len(arguments) < 3:
        print("Uso: python main.py <USUARIO> <SENHA>")
        sys.exit()

    user = arguments[1]
    password = arguments[2]
    processo = arguments[3]

    drive_init('tjsc')
    eproc_login(user, password)
    search(processo)
    download_inicial(processo)

    sleep(1000000)



if __name__ == "__main__":
    main()