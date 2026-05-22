''' Script to handle with the fifty page 'Save' '''
import os
from pathlib import Path
from helpers.constants import CONFIGS, BASE_FOLDER, VERDADEIROS
from helpers.dialogator import show_popup_ask, throw_popup_error
from scrapper.webhandler import WebHandler
from scrapper.download import download_file

def page5_save(handler: WebHandler, filepath: Path) -> None:
    ''' Method to handle with the fifty page 'Save' '''
    download_dir = os.path.join(BASE_FOLDER, 'data')
    download_dir = Path(download_dir)
    destpath = Path(filepath.parent)

    if not download_dir.is_dir() or not destpath.is_dir():
        raise throw_popup_error(OSError(
            'Os caminhos para download não estão disponíveis!'))

    # If the EMITIR configuration is not enabled, the program will ask for confirmation
    # before proceeding to the next steps, operating in a "semi-automatic" mode.
    is_emit_allowed = str(CONFIGS.get('EMITIR', '')).lower() in VERDADEIROS
    if not is_emit_allowed:
        if not show_popup_ask('Aguardando a liberação para prosseguir...'):
            raise throw_popup_error(ValueError(
                'Operação cancelada pelo usuário!'))

    handler.get_element('EMIT_GENERATE', 'CURTO').click()

    note = handler.get_element('EMIT_NFE_NUM', 'CURTO', None, 1).text
    if len(note) == 50:
        note = note[32:36]

    os.mkdir(str(destpath / ('NF ' + note)))
    destpath = destpath / ('NF ' + note)
    filepath.replace(destpath / filepath.name)

    handler.get_element('EMIT_XML_SAVE', 'CURTO').click()
    download_file(download_dir, destpath)

    handler.get_element('EMIT_PDF_SAVE', 'CURTO').click()
    download_file(download_dir, destpath)

    handler.get_element('EMIT_NFE_NEW', 'CURTO').click()
