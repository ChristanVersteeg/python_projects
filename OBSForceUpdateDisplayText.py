import obspython as obs

source_name = "display"  
file_path = "C:/Users/Christan/Desktop/python_projects/display.txt" 
check_interval_ms = 100

def update_text_source():
    with open(file_path, 'r') as file:
        file_contents = file.read()
            
    source = obs.obs_get_source_by_name(source_name)
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", file_contents)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)

def script_load(settings):
    obs.timer_add(update_text_source, check_interval_ms)

def script_unload():
    obs.timer_remove(update_text_source)