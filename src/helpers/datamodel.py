''' Class to hold information to use alongside the program '''
from typing import Any
import pandas
from Levenshtein import distance
from helpers.dialogator import throw_popup_error
from helpers.excelhandler import find_column
from helpers.constants import CITIES, CITIES_RAW, TEXT_TOLERANCE
from helpers.normalizer import norm_txt

class DataModel:
    ''' Class to hold information to use alongside the program '''
    tomador: str
    codigo: str
    pedido: str
    contrato: str
    municipio: str
    valor_total: float
    data: dict [str, str]
    iss_data: dict [str, str]
    cotas_impostos: dict[str, Any]
    code_complementar: dict[str, str]

    def __init__(self,
            tomador: str,
            dat: pandas.DataFrame,
            tax: pandas.DataFrame,
            ext: pandas.DataFrame,
            iss: pandas.DataFrame,
        ) -> None:
        self.tomador = tomador
        self.get_dat_info(dat)
        self.get_iss_info(iss)
        self.get_tax_info(tax)
        self.get_ext_info(ext)

    def get_correct_city_name(self, text: str) -> str:
        ''' Method that assert municipio value '''
        norm_city = norm_txt(text)
        # If
        if norm_city in CITIES_RAW:
            index = CITIES_RAW.index(norm_city)
            return CITIES[index]
        current_index = 0
        current_distance = 99
        for i, raw_city in enumerate(CITIES_RAW):
            j = distance(norm_city, raw_city)
            if j < current_distance:
                current_distance = j
                current_index = i
        if current_distance > TEXT_TOLERANCE:
            raise throw_popup_error(ValueError(
                f'Não foi encontrada cidade para o valor {text}'))
        return CITIES[current_index]

    def get_dat_info(self, dat: pandas.DataFrame) -> None:
        ''' Method to extract data information '''
        self.data = dat.iloc[0].to_dict()
        ctt_column = find_column(dat, 'COLUNAS_CONTRATO')
        val_column = find_column(dat, 'COLUNAS_VALORADO')
        cod_column = find_column(dat, 'COLUNAS_CODIGO')
        cit_column = find_column(dat, 'COLUNAS_MUNICIPIO')
        cof_column = find_column(dat, 'COLUNAS_CONFORME')
        ped_column = find_column(dat, 'COLUNAS_PEDIDO')
        self.codigo = self.data[cod_column]
        self.pedido = self.data[ped_column]
        self.contrato = self.data[ctt_column]
        self.conformidade = self.data[cof_column]
        self.municipio = self.data[cit_column]
        self.valor_total = dat[val_column].sum()

        if dat[cof_column].nunique() != 1:
            raise throw_popup_error(ValueError(
                'A planilha contém mais de uma conformidade!'))

    def get_iss_info(self, iss: pandas.DataFrame) -> None:
        ''' Method to extract iss tax info '''
        iss_info = iss[
            (iss['MUNICÍPIO'] == self.municipio) |
            (iss['MUNICÍPIO2'] == self.municipio)]
        if iss_info.empty:
            self.municipio = self.get_correct_city_name(self.municipio)
            return
        if not len(iss_info) == 1:
            error_message = 'Foram retornados mais de um resultado!\n\n'
            error_message += f'Critério: {self.municipio}, Quantidade: {len(iss_info)}'
            raise throw_popup_error(ValueError(error_message))
        self.iss_data = iss_info.iloc[0].to_dict()
        self.municipio = self.get_correct_city_name(self.iss_data['MUNICÍPIO'])

    def get_tax_info(self, tax: pandas.DataFrame) -> None:
        ''' Method to extract tax information '''
        tax_info = tax[(tax['TOMADOR'] == self.tomador) & (tax['CODE'] == self.codigo)]
        if not len(tax_info) == 1:
            error_message = 'Foram retornados nenhum ou mais de um resultado!\n\n'
            error_message += f'Critérios: Tomador {self.tomador}, Código: {self.codigo},'
            error_message += f' Quantidade: {len(tax_info)}'
            raise throw_popup_error(ValueError(error_message))
        self.cotas_impostos = tax_info.iloc[0].to_dict()

    def get_ext_info(self, ext: pandas.DataFrame) -> None:
        ''' Method to extract complementary code '''
        ext_info = ext[ext['Municipio'] == self.municipio]
        if ext_info.empty:
            self.code_complementar = {}
            return
        if not len(ext_info) == 1:
            error_message = 'Foram retornados mais de um resultado!\n\n'
            error_message += f'Critério: {self.municipio}, Quantidade: {len(ext_info)}'
            raise throw_popup_error(ValueError(error_message))
        self.code_complementar = ext_info.iloc[0].to_dict()
