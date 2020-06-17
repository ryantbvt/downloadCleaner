from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os
import json
import shutil
from extensions import extension_paths

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            i = 1
            if filename != 'sorting' and filename != 'zAllFolderDumps':
                try:
                    extension = str(os.path.splitext(folder_to_track + '/' + filename)[1])
                    new_name = filename
                    file_exists = os.path.isfile(extension_paths[extension] + '/' + new_name)
                    while file_exists:
                        i += 1
                        new_name = os.path.splitext(folder_to_track + '/' + new_name)[0] + str(i) + os.path.splitext(folder_to_track + '/' + filename)[1]
                        new_name = new_name.split('/')[4]
                        file_exists = os.path.isfile(folder_destination + '/' + new_name)
                    src = folder_to_track + '/' + filename
                    new_name = extension_paths[extension] + '/' + new_name
                    os.rename(src, new_name)
                except Exception:
                    print(filename)


folder_to_track = 'C:/Users/Ryan Bui/Downloads'
folder_destination = 'C:/Users/Ryan Bui/Downloads/sorted'
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()