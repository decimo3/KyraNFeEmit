''' Project to automate EmissorNacional form fill '''
import os
import re
from pathlib import Path
from helpers.bannershow import print_header_presentation
from helpers.runchecker import instance_checker
from helpers.updater import update_chromedriver
from helpers.constants import CONFIGS, BASE_FOLDER
from helpers.excelhandler import get_dataframe_from_excel
from helpers.dialogator import show_popup_info
from helpers.datamodel import DataModel
from scrapper.webhandler import WebHandler, ElementNotFoundException
from scrapper.authentication import authentication
from scrapper.page1_people import page1_people
from scrapper.page2_service import page2_service
from scrapper.page3_values import page3_values
from scrapper.page4_emit import page4_emit
from scrapper.page5_save import page5_save

if __name__ == '__main__':
    print_header_presentation()
    instance_checker()
    update_chromedriver()

    # DONE - Init handler web
    handler = WebHandler('NFSE_SITE')
    authentication(handler)

    # DONE - Get tax table informations
    tax_path = os.path.join(BASE_FOLDER,
        'Cota de Impostos Estruturados.xls')
    tax_data = get_dataframe_from_excel(tax_path)

    # DONE - Get complementary codes info
    ext_path = os.path.join(BASE_FOLDER,
        'Codes Complementares por Municipio.xls')
    ext_data = get_dataframe_from_excel(ext_path)

    iss_path = os.path.join(BASE_FOLDER, 'ISS.xls')
    iss_data = get_dataframe_from_excel(iss_path)

    # DONE - Get workorder informations
    dat_path = Path(str(CONFIGS.get('DATAPATH', '')))
    dat_files = list(dat_path.rglob('*.xls'))

    pattern = re.compile(r'^\d{10}\.xls$')

    for dat_file in dat_files:
        try:
            if not pattern.match(dat_file.name):
                show_popup_info(f'O nome do arquivo {dat_file.name} não está conforme o padrão', False)
                continue
            # DONE - Check if have '.xml' on same folder, if have, continue to next
            if list(dat_file.parent.glob('*.xml')):
                show_popup_info(f'O documento {dat_file} já foi enviado, pulando...', False)
                continue
            # DONE - Get informations value from file path
            tomador = str(dat_file).replace(str(dat_path) + os.sep, '').split(os.sep, 1)[0]
            # DONE - Get order values from order table
            order_data = get_dataframe_from_excel(str(dat_file), 1)
            # DONE - Filter tax table to get current tax info
            data_model = DataModel(tomador, order_data, tax_data, ext_data, iss_data)
            page1_people(handler, data_model)
            page2_service(handler, data_model)
            page3_values(handler, data_model)
            page4_emit(handler, data_model)
            page5_save(handler, dat_file)
        except ValueError, ElementNotFoundException:
            pass
    show_popup_info('Programa finalizado!')
