''' Module to handle with authentication '''
from scrapper.webhandler import WebHandler
from helpers.constants import CONFIGS, WAYPATH

def authentication(handler: WebHandler) -> None:
    ''' Method  to handle with authentication '''
    website = str(WAYPATH.get('AUTH_SITE', ''))
    username = str(CONFIGS.get('USUARIO', ''))
    password = str(CONFIGS.get('PALAVRA', ''))
    handler.driver.get(website)
    handler.get_element('AUTH_LOGIN', 'MEDIO', username)
    handler.get_element('AUTH_PASSWD', 'CURTO', password)
    handler.get_element('AUTH_BUTTON', 'CURTO').click()
    handler.loading_wait('NFSE_LOAD', 'CURTO')
