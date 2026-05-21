''' Module to check multiples instances and kill residual processes '''
from helpers.executor import execute
from helpers.dialogator import show_popup_error
from helpers.constants import DEV_ENV

class CouldNotDetermineInstances(Exception):
    ''' Exception to indicate that number of instances cold not be defined '''

class MultiplesInstancesException(Exception):
    ''' Exception to indicate multiples instances running '''

def check_multiple_instances(imagename: str) -> None:
    ''' Function to check running processes and return they PID '''
    result = execute('tasklist', '/FI', '"' + 'IMAGENAME', 'eq', imagename + '"')
    if not result or result.startswith('INFO'):
        error_message = f'Instances of {imagename} cannot be defined!'
        show_popup_error(error_message)
        raise CouldNotDetermineInstances(error_message)
    if result.count(imagename) > 1:
        error_message = f'There is more than one instance of {imagename}!'
        show_popup_error(error_message)
        raise MultiplesInstancesException(error_message)

def kill_residual_process(imagename: str) -> None:
    ''' Function to kill residual process '''
    execute('taskkill', '/F', '/IM', imagename)

def instance_checker() -> None:
    ''' Main function to check if program is already running and kill residual programs '''
    #(check_multiple_instances(APPNAME + '.py')
    #    if DEV_ENV else
    #check_multiple_instances(APPNAME + '.exe'))
    if not DEV_ENV:
        kill_residual_process('chromedriver.exe')
        kill_residual_process('chrome.exe')
