from datetime import date
from time import sleep
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from extensions import extension_paths

# all code in one file

def prevent_override(source: Path, destination_path: Path):
    '''
    helper method to prevent files from overriding

    :param Path source: source of the file to be move
    :param Path destination_path: path to the destination directory
    '''
    if Path(destination_path / source.name).exists():
        # initialize increment variable
        i = 0

        while True:
            i += 1

            new_name = destination_path / f'{source.stem}_{i}{source.suffix}'

            if not new_name.exists():
                return new_name

    else:
        return destination_path /source.name

def date_path(path: Path):
    '''
    helper method
    create/add to year/month folders within the destination folder

    param Path path: set destination root to append subdirectories based on date
    '''

    date_path = path / f'{date.today().year}' / f'{date.today().month:02d}'
    date_path.mkdir(parents=True, exist_ok=True)

    return date_path

# class from watchdog (looks for changes in a folder)
class MyHandler(FileSystemEventHandler):
    # initialize
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    # moving files to destination
    def on_modified(self, event):
        # iterdir: path points to a directory, yield path objects of the directory contents
        for child in self.watch_path.iterdir():
            if child.is_file() and child.suffix.lower() in extension_paths:
                destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                destination_path = date_path(path=destination_path)
                destination_path = prevent_override(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)

# run the actual code

# set Paths
watch_path = Path.home() / 'Downloads'
destination_root = Path.home() / '/Downloads/sorted'
event_handler = MyHandler(watch_path=watch_path, destination_root=destination_root)

# initialize the observer
observer = Observer()
observer.schedule(event_handler, f'{watch_path}', recursive=True)
observer.start()

try:
    while True:
        sleep(60)
except KeyboardInterrupt:
    observer.stop()
observer.join()