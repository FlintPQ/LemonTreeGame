import configparser
import os


def create_config(path):
    # Create default config file in .ini format
    config = configparser.ConfigParser()

    config.add_section('AudioProcessing')
    config.set('AudioProcessing', 'sampling_rate', '44100')

    config.add_section('PianoRoll')
    config.set('PianoRoll', 'START_OCTAVE', '4')
    config.set('PianoRoll', 'get_lower', 'scrollup')
    config.set('PianoRoll', 'get_higher', 'scrolldown')


    with open(path, "w") as config_file:
        config.write(config_file)

# ----------------------------------------------------------------


def get_config(path):
    # Create config obj
    if not os.path.exists('config.ini'):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    return config


PROJ_CONFIG = get_config('config.ini')

