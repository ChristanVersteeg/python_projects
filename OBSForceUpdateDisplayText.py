import obspython as obs

source_name = "display"
file_path = ""
check_interval_ms = 100

def update_text_source():
    global file_path
    with open(file_path, 'r') as file:
        file_contents = file.read()
            
    source = obs.obs_get_source_by_name(source_name)
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", file_contents)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)

def script_update(settings):
    global file_path
    file_path = obs.obs_data_get_string(settings, "file_path")

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "file_path", "File Path", obs.OBS_PATH_FILE, "Text files (*.txt)", None)
    return props

def script_load(settings):
    script_update(settings)
    obs.timer_add(update_text_source, check_interval_ms)

def script_unload():
    obs.timer_remove(update_text_source)