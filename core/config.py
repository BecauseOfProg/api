import json


class Config:

    def __init__(self):
        self.config_path = 'config.json'
        self.config = json.loads(open(self.config_path, 'r').read())

    def get(self, key, subkey=''):
        return self.config[key][subkey]
