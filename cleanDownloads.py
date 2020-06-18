import os
from datetime import date
from extensions import extension_paths

root_path = 'C:/Users/Ryan Bui/Downloads/'

file_list = os.listdir(root_path)

'''
helper method to move file to a month and date system
creating new folders for new years and months

Example: C:/Users/Ryan Bui/Downloads/sorted/text_pdf/2020/06

param path str: the path that the file is going to
'''
def date_path(path: str):

    # grab year and month
    year = f'{date.today().year}'
    month = f'{date.today().month:02d}'

    date_path = 'path' + '/' + year + '/' + month
    # fix this line v
    date_path.mkdir(parents=True, exist_ok=True)

    return date_path

# iterate through the list of files
for i in file_list:
    file_name = i
    # ignore these files
    if file_name != 'sorted' and file_name != 'zAllFolderDumps':
        # split file name into extension and file name to sort
        file_name_extension = file_name.split('.')
        file_name_no_extension = file_name_extension[0]
        file_extension = file_name_extension[1]

        try:
            # checks if current file is in the destination folder
            file_exists = os.path.isfile(extension_paths[file_extension] + '/' + file_name_no_extension + '.' + file_extension)

            # j is for if a file exists
            j = 0
            '''
            if the file does exist,
            we want to add a number at the end so
            that it doesn't override the current file
            '''
            while file_exists:
                j += 1
                temp = None
                temp = file_name_no_extension + str(j)
                #need to redo file_exists to prevent infinite loop
                file_exists = os.path.isfile(extension_paths[file_extension] + '/' + temp + '.' + file_extension)

            # only do if while loop did something
            if j > 0:
                file_name_no_extension = file_name_no_extension + str(j)

            # rename / update file name from the root
            source_name = root_path + file_name
            destination_name = date_path(extension_paths[file_extension]) + '/' + file_name_no_extension +'.' + file_extension

            # move the file
            os.rename(source_name, destination_name)

        except Exception:
            print(file_name)