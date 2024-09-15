import time 
import os 
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler
import shutil

desktop_location = r'C:\Users\Abbi\Desktop'  
extension_folders = { 
#Audio
    '.aif' : r"\Users\Abbi\Desktop\Audio\aif", 
    '.wav' : r"\Users\Abbi\Desktop\Audio\wav",
#Text 
    '.txt' : r"\Users\Abbi\Desktop\Text\txt", 
    '.doc' : r"\Users\Abbi\Desktop\Text\doc",
    '.docx': r"\Users\Abbi\Desktop\Text\docx", 
    '.pdf' : r"\Users\Abbi\Desktop\Text\pdf",
    '.tex' : r"\Users\Abbi\Desktop\Text\tex", 
    '.wks' : r"\Users\Abbi\Desktop\Text\wks",
    '.wps' : r"\Users\Abbi\Desktop\Text\wps", 
    '.wpd' : r"\Users\Abbi\Desktop\Text\wpd",
#Video 
    '.3g2' : r"\Users\Abbi\Desktop\Video\3g2", 
    '.m4v' : r"\Users\Abbi\Desktop\Video\m4v",
    '.3gp' : r"\Users\Abbi\Desktop\Video\3gp", 
    '.flv' : r"\Users\Abbi\Desktop\Video\flv",
    '.mkv' : r"\Users\Abbi\Desktop\Video\mkv", 
    '.mov' : r"\Users\Abbi\Desktop\Video\mov",
    '.h264': r"\Users\Abbi\Desktop\Video\h264", 
    '.avi' : r"\Users\Abbi\Desktop\Video\avi",
#Images 
    '.jpeg' : r"C:\Users\Abbi\Desktop\Images\jpeg", 
    '.jpg'  : r"C:\Users\Abbi\Desktop\Images\jpg",
    '.svg'  : r"\Users\Abbi\Desktop\Images\svg",
    '.gif'  : r"\Users\Abbi\Desktop\Images\gif", 
    '.tiff' : r"\Users\Abbi\Desktop\Images\tiff",
    '.tif'  : r"\Users\Abbi\Desktop\Images\tif", 
    '.png'  : r"\Users\Abbi\Desktop\Images\png",
#Programming
    '.html': r"\Users\Abbi\Desktop\Programming\html",
    '.py'  : r"\Users\Abbi\Desktop\Programming\py",
#Other 
    'noname': r"\Users\Abbi\Desktop\Other",

}


# Function to move files to the appropriate folder based on the extension

def move_to_extension_folder(filename, src_folder): # moves to new folder
      
    extension = os.path.splitext(filename)[1].lower() 
    # get the files extension type 'html','py' etc so we can determine 
    # where to store it (and make sure lowercase formatted) 
    folder_destination = extension_folders.get(extension, desktop_location)
    # get the folder we want to store within 
    file_destination = os.path.join(folder_destination, filename)
    # join the file name to the path 
    copy_number = 1 # Append a number if a file with the same name exists
    
    while os.path.exists(file_destination): 
        # if this file already exists, instead of overwriting, create copy 
        # with i added to the name then extension(ex file(1).pdf,
        name, extension = os.path.splitext(filename) 
        name = name.strip()
        extension = extension.strip()
        new_name = f"{name}({copy_number}){extension}"
        # then join with the path and increm i for next time copy found
        file_destination = os.path.join(folder_destination, new_name)
        copy_number += 1

    # Move the file once we have a unique copy 
    try:
        shutil.move(os.path.join(src_folder, filename), file_destination)
    except Exception as e: # e holds type of exception raised 
        print(f'Unable to move file {filename} to {src_folder}: {e}') 
# Function to handle the initial cleanup of existing files on the desktop

def initial_cleanup(desktop_path): # handles files already on the computer 
    for filename in os.listdir(desktop_path): 
        # os.listdir returns file names and extensions only (file.py) 
        
        if os.path.isfile(file_path): 

        # os.listdir can potentially return subdirectories(subfolders) 
        # as well as files so make sure they are files first!

            print(f'File found on desktop: {filename}')
            file_path = os.path.join(desktop_path, filename)
            move_to_extension_folder(filename, desktop_path)
                # now move them 

initial_cleanup(desktop_location) # call init cleanup 


class FileHandler(FileSystemEventHandler): # handles files found 
    def on_created(self, event): 
        filename = os.path.basename(event.src_path)
   
        if os.path.isfile(filename): # make sure it is a file not folder! 
            print(f'File created: {filename}') # log message to confirm a file was detected
            move_to_extension_folder(filename, desktop_location) 
            # send file to be moved to the organized folder 
                

event_handler = FileHandler() # get an instance of the file handler  and observer
observer = Observer()
observer.schedule(event_handler, desktop_location, recursive=False) 
# go ahead and schedule the file handler to run on the desktop location with recursive to false
# (dont include subdirectories) 
observer.start() # start loop 

try:
    while True: # observer loops looking for new files with a sleep time scheduled between each look 
        # for better performance 
        time.sleep(30)

except KeyboardInterrupt: # if ctrl+c pushed observer called to stop and join waits 
    # for it finish all processes and then shuts down the script 
    # for it finish all processes and then shuts down the script 
    observer.stop()
    observer.join()
