# Shoestring Rest API Service Module
## Description
The service module provides a framework for running django apps to provide a rest api. It includes functionality for receiving and sending MQTT events.

## Usage
This service module is designed to be deployed using the Shoestring Assembler.

To integrate in a solution (for context refer to [the Assembler Solution File Structure](https://github.com/DigitalShoestringSolutions/shoestring_assembler/blob/main/docs/file_structure.md)):

### Source config
* At `solution_config/source_config/<source_name>/django_apps` put your django apps (each in their own folder as is typical for django)
* At `solution_config/source_config/<source_name>/module_settings.py` you can overwrite any of the variables in `settings.py` for the base service module setup. You must also specify your apps using the `INCLUDED_APPS` variable which is appended to the base list of `INSTALLED_APPS`.
* You can add `solution_config/source_config/<source_name>/extra_requirements.txt` with additional pip requirements if needed.

### User config
* At `solution_config/user_config_templates/<source_name>/settings.py` put any user configurable settings (you can use the prompts and templating capabilities of the assembler)


### Worked Example:

`filestructure`
```
.
├── solution_config/
│   ├── source_config/
│   │   ├── <source_name>/
│   │   │   ├── django_apps/
│   │   │   │   ├── my_app_name/
│   │   │   │   │   └── ...
│   │   │   │   └── my_other_app/
│   │   │   │       └── ...
│   │   │   ├── module_settings.py    
│   │   │   └── extra_requirements.txt (optional)
│   │   └── ...
│   ├── user_config_templates/
│   │   ├── <source_name>/
│   │   │   ├── settings.py  
│   │   │   └── ...
│   │   └── ...
│   └── ...
└── ...

```

`module_settings.py`
```
INCLUDED_APPS = [
    "my_app_name",
    "my_other_app"
]
```


## Event Handler

To handle received events - add a `event_handler.py` file in the corresponding django app. (The file is auto detected in the same way that the `models.py` file is). 

The `event_handler.py` should be as follows:

```
from event_handler import Event, EventHandler
... other imports

# register handler against topic
@EventHandler.register("topic/to/use")
def handle_my_event(msg: Event):
    ... handle events

    return output_events    # List of Events
```

An `Event` is initialised as `event = Event(topic, content)` and has `event.topic` and `event.content` available for access. `event.topic` is a list of the topic segments - so `"topic/to/use"` would be represented as `["topic","to","use"]`. 