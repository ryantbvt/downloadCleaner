from pathlib import Path
from time import sleep
from watchdog.observers import Observer
from EventHandler import MyHandler

# run the actual code
if __name__ == '__main__':
    # set Paths
    watch_path = Path.home() / 'Downloads'
    destination_root = Path.home() / 'Downloads/sorted'
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