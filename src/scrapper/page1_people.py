''' Script to handle with the first page 'Pessoas' '''
import datetime
from helpers.datamodel import DataModel
from helpers.constants import WAYPATH
from helpers.dialogator import throw_popup_error
from scrapper.webhandler import WebHandler, ElementNotFoundException

def page1_people(handler: WebHandler, data: DataModel) -> None:
    ''' Method to handle with the first page 'Pessoas' '''
    website = str(WAYPATH.get('EMIT_SITE', ''))
    handler.driver.get(website)
    current_date = datetime.datetime.now()
    handler.get_element('EMIT_COMPETENCIA', 'CURTO', current_date)
    handler.get_element('EMIT_AVANCAR', 'CURTO').click()
    handler.loading_wait('NFSE_LOAD', 'CURTO')
    #handler.select_radio('EMIT_EMITENTE_RDB', 'CURTO', 1) # Disabled
    handler.select_radio('EMIT_TOMADOR_RDB', 'CURTO', 2)
    handler.get_element('EMIT_TOMADOR_BTN', 'CURTO').click()
    tomadores = handler.get_elements('EMIT_TOMADOR_LIST_ROW', 'CURTO')
    if tomadores is None:
        raise throw_popup_error(
            ElementNotFoundException(
                'O elemento EMIT_TOMADOR_LIST_ROW não foi encontrado!'))
    for i, _ in enumerate(tomadores, 1):
        tomador = handler.get_element('EMIT_TOMADOR_LIST_TXT', 'CURTO', None, i)
        if data.tomador in tomador.text.upper():
            #tomador.click()
            handler.get_element('EMIT_TOMADOR_LIST_RDB', 'CURTO', None, i).click()
            handler.get_element('EMIT_TOMADOR_IMPORT_BTN', 'CURTO').click()
    #handler.select_radio('EMIT_INTERMEDIARIO', 'CURTO', 1) # Disabled
    handler.get_element('EMIT_AVANCAR', 'CURTO').click()
