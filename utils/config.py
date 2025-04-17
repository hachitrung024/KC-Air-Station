import configparser

_config = configparser.ConfigParser()
_config.read("config/settings.ini")

def get_lora_config():
    return _config["lora"]

def get_uart_config():
    return _config["uart"]

def get_target_config():
    return _config["target"]