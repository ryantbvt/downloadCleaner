import shutil
from datetime import date
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from extensions import extension_paths

def prevent_override(source: Path, destination_path: Path):
    # increment file name by number if file already exists in the folder
    if Path(destination_path / source.name).exists():
        i = 0

        while True:
            i += 1
            new_name = destination_path / f'{source.stem}_{i}{source.suffix}'

            if not new_name.exists():
                return new_name

    else:
        return destination_path / source.name

def add_date(path: Path):
    # sort files by date
    # if folder by date doesn't exist, then create a new folder

    date_path = path / f'{date.today()}.year' / f'{date.today().month:02d}'
    date_path.mkdir(parents=True, exist_ok=True)

    return date_path

class EventHandler(FileSystemEventHandler):
    # initialize
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    # move file