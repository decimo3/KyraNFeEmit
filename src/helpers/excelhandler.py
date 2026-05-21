''' Module to get dataframe from Excel file '''
import os
import xlrd
import pandas
from helpers.constants import CONFIGS
from helpers.dialogator import show_popup_error, show_popup_debug, show_popup_info

class WorksheetNotFoundException(Exception):
    ''' Exception to inform that worksheet was not found '''

def get_dataframe_from_excel(file_path: str, skipt_rows: int = 0) -> pandas.DataFrame:
    ''' Function to get DataFrame from Excel file '''
    if not os.path.exists(file_path):
        error_message = f'A arquivo {file_path} não está acessível!'
        show_popup_error(error_message)
        raise FileNotFoundError(error_message)
    show_popup_info(f'Obtendo informações do arquivo {file_path}...', False)
    # Use xlrd to read legacy .xls files
    workbook = xlrd.open_workbook(file_path)
    worksheet = workbook.sheet_by_index(0)
    rows_gen = iter(worksheet.get_rows())
    skipped = 0
    while skipped < skipt_rows:
        next(rows_gen)
        skipped += 1
    header_row = next(rows_gen)
    head = [cell.value for cell in header_row]
    # Body: consume remaining rows from generator
    body = [[cell.value for cell in row] for row in rows_gen]
    dataframe = pandas.DataFrame(body, columns=head)
    show_popup_debug('Planilha carregada em memória com sucesso!')
    return dataframe

def find_column(df: pandas.DataFrame, column_list_key: str) -> str:
    ''' Function to resolve correct column name from column list '''
    possible_names = str(CONFIGS.get(column_list_key, '')).split(',')
    if not possible_names:
        raise ValueError(f'Não foi encontrada a configuração {column_list_key}!')
    for column in df.columns:
        if column in possible_names:
            return column
    raise ValueError('A coluna não foi encontrada pelos critérios!')
