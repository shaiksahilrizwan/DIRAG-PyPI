import json
class ConfigLoader():
    """Class to handel ollama configurations via json config file"""
    def __init__(self):
        try:
            with open("dirag.json","r+") as fp:
                self.config=json.load(fp)
        except json.JSONDecodeError as e:
            self.config=None
    def get_config(self):
            """return configuration json as python dictionary"""
            return  self.config