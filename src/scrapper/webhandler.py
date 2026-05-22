''' Module to setup and startup webdriver '''
import os
import datetime
from time import sleep
from typing import Any
from pandas import Timestamp
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from helpers.constants import CONFIGS, WAYPATH, WAITSEC, BASE_FOLDER
from helpers.dialogator import throw_popup_error

class ElementNotFoundException(Exception):
    ''' Custon exception to indicate when element is not found '''

BY = {
    '#': By.ID,
    '/': By.XPATH,
    '.': By.CLASS_NAME
}

class WebHandler:
    ''' Class to Wrap webdriver '''
    def __init__(self, sitepath: str) -> None:
        siteurl = str(WAYPATH.get(sitepath, ''))
        if not siteurl:
            raise throw_popup_error(ValueError(
                f'A caminho {sitepath} não foi definido!'))
        chromepath = CONFIGS.get('GCHROME', '')
        if not chromepath:
            raise throw_popup_error(ValueError(
                'A configuração GCHROME não foi definida!'))
        downpath = os.path.join(BASE_FOLDER, 'data')
        if not os.path.exists(downpath):
            os.mkdir(downpath)
        temppath = os.path.join(BASE_FOLDER, 'temp')
        if not os.path.exists(temppath):
            os.mkdir(temppath)
        driverpath = os.path.join(BASE_FOLDER, 'chromedriver-win64', 'chromedriver.exe')
        if not os.path.exists(driverpath):
            raise throw_popup_error(FileNotFoundError(
                f'O programa "{driverpath}" não está acessível!'))
        service = Service(executable_path=driverpath)
        options = webdriver.ChromeOptions()
        options.binary_location = chromepath
        options.add_argument(f'--app={siteurl}')
        options.add_argument(f'--user-data-dir={temppath}')
        options.add_experimental_option('prefs',
                {
                    'profile.default_content_settings.popups': 0,
                    'download.default_directory': downpath,
                })
        self.driver = webdriver.Chrome(service=service, options=options) # pylint: disable=not-callable
        self.driver.maximize_window()
    def get_elements(self,
            pathname: str,
            timeout: str,
            replace_text1: int | None = None,
            replace_text2: int | None = None,
            element_check: bool = True
        ) -> list[WebElement] | None:
        ''' Function to get a list of WebElements '''
        # Example 1: /html/body/main/form
        # Will be By.XPATH and '/html/body/main/form'
        # Example 2: #form-item
        # Will be By.CLASS_NAME and 'form-item'
        # Example 3: .form-id
        # Will be By.ID and 'form-id'
        pathvalue = WAYPATH.get(pathname, '')
        if not pathvalue:
            raise throw_popup_error(ValueError(
                f'A caminho {pathname} não foi encontrado na configuração!'))
        if not replace_text1 is None:
            pathvalue = pathvalue.replace('?', str(replace_text1))
        if not replace_text2 is None:
            pathvalue = pathvalue.replace('¿', str(replace_text2))
        bytype = BY.get(pathvalue[:1], '')
        if not bytype:
            raise throw_popup_error(ValueError(
                f'O tipo do caminho {pathname} não pode ser definido!'))
        byvalue = pathvalue[1:] if bytype != By.XPATH else pathvalue
        seconds = WAITSEC.get(timeout, 0)
        expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        while datetime.datetime.now() <= expiration_time:
            elements = self.driver.find_elements(bytype, byvalue)
            if elements:
                if element_check:
                    element = elements[0]
                    if not element.is_displayed() or not element.is_enabled():
                        sleep(0.2)
                        continue
                return elements
            sleep(0.2)
        return None
    def get_element(self,
            pathname: str,
            timeout: str,
            value: Any | None = None,
            replace_text1: int | None = None,
            replace_text2: int | None = None,
        ) -> WebElement:
        ''' Function to get a single WebElement '''
        elements = self.get_elements(pathname, timeout, replace_text1, replace_text2)
        if not elements:
            raise throw_popup_error(ElementNotFoundException(
                f'O elemento {pathname} não foi encontrado!'))
        element = elements[0]
        if value:
            if isinstance(value, list):
                element.send_keys('\n'.join(value))
            if isinstance(value, (str, int)):
                element.click() # Set focus on input
                element.clear() # Clear value if already filled
                element.send_keys(str(value)) # Set new input value
            if isinstance(value, (datetime.datetime, Timestamp)):
                element.send_keys(value.strftime('%d/%m/%Y')) # If value is
        return element
    def select_option(self,
            pathname: str,
            timeout: str,
            value: str,
            replace_text1: int | None = None,
            replace_text2: int | None = None,
        ) -> None:
        ''' Function to wrap change select element value '''
        options = self.get_elements(pathname, timeout, replace_text1, replace_text2)
        if not options:
            raise throw_popup_error(ElementNotFoundException(
                f'As opções de seleção para {pathname} não foram encontradas!'))
        for option in options:
            if option.text == value or option.text.startswith(value):
                option.click()
                return
        raise throw_popup_error(ElementNotFoundException(
                f'A opção para o valor "{value}" não foi encontrado!'))
    def select_search(self,
            _: str,
            timeout: str,
            value: str,
            replace_text1: int | None = None,
            replace_text2: int | None = None,
        ) -> None:
        ''' Function to wrap change select search value '''
        select = self.get_element('NFSE_SEARCH', timeout, replace_text1, replace_text2)
        select.send_keys(value.split('/', 1)[0])
        self.loading_wait('NFSE_LOAD', timeout)
        options = self.get_elements('NFSE_OPTION', timeout)
        if not options:
            raise throw_popup_error(ElementNotFoundException(
                f'Não foram encontrados resultados para o valor "{value}"'))
        for option in options:
            if option.text == value or ('/' not in value and option.text.startswith(value)):
                option.click()
                return
        raise throw_popup_error(
            ElementNotFoundException(
                f'A opção para o valor "{value}" não foi encontrado!'))
    def select_radio(self,
            pathname: str,
            timeout: str,
            value: int,
            replace_text1: int | None = None,
            replace_text2: int | None = None,
        ) -> None:
        ''' Function to wrap change radio element value

        value is not 0 base number, the first is 1
        '''
        radios = self.get_elements(pathname, timeout, replace_text1, replace_text2, False)
        if radios is None:
            raise throw_popup_error(ElementNotFoundException(
                f'O elemento {pathname} não foi encontrado!'))
        if len(radios) < value:
            raise throw_popup_error(ElementNotFoundException(
                f'''Não foram encontrados elementos suficientes de
                    {pathname} ({len(radios)}) para o indice {str(value)}!'''))
        radios[value - 1].click()
    def loading_wait(self,
        pathname: str,
        timeout: str,
        replace_text1: int | None = None,
        replace_text2: int | None = None,
        ) -> None:
        ''' Function to wait a amount of time or loading element desapear '''
        loading_found = False
        seconds = WAITSEC.get(timeout, 0)
        wait_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        while datetime.datetime.now() <= wait_time:
            elements = self.get_elements(pathname, 'CURTO', replace_text1, replace_text2)
            if elements:
                loading_found = True
            if loading_found and not elements:
                return
            sleep(1)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
