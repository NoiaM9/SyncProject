## Folder Synchronization Tool
This Folder Synchronization Tool is a Python script that allows users to synchronize the contents of two folders, ensuring that they remain identical. 
It provides a convenient way to maintain an up-to-date replica of a source folder by automatically detecting changes and applying them to the replica.


# Features:
Command-Line Interface (CLI): Users can run the script from the command line, providing the paths to the source and replica folders, along with the synchronization interval.

Graphical User Interface (GUI): The script also includes a simple GUI for users who prefer a visual interface. The GUI allows users to enter the folder paths and synchronization interval easily.
*GUI is still under work, will need an update*

Periodic Synchronization: The script uses the schedule library to schedule periodic synchronization based on the specified interval. 
This ensures that changes in the source folder are regularly applied to the replica.

Logging: Detailed logs are generated during synchronization, providing information about file additions, updates, and deletions. Logs are written to a file for reference.

# How to Use:
Command-Line Mode:

Copy code:
python sync_folders.py -s [source_folder] -c [replica_folder] -t [sync_interval]
Replace [source_folder] with the path to the source folder.
Replace [replica_folder] with the path to the replica folder.
Replace [sync_interval] with the synchronization interval in seconds.

# Graphical User Interface (GUI):
Run the script without any command-line arguments to launch the GUI.
Enter the paths to the source and replica folders, and specify the synchronization interval.
Click the "Sync Now" button to initiate synchronization.

# Dependencies:
Python 3.x
schedule library (Install using pip install schedule)

# Contributions:
Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

# License:
This project is licensed under the MIT License.
