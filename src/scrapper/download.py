''' Module to help to wait to download complete and move file '''
from pathlib import Path
from time import monotonic, sleep
from typing import Optional
from helpers.dialogator import show_popup_info, throw_popup_error

CHECK_INTERVAL = 0.2
DEFAULT_TIMEOUT = 30
TEMP_EXTENSIONS = {'.tmp', '.crdownload'}


def is_file_ready(file_path: Path) -> bool:
    ''' Returns True when the file is no longer being written '''
    try:
        initial_size = file_path.stat().st_size
        with open(file_path, 'ab'):
            pass
        sleep(CHECK_INTERVAL)
        return file_path.stat().st_size == initial_size
    except OSError:
        return False

def wait_until_file_is_ready(
    file_path: Path,
    timeout_at: float,
    ) -> None:
    ''' Wait until file becomes stable and writable '''
    while monotonic() < timeout_at:
        if file_path.exists() and is_file_ready(file_path):
            return

        sleep(CHECK_INTERVAL)

    raise throw_popup_error(TimeoutError(
        f'File "{file_path}" is still being written.'
    ))

def get_latest_download(
    directory: Path,
    after_timestamp: float,
    ) -> Optional[Path]:
    ''' Return the newest valid downloaded file '''
    latest_file: Optional[Path] = None
    latest_mtime = 0.0

    for file_path in directory.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix in TEMP_EXTENSIONS:
            continue

        try:
            stat = file_path.stat()
        except OSError:
            continue

        if stat.st_mtime <= after_timestamp:
            continue

        if stat.st_mtime > latest_mtime:
            latest_mtime = stat.st_mtime
            latest_file = file_path

    return latest_file

def download_file(
    download_dir: str | Path,
    target_dir: str | Path,
    timeout_seconds: int = DEFAULT_TIMEOUT,
) -> str:
    ''' waits until the file is fully downloaded '''
    target_dir = Path(target_dir)
    download_dir = Path(download_dir)

    started_at = monotonic()
    timeout_at = started_at + timeout_seconds

    show_popup_info('Aguardando o download...', False)

    while monotonic() < timeout_at:
        file_path = get_latest_download(download_dir, started_at)

        if file_path:
            wait_until_file_is_ready(file_path, timeout_at)

            new_file_path = target_dir / file_path.name
            file_path.replace(new_file_path)
            show_popup_info(f'Download salvo na pasta: {new_file_path}', False)
            return str(file_path)
        sleep(CHECK_INTERVAL)

    raise throw_popup_error(FileNotFoundError(
        'Download file not found within timeout!'))
