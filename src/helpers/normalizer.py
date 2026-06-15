''' Module to normalize strings '''
import unicodedata

def norm_txt(text: str) -> str:
    ''' Function to normalize strings '''
    text = text.strip().casefold()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(
        c for c in text
        if unicodedata.category(c) != 'Mn'
    )
    return text

def norm_float(number: float | int) -> str:
    ''' Function to normalize float '''
    return str(
        f'{number:,.2f}'
            .replace(',', '_')
            .replace('.', ',')
            .replace('_', '.')
        )

def norm_money(value: str) -> float:
    ''' Function to convert brazilian monetary string to float '''
    return float(
        value
            .replace('R$', '')
            .replace('%', '')
            .replace('.', '')
            .replace(',', '.')
            .strip()
        )
