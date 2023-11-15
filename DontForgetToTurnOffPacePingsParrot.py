import obspython as obs
import subprocess
import json
import os

external_process = None
script_path = ""

def script_description():
    return "A tool that creates a window with text upon a hotkey press. This window will always on top of everything. Made by Wumpie, for Parrot <3."

def script_load(settings):
    global external_process
    
    json_file = os.path.join(os.environ['LOCALAPPDATA'], 'DontForgetToTurnOffPacePingsParrot', 'label_settings.json')
    if not os.path.exists(os.path.dirname(json_file)): os.makedirs(os.path.dirname(json_file))
    if not os.path.exists(json_file): open(json_file, 'w')
    
    creation_flags = subprocess.CREATE_NO_WINDOW
    external_process = subprocess.Popen(['python', script_path], creationflags=creation_flags)
    print("External Python script started.")
    
def script_properties():
    props = obs.obs_properties_create()
    
    obs.obs_properties_add_path(props, "script_path", "Python Script Path", obs.OBS_PATH_FILE, "Python (*.py)", '')
    return props

def script_update(settings):
    json_file = os.path.join(os.environ['LOCALAPPDATA'], 'DontForgetToTurnOffPacePingsParrot', 'label_settings.json')
    with open(json_file, 'w') as file:
        json.dump({"script_path": script_path}, file)

def script_unload():
    global external_process
    if external_process:
        external_process.terminate()
        external_process = None
        print("External Python script terminated.")
