''' Module to wrap logger, console and interface messages '''
import os
import sys
import logging
import datetime
from logging import FileHandler
from tkinter import messagebox
from helpers.constants import BASE_FOLDER, APPNAME, DEV_ENV

logger = logging.getLogger(APPNAME)
logspath = os.path.join(BASE_FOLDER, 'logs')
if not os.path.exists(logspath):
    os.mkdir(logspath)
logsfile = APPNAME + '_' + datetime.datetime.now().strftime('%Y%m%d') + '.log'
logspath = os.path.join(logspath, logsfile)
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.DEBUG if DEV_ENV else logging.INFO,
    handlers = [
        logging.StreamHandler(sys.stdout),
        FileHandler(filename=logspath, mode='a', encoding='utf-8'),
    ]
)

def throw_popup_error(erro: BaseException, throw: bool = True) -> BaseException:
    ''' Function to show messages and throw erros '''
    logger.error(erro.args)
    if throw:
        messagebox.showerror('Erro!', message=str(erro.args))
    return erro

def show_popup_error(message: str, show: bool = True) -> None:
    ''' Function to show a popup message about erros '''
    logger.error(message)
    if show:
        messagebox.showerror('Erro!', message=message)

def show_popup_info(message: str, show: bool = True) -> None:
    ''' Function to show a popup message about info '''
    logger.info(message)
    if show:
        messagebox.showinfo('Info!', message=message)

def show_popup_debug(message: str) -> None:
    ''' Function to show a popup message about debug '''
    logger.debug(message)
    if DEV_ENV:
        messagebox.showinfo('Debug!', message=message)
