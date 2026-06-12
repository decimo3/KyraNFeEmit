''' Script to handle with the second page 'Serviços' '''
from helpers.normalizer import norm_float
from helpers.datamodel import DataModel
from scrapper.webhandler import WebHandler

def page2_service(handler: WebHandler, data: DataModel) -> None:
    ''' Method to handle with the second page 'Serviços' '''
    #handler.get_element('SERV_NACAO', 'CURTO').click()
    #if not handler.get_elements('SERV_NACAO_OPT', 'CURTO'):
    #    handler.get_element('SERV_NACAO', 'CURTO').click()
    #handler.select_option('SERV_NACAO_OPT', 'CURTO', 'Brasil')

    handler.get_element('SERV_ESTADO', 'CURTO').click()
    if data.tomador == 'AMPLA' and data.codigo == '0711':
        handler.select_search('SERV_ESTADO', 'CURTO', 'Rio de Janeiro/RJ')
    else:
        handler.select_search('SERV_ESTADO', 'CURTO', data.municipio + '/RJ')

    handler.get_element('SERV_CODIGO', 'CURTO').click()
    # FIXME - Adicionar a condição para concessionária LIGHT
    if data.tomador == 'AMPLA' and data.codigo == '0711':
        handler.select_search('SERV_CODIGO', 'CURTO', '07.11.02')
        handler.get_element('SERV_ADICIONAL', 'CURTO').click()
        if not handler.get_elements('SERV_ADICIONAL_OPT', 'CURTO'):
            handler.get_element('SERV_ADICIONAL', 'CURTO').click()
        handler.select_option('SERV_ADICIONAL_OPT', 'CURTO', '07.11.02.002')

    elif data.tomador == 'AMPLA' and data.codigo == '0702' and data.code_complementar:
        handler.select_search('SERV_CODIGO', 'CURTO', data.code_complementar['Code'])
        handler.get_element('SERV_ADICIONAL', 'CURTO').click()
        if not handler.get_elements('SERV_ADICIONAL_OPT', 'CURTO'):
            handler.get_element('SERV_ADICIONAL', 'CURTO').click()
        handler.select_option('SERV_ADICIONAL_OPT', 'CURTO', data.code_complementar['Complementar'])

    elif data.tomador == 'LIGHT' and data.code_complementar:
        handler.select_search('SERV_CODIGO', 'CURTO', data.code_complementar['Code'])
        handler.get_element('SERV_ADICIONAL', 'CURTO').click()
        if not handler.get_elements('SERV_ADICIONAL_OPT', 'CURTO'):
            handler.get_element('SERV_ADICIONAL', 'CURTO').click()
        handler.select_option('SERV_ADICIONAL_OPT', 'CURTO', data.code_complementar['Complementar'])

    else:
        formated_code = data.codigo[0:2] + '.' + data.codigo[2:4] + '.02'
        handler.select_search('SERV_CODIGO', 'CURTO', formated_code)

    handler.select_radio('SERV_ISSQN', 'CURTO', 1)

    formated_desc = str(data.cotas_impostos['DESCRICAO']).format(
        contrato = data.contrato,
        pedido = data.pedido,
        conformidade = (str(int(
            data.conformidade
            if data.tomador == 'AMPLA' else
            data.pedido))),
        valor_cmo = norm_float(data.valor_total * data.cotas_impostos['CMO']),
        valor_inss = norm_float(
            data.valor_total *
            data.cotas_impostos['CMO'] *
            data.cotas_impostos['INSS']),
        municipio = data.municipio.upper()
    )
    handler.get_element('SERV_DESCRICAO', 'CURTO', formated_desc)

    handler.get_element('SERV_NBS', 'CURTO').click()
    if not handler.get_elements('SERV_NBS_OPT', 'CURTO'):
        handler.get_element('SERV_NBS', 'CURTO').click()
    handler.get_element('SERV_NBS_SRC', 'CURTO',
            str(int(data.cotas_impostos['NBS'])))
    handler.select_option('SERV_NBS_OPT', 'CURTO',
            str(int(data.cotas_impostos['NBS'])))

    if not data.codigo == '0711':
        handler.select_radio('SERV_OBRA_RDB', 'CURTO', 1)
        handler.get_element('SERV_OBRA_TXT', 'CURTO', 'COI')

    handler.get_element('SERV_AVANCAR', 'CURTO').click()
