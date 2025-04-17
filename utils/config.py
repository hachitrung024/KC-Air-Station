import configparser

def get_mode():
    config = configparser.ConfigParser()
    config.read("config/settings.ini")
    return config["system"].get("mode", "gateway")
