import json

from Anilist.auth.token import get_token

class Auth:
    """
    Representation of an authenticated connection to the Anilist API

    :param client_id: The ID of the API Client
    :type client_id: :class:`~int`
        
    :param client_secret: The secret code of the API Client
    :type client_secret: :class:`~str`
    """
    def __init__(self, client_id, client_secret):
        """Constructor method
        """
        self.__id = client_id
        self.__secret = client_secret
        self.__token = None

        self.__gen_token()

    def __gen_token(self):
        self.__token = get_token(self.__id, self.__secret)

    @property
    def token(self):
        return self.__token

    @classmethod
    def from_config_object(cls, config):
        """Authenticates an Auth object from a config object

        :param config: The config object
        :type config: :class:`~dict`

        :return: An authenticated Auth object
        :rtype: :class:`~.Auth`
        """
        return cls(config["ID"], config["SECRET"])
    
    @classmethod
    def from_config_file(cls, file):
        """Authenticates an Auth object from a config file

        :param file: The config file's name
        :type file: :class:`~str`

        :return: An authenticated Auth object
        :rtype: :class:`~.Auth`
        """
        with open(file, 'r') as f:
            config = json.loads(f.read())
        return cls(config["ID"], config["SECRET"])
