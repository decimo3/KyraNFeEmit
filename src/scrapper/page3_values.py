''' Script to handle with the third page 'Valores' '''
from helpers.normalizer import norm_float
from helpers.datamodel import DataModel
from scrapper.webhandler import WebHandler

def page3_values(handler: WebHandler, data: DataModel) -> None:
    ''' Method to handle with the third page 'Valores' '''
    handler.get_element('VAL_VALORES', 'CURTO', norm_float(data.valor_total))
    handler.select_radio('VAL_ISSQN', 'CURTO', 1)

    if data.cotas_impostos['ISS']:
        handler.select_radio('VAL_RETIDO', 'CURTO', 2)
        handler.loading_wait('NFSE_LOAD', 'CURTO')
        handler.select_radio('VAL_TOMADOR', 'CURTO', 1)
    else:
        handler.select_radio('VAL_RETIDO', 'CURTO', 1)

    handler.select_radio('VAL_BENEFICIARIO', 'CURTO', 1)

    if data.cotas_impostos['ISS']:
        handler.select_radio('VAL_DEDUCAO', 'CURTO', 1)

    handler.get_element('VAL_ALIQUOTA', 'CURTO').click()
    if not handler.get_elements('VAL_ALIQUOTA_OPT', 'CURTO'):
        handler.get_element('VAL_ALIQUOTA', 'CURTO').click()
    handler.select_option('VAL_ALIQUOTA_OPT', 'CURTO',
            '01 - Operação Tributável com Alíquota Básica')

    handler.get_element('VAL_ALIQUOTA_BASE', 'CURTO',
            norm_float(data.valor_total))
    handler.get_element('VAL_ALIQUOTA_PIS', 'CURTO',
            norm_float(data.cotas_impostos['PIS'] * 100))
    handler.get_element('VAL_ALIQUOTA_COFINS', 'CURTO',
            norm_float(data.cotas_impostos['COFINS'] * 100))

    handler.get_element('VAL_RETENCAO_PCC_TIPO', 'CURTO').click()
    if not handler.get_elements('VAL_RETENCAO_PCC_TIPO_OPT', 'CURTO'):
        handler.get_element('VAL_RETENCAO_PCC_TIPO', 'CURTO').click()
    handler.select_option('VAL_RETENCAO_PCC_TIPO_OPT', 'CURTO',
            'PIS/COFINS/CSLL Retidos')

    irpf_value = norm_float(data.valor_total * data.cotas_impostos['IRPJ'])
    handler.get_element('VAL_RETENCAO_IRPJ_VAL', 'CURTO', irpf_value)

    ifcs_value = norm_float(data.valor_total * data.cotas_impostos['PCC'])
    handler.get_element('VAL_RETENCAO_PCC_VAL', 'CURTO', ifcs_value)

    inss_value = norm_float(data.valor_total * data.cotas_impostos['CMO'] * data.cotas_impostos['INSS'])
    handler.get_element('VAL_RETENCAO_INSS_VAL', 'CURTO', inss_value)

    handler.select_radio('VAL_TRIBUTOS_TIPO', 'CURTO', 2)
    handler.get_element('VAL_TRIBUTOS_FEDERAL', 'CURTO',
            norm_float(data.cotas_impostos['FEDERAIS'] * 100))
    handler.get_element('VAL_TRIBUTOS_ESTADUAL', 'CURTO',
            norm_float(data.cotas_impostos['ESTADUAIS'] * 100))
    handler.get_element('VAL_TRIBUTOS_MUNINCIPAL', 'CURTO',
            norm_float(data.cotas_impostos['MUNICIPAIS'] * 100))

    handler.get_element('VAL_AVANCAR', 'CURTO').click()
