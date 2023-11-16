import obspython as obs
import subprocess
import json
import os

external_process = None
json_file = os.path.join(os.environ['LOCALAPPDATA'], 'DontForgetToTurnOffPacePingsParrot', 'label_settings.json')

def script_description():
    return "A tool that creates a window with text upon a hotkey press. This window will always be on top of everything. Made by Wumpie, for Parrot <3."

def script_load(settings):
    global external_process

    if not os.path.exists(os.path.dirname(json_file)): os.makedirs(os.path.dirname(json_file))
    if not os.path.exists(json_file): open(json_file, 'w')

    creation_flags = subprocess.CREATE_NO_WINDOW
    external_process = subprocess.Popen(['python', obs.obs_data_get_string(settings, "script_path")], creationflags=creation_flags)
    print("External Python script started.")

def script_properties():
    props = obs.obs_properties_create()

    fg_group = obs.obs_properties_create()
    obs.obs_properties_add_path(fg_group, "script_path", "Python Script Path", obs.OBS_PATH_FILE, "Python (*.py)", '')
    obs.obs_properties_add_text(fg_group, "warn_text", "Warning Text", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_color(fg_group, "fg_color", "Text Color")
    obs.obs_properties_add_int(fg_group, "font_size", "Font Size", 1, 100, 1)
    obs.obs_properties_add_group(props, "foreground_group", "Foreground Settings", obs.OBS_GROUP_NORMAL, fg_group)
     
    bg_group = obs.obs_properties_create()
    obs.obs_properties_add_color(bg_group, "bg_color", "Background Color")
    obs.obs_properties_add_int(bg_group, "border_size", "Border Size", 0, 10, 1)
    obs.obs_properties_add_list(bg_group, "relief_type", "Relief Type", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_group(props, "background_group", "Background Settings", obs.OBS_GROUP_NORMAL, bg_group)
    
    misc_group = obs.obs_properties_create()
    obs.obs_properties_add_float_slider(misc_group, "alpha", "Alpha", 0.0, 1.0, 0.01)
    obs.obs_properties_add_text(misc_group, "hotkey", "Hotkey", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_group(props, "miscellaneous_group", "Miscellaneous Settings", obs.OBS_GROUP_NORMAL, misc_group)
    

    relief_property = obs.obs_properties_get(props, "relief_type")
    obs.obs_property_list_add_string(relief_property, "Flat", "flat")
    obs.obs_property_list_add_string(relief_property, "Ridge", "ridge")
    obs.obs_property_list_add_string(relief_property, "Solid", "solid")
    obs.obs_property_list_add_string(relief_property, "Sunken", "sunken")
    obs.obs_property_list_add_string(relief_property, "Raised", "raised")
    obs.obs_property_list_add_string(relief_property, "Groove", "groove")

    return props

def script_update(settings):

    settings_data = {
        "script_path": obs.obs_data_get_string(settings, "script_path"),
        "warn_text": obs.obs_data_get_string(settings, "warn_text"),
        "fg_color": obs.obs_data_get_int(settings, "fg_color"),
        "bg_color": obs.obs_data_get_int(settings, "bg_color"),
        "font_size": obs.obs_data_get_int(settings, "font_size"),
        "border_size": obs.obs_data_get_int(settings, "border_size"),
        "relief_type": obs.obs_data_get_string(settings, "relief_type"),
        "alpha": obs.obs_data_get_double(settings, "alpha"),
        "hotkey": obs.obs_data_get_string(settings, "hotkey")
    }

    with open(json_file, 'w') as file:
        json.dump(settings_data, file)

def script_unload():
    global external_process
    if external_process:
        external_process.terminate()
        external_process = None
        print("External Python script terminated.")
