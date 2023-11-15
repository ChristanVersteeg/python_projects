import obspython as obs
import subprocess
import os

external_process = None

def script_description():
    return "Script to launch and manage an external Python process."

def script_load(settings):
    global external_process
    # Path to your external Python script
    script_path = r'C:\Users\Christan\Desktop\python_projects\godthisisstupidbutelseillgetconfused.py'
    
    # Start the external Python script
    creation_flags = subprocess.CREATE_NO_WINDOW
    external_process = subprocess.Popen(['python', script_path], creationflags=creation_flags)
    print("External Python script started.")

def script_unload():
    global external_process
    # Terminate the external Python script
    if external_process:
        external_process.terminate()
        external_process = None
        print("External Python script terminated.")
