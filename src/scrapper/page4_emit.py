''' Script to handle with the fourth page 'Emissão' '''
from helpers.constants import VALUE_TOLERANCE
from helpers.dialogator import throw_popup_error
from helpers.normalizer import norm_money
from helpers.datamodel import DataModel
from scrapper.webhandler import ElementNotFoundException, WebHandler


def page4_emit(handler: WebHandler, data: DataModel) -> None:
    ''' Method to handle with the fourth page 'Emissão' '''
    keys = handler.get_elements('EMIT_DICTIONARY', 'CURTO', 1)
    vals = handler.get_elements('EMIT_DICTIONARY', 'CURTO', 2)


    if not keys or not vals or len(keys) != len(vals):
        raise throw_popup_error(
            ElementNotFoundException(
                'O elemento EMIT_DICTIONARY não foi encontrado!'))

    kv_dict = { key.text.strip(): norm_money(val.text) for key, val in zip(keys, vals) }

    # Check
    value_bruto_expected = data.valor_total
    if (kv_dict['Base de cálculo:'] - value_bruto_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor BRUTO não corresponde com o esperado!\n\nValor esperado: {value_bruto_expected}, Valor encontrado: {kv_dict['Base de cálculo:']}'))

    # Check

    if data.cotas_impostos['ISS'] > 0:
        value_issqn_expected = data.valor_total * float(data.data['ISS'])
        value_issqn_calculated = kv_dict['ISSQN (Retido):']
        if (value_issqn_calculated - value_issqn_expected) > VALUE_TOLERANCE:
            raise throw_popup_error(ValueError(
                f'O valor ISSQN não corresponde com o esperado!\n\nValor esperado: {value_issqn_expected}, Valor encontrado: {kv_dict['ISSQN :']}'))

    value_pis_expected = data.valor_total * data.cotas_impostos['PIS']
    if (kv_dict['PIS - Débito Apuração Própria:'] - value_pis_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor PIS não corresponde com o esperado!\n\nValor esperado: {value_pis_expected}, Valor encontrado: {kv_dict['PIS - Débito Apuração Própria:']}'))

    value_cofins_expected = data.valor_total * data.cotas_impostos['COFINS']
    if (kv_dict['COFINS - Débito Apuração Própria:'] - value_cofins_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor COFINS não corresponde com o esperado!\n\nValor esperado: {value_cofins_expected}, Valor encontrado: {kv_dict['COFINS - Débito Apuração Própria:']}'))

    value_irpj_expected = data.valor_total * data.cotas_impostos['IRPJ']
    value_irpj_calculated = kv_dict['Imposto de Renda Retido na Fonte (IRRF):']
    if (value_irpj_calculated - value_irpj_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor IRPJ não corresponde com o esperado!\n\nValor esperado: {value_irpj_expected}, Valor encontrado: {kv_dict['Imposto de Renda Retido na Fonte (IRRF):']}'))

    value_ifcs_expected = data.valor_total * data.cotas_impostos['PCC']
    if (kv_dict['Contribuições Sociais - Retidas:'] - value_ifcs_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor IFCS não corresponde com o esperado!\n\nValor esperado: {value_ifcs_expected}, Valor encontrado: {kv_dict['Contribuições Sociais - Retidas:']}'))

    value_inss_expected = (
        data.valor_total *
        data.cotas_impostos['CMO'] *
        data.cotas_impostos['INSS']
    )
    if (kv_dict['Contribuição Previdenciária - Retida:'] - value_inss_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor INSS não corresponde com o esperado!\n\nValor esperado: {value_inss_expected}, Valor encontrado: {kv_dict['Contribuição Previdenciária - Retida:']}'))

    value_liquido_expected = (
        data.valor_total - (
        float(value_irpj_expected) +
        float(value_ifcs_expected) +
        float(value_inss_expected) +
        (float(data.valor_total * float(data.data['ISS'])) if data.cotas_impostos['ISS'] > 0 else 0)
    ))
    if (kv_dict['Valor líquido da NFS-e:'] - value_liquido_expected) > VALUE_TOLERANCE:
        raise throw_popup_error(ValueError(
            f'O valor LIQUIDO não corresponde com o esperado!\n\nValor esperado: {value_liquido_expected}, Valor encontrado: {kv_dict['Valor líquido da NFS-e:']}'))
