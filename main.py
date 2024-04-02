import os
import hashlib
import logging
import argparse
import shutil
import schedule
import time
import tkinter as tk
from tkinter import ttk
import inspect


# Function to create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Folder Synchronization")

    # Function to handle synchronization button click
    def sync_folders():
        source_path = source_entry.get()
        copy_path = copy_entry.get()
        time_period = int(time_entry.get())

        # Log the paths and interval
        logging.info(f"Source folder: {source_path}")
        logging.info(f"Replica folder: {copy_path}")
        logging.info(f"Sync interval: {time_period} seconds")

        # Call the folder synchronization function
        folder_updater(source_path, copy_path)

    # Source folder entry
    source_label = ttk.Label(root, text="Source Folder:")
    source_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    source_entry = ttk.Entry(root, width=50)
    source_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)  # Expand entry horizontally
  # Expand entry horizontally

    # Replica folder entry
    copy_label = ttk.Label(root, text="Replica Folder:")
    copy_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    copy_entry = ttk.Entry(root, width=50)
    copy_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)  # Expand entry horizontally

    # Time interval entry
    time_label = ttk.Label(root, text="Sync Interval (seconds):")
    time_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    time_entry = ttk.Entry(root, width=10)
    time_entry.grid(row=2, column=1, padx=5, pady=5)

    # Synchronize button
    sync_button = ttk.Button(root, text="Sync Now", command=sync_folders)
    sync_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    # Configure row and column weights to make them expandable
    root.rowconfigure((0, 1, 2), weight=1)
    root.columnconfigure((0, 1), weight=1)

    root.mainloop()



# Function to perform folder synchronization
def folder_updater(source_path, copy_path):
    # Your synchronization logic here
    logging.info("Synchronization started.")
    # Example: print source_path, copy_path


# Parser to obtain the arguments from the command line
parser = argparse.ArgumentParser(description='Configuration arguments for folder synchronization processor')
# Arguments with the path to source folder
parser.add_argument('-s', '--source', required=False, type=str, help=r"C:\Users\Cris\Desktop\SyncProject\source_folder")
# Arguments with the path to copy folder
parser.add_argument('-c', '--copy', required=False, type=str, help=r"C:\Users\Cris\Desktop\SyncProject\replica_folder")
# Arguments with the time (seconds)
parser.add_argument('-t', '--time', required=False, help='5', type=int)

# Get the arguments from the parser
arguments = parser.parse_args()

# Check if the script is run without any command-line arguments (indicating GUI mode)
if not any(vars(arguments).values()):
    create_gui()  # Start GUI
else:
    # Extract values from command-line arguments
    source_path = arguments.source
    copy_path = arguments.copy
    time_period = arguments.time

    # Perform folder synchronization
    folder_updater(source_path, copy_path)



# Function for creating logger for log file & console
def get_logger():
    #Refers to function name
    logger_name = inspect.stack()[1][3]
    logger_ini = logging.getLogger(logger_name)
    fileHandler = logging.FileHandler('logfile.log')
    formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s')
    fileHandler.setFormatter(formatter)
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger_ini.addHandler(fileHandler)
    logger_ini.setLevel(logging.INFO)
    return logger_ini


# Function that return the sha256 hash digest of a file parameter
def generate_hash(file):
    with open(file, 'rb') as f:
        content = f.read()
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()


# Function to get the hashes of contents from a folder on a dictionary
def folder_hasher(folder_path):
    # Dictionary for path,hash
    folder_hash = {}

    # Start going over the source folder having path, subdir and files
    for path, subdir, files in os.walk(folder_path):

        # Subdirectories inside the folder
        for s in subdir:
            # For folders inside the folder they will be inside the dictionary with key relative path and value "folder"
            relative_dir = os.path.relpath(path, folder_path)
            relative_folder = os.path.join(relative_dir, s)
            if ".\\" in relative_folder:
                relative_folder = relative_folder.replace('.\\', '')
            folder_hash[relative_folder] = "folder"

        # Files inside every folder
        for f in files:
            # The files will be represented with key=relative_path and value=hash
            rel_dir = os.path.relpath(path, folder_path)
            rel_file = os.path.join(rel_dir, f)
            if ".\\" in rel_file:
                rel_file = rel_file.replace('.\\', '\\')
            if '\\\\' in rel_file:
                rel_file = rel_file.replace('\\\\', '\\')
            folder_hash[rel_file] = generate_hash(os.path.join(path, f))

    return folder_hash


# Declare the logger outside the function so the logs are not repeting on logfile
logger = get_logger()


# Function to compare two folders content according to their hash digest
def folder_updater():
    # Obtain the hashes of both folders
    source_files = folder_hasher(source_path)
    copy_files = folder_hasher(copy_path)

    # Loop through the files (paths) on the source folder
    for f in source_files.items():

        # If it is a folder
        if f[1] == "folder":
            # Check if the folder is contained in the copy folder add it to it
            if f[0] not in copy_files:
                os.makedirs(copy_path + '\\' + f[0])
                logger.info(' Added folder: ' + f[0])

        # File not in copy according to name, the file is not in copy, or it was renamed
        if f[0] not in copy_files and f[1] != 'folder':
            shutil.copy(source_path+'\\'+f[0], copy_path+'\\'+f[0])
            logger.info(' Added file: ' + f[0])

        # Same name but different hash, not updated
        elif f[0] in copy_files and f[1] != copy_files.get(f[0]) and f[1] != 'folder':
            shutil.copy(source_path+'\\'+f[0], copy_path+'\\'+f[0])
            logger.info(' Updated file: ' + f[0])

    # Put into the deleted set the files that are only on copy folder
    copy_files_updated = folder_hasher(copy_path)
    deleted_files = find_deleted_items(source_files, copy_files_updated)

    # For the hash of the files that are only on copy delete them
    for d in copy_files_updated.items():
        if d in deleted_files and d[1] != 'folder':
            os.remove(copy_path+'\\'+d[0])
            logger.info(' Deleted file: ' + d[0])
    # Perform the same for deleting folders in reversed order
    for d in reversed(copy_files_updated.items()):
        if d in deleted_files and d[1] == 'folder':
            os.rmdir(copy_path+'\\'+d[0])
            logger.info(' Deleted folder: ' + d[0])


# Function to find the files that were deleted from source
def find_deleted_items(source, copy):

    deleted_set = set()
    source_set = set(source.items())
    copy_set = set(copy.items())
    deleted_items = copy_set - source_set
    for d in deleted_items:
        deleted_set.add(d)

    return deleted_set


# Schedule for the function folder_updater() to run periodically based on time_period
schedule.every(time_period).seconds.do(folder_updater)

# Time between executions
while True:
    schedule.run_pending()
    time.sleep(5)