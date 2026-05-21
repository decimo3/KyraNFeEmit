''' Module to hold constants and configurations values '''
import os
import sys
from dotenv import dotenv_values
from helpers.normalizer import norm_txt

# Set what environment it is
DEV_ENV = not getattr(sys, 'frozen', False)

# Define App name by file name
APPNAME = (
    sys.argv[0].split('\\')[-1].replace('.exe','')
    if not DEV_ENV else
    sys.argv[0].split('\\')[-1].replace('.py','')
)

# Set variable that define the folder that it's executed
BASE_FOLDER = (
    os.path.dirname(sys.executable)
    if not DEV_ENV else
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Load configuration file
configuration_filepath = os.path.join(BASE_FOLDER, APPNAME + '.conf')
CONFIGS = dotenv_values(configuration_filepath)

# Load webelements path file
webelements_filepath = os.path.join(BASE_FOLDER, APPNAME + '.path')
WAYPATH = dotenv_values(webelements_filepath)

WAITSEC = { 'AGORA': 0, 'CURTO': 3, 'MEDIO': 5, 'LONGO': 10, 'TOTAL': 15 }

VERDADEIROS = ['verdadeiro', 'true', 'sim', 'yes']

TEXT_TOLERANCE = 3

VALUE_TOLERANCE = 0.01

CITIES = [
    'Angra dos Reis', 'Aperibé', 'Araruama', 'Areal', 'Armação dos Búzios',
    'Arraial do Cabo', 'Barra do Piraí', 'Barra Mansa', 'Belford Roxo',
    'Bom Jardim', 'Bom Jesus do Itabapoana', 'Cabo Frio', 'Cachoeiras de Macacu',
    'Cambuci', 'Campos dos Goytacazes', 'Cantagalo', 'Carapebus', 'Cardoso Moreira',
    'Carmo', 'Casimiro de Abreu', 'Comendador Levy Gasparian', 'Conceição de Macabu',
    'Cordeiro', 'Duas Barras', 'Duque de Caxias', 'Engenheiro Paulo de Frontin',
    'Guapimirim', 'Iguaba Grande', 'Itaboraí', 'Itaguaí', 'Italva', 'Itaocara',
    'Itaperuna', 'Itatiaia', 'Japeri', 'Laje do Muriaé', 'Macaé', 'Macuco', 'Magé',
    'Mangaratiba', 'Maricá', 'Mendes', 'Mesquita', 'Miguel Pereira', 'Miracema',
    'Natividade', 'Nilópolis', 'Niterói', 'Nova Friburgo', 'Nova Iguaçu', 'Paracambi',
    'Paraíba do Sul', 'Paraty', 'Paty do Alferes', 'Petrópolis', 'Pinheiral', 'Piraí',
    'Porciúncula', 'Porto Real', 'Quatis', 'Queimados', 'Quissamã', 'Resende',
    'Rio Bonito', 'Rio Claro', 'Rio das Flores', 'Rio das Ostras', 'Rio de Janeiro',
    'Santa Maria Madalena', 'Santo Antônio de Pádua', 'São Fidélis',
    'São Francisco de Itabapoana', 'São Gonçalo', 'São João da Barra', 'São João de Meriti',
    'São José de Ubá', 'São José do Vale do Rio Preto', 'São Pedro da Aldeia',
    'São Sebastião do Alto', 'Sapucaia', 'Saquarema', 'Seropédica', 'Silva Jardim',
    'Sumidouro', 'Tanguá', 'Teresópolis', 'Trajano de Moraes', 'Três Rios', 'Valença',
    'Varre-Sai', 'Vassouras', 'Volta Redonda'
]

CITIES_RAW = [norm_txt(x) for x in CITIES]
