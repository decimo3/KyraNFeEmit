''' Module to wrap calls to external programs '''
import subprocess
from helpers.dialogator import show_popup_error, show_popup_debug

def execute(*args: str) -> str:
    ''' Function to execute and return code and stdout '''
    if not args:
        error_message = 'Não foram passados argumentos para a função!'
        show_popup_error(error_message)
        raise ValueError(error_message)
    command = ' '.join(args)
    try:
        result = subprocess.run(
            args=command,
            capture_output=True,
            text=True,
            shell=False,
            check=True
            )
        show_popup_debug(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        show_popup_error(e.stderr or f'O programa {args[0]} retornou com erro desconhecido!')
        return ''
    except FileNotFoundError as e:
        show_popup_error(e.strerror or f'O sistema não pode encontrar o programa {args[0]}!')
        return ''
