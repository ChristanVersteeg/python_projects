import obspython as obs
import subprocess
import json
import os

external_process = None
json_file = os.path.join(os.environ['LOCALAPPDATA'], 'DontForgetToTurnOffPacePingsParrot', 'label_settings.json')

def run_script(run, settings = None):
    global external_process
    if run:
        creation_flags = subprocess.CREATE_NO_WINDOW
        external_process = subprocess.Popen(['python', obs.obs_data_get_string(settings, "script_path")], creationflags=creation_flags)
        print("External Python script started.")
    elif external_process:
        external_process.terminate()
        external_process = None
        print("External Python script terminated.")

def script_description():
    return "A tool that creates a window with text upon a hotkey press. This window will always be on top of everything. Made by Wumpie, for Parrot <3."

def script_load(settings):

    if not os.path.exists(os.path.dirname(json_file)): os.makedirs(os.path.dirname(json_file))
    if not os.path.exists(json_file): open(json_file, 'w')
    
    run_script(True, settings)

def script_properties():
    props = obs.obs_properties_create()

    fg_group = obs.obs_properties_create()
    obs.obs_properties_add_path(fg_group, "script_path", "Python Script Path", obs.OBS_PATH_FILE, "Python (*.py)", '')
    obs.obs_properties_add_text(fg_group, "text", "Text", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_font(fg_group, "font", "Font")
    obs.obs_properties_add_color(fg_group, "fg_color", "Text Color")
    obs.obs_properties_add_group(props, "foreground_group", "Foreground Settings", obs.OBS_GROUP_NORMAL, fg_group)
     
    bg_group = obs.obs_properties_create()
    obs.obs_properties_add_color(bg_group, "bg_color", "Background Color")
    obs.obs_properties_add_int(bg_group, "border_size", "Border Size", 0, 10, 1)
    obs.obs_properties_add_list(bg_group, "relief_type", "Relief Type", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_group(props, "background_group", "Background Settings", obs.OBS_GROUP_NORMAL, bg_group)
    
    misc_group = obs.obs_properties_create()
    obs.obs_properties_add_float_slider(misc_group, "alpha", "Alpha", 0.0, 1.0, 0.01)
    obs.obs_properties_add_list(misc_group, "hotkey", "Hotkey", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_properties_add_group(props, "miscellaneous_group", "Miscellaneous Settings", obs.OBS_GROUP_NORMAL, misc_group)
    
    
    def add_prop_to_list(prop, list):
        for item in list:
            item_display = item.capitalize()
            obs.obs_property_list_add_string(prop, item_display, item)
        
    reliefs = ["flat", "ridge", "solid", "sunken", "raised", "groove"]
    relief_property = obs.obs_properties_get(props, "relief_type")
    add_prop_to_list(relief_property, reliefs)

    keys = [
        "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]",
        "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'",
        "z", "x", "c", "v", "b", "n", "m", ",", ".", "/"
    ]
    hotkey_property = obs.obs_properties_get(props, "hotkey")
    add_prop_to_list(hotkey_property, keys)
    
    return props

def script_update(settings):

    def integer_to_hex_color(integer):
        blue = (integer >> 16) & 0xFF  
        green = (integer >> 8) & 0xFF  
        red = integer & 0xFF      

        return "#{:02x}{:02x}{:02x}".format(red, green, blue)


    font_data = obs.obs_data_get_obj(settings, "font")
    font_style = obs.obs_data_get_string(font_data, "style")
    
    def if_matches_return(matches, returns, default):
        if any(word in font_style.lower() for word in matches):
            returns = returns
        else: returns = default

        return returns
    
    settings_data = {
        "text": obs.obs_data_get_string(settings, "text"),
        "fg_color": integer_to_hex_color(obs.obs_data_get_int(settings, 'fg_color')),
        "bg_color": integer_to_hex_color(obs.obs_data_get_int(settings, 'bg_color')),
        "font_size": obs.obs_data_get_int(font_data, "size"),
        'font_family': obs.obs_data_get_string(font_data, "face"),
        'font_weight': if_matches_return(["bold", "vet"], "bold", "normal"),
        'font_slant': if_matches_return(["italic", "schuin", "cursief"], "italic", "roman"),
        "border_size": obs.obs_data_get_int(settings, "border_size"),
        "relief_type": obs.obs_data_get_string(settings, "relief_type"),
        "alpha": obs.obs_data_get_double(settings, "alpha"),
        "hotkey": obs.obs_data_get_string(settings, "hotkey")
    }

    with open(json_file, 'w') as file:
        json.dump(settings_data, file)
    
    
    if font_data:
        face = obs.obs_data_get_string(font_data, "face")
        font_style = obs.obs_data_get_string(font_data, "style")
        size = obs.obs_data_get_int(font_data, "size")
        flags = obs.obs_data_get_int(font_data, "flags") 

        obs.obs_data_release(font_data)

def script_unload():
    run_script(False)