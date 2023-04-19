import json

from Anilist.auth.token import get_token

class Auth:

    def __init__(self, client_id, client_secret):
        self.__id = client_id
        self.__secret = client_secret
        self.__token = None

        self.__gen_token()

    def __gen_token(self):
        self.__token = get_token(self.__id, self.__secret)

    @classmethod
    def from_config_object(cls, config):
        return cls(config["ID"], config["SECRET"])
    
    @classmethod
    def from_config_file(cls, file):
        with open(file, 'r') as f:
            config = json.loads(f.read())
        return cls(config["ID"], config["SECRET"])
