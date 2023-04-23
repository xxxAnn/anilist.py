"""
.. highlight:: python

Authentication module

There are several ways to generate an :class:`~.Auth` object::

    # First method
    # Requires a JSON file 
    # with the following structure
    # {
    #   "ID": ...,
    #   "SECRET: ...
    # }
    # where ID and SECRET are the Client ID and the Client Secret

    auth = Auth.from_config_file("filename.json")

    # Second method
    # Requires a dict object
    # with keys "ID" and "SECRET"
    # where ID and SECRET are the Client ID and the Client Secret

    auth = Auth.from_config_object(config_object_name
    
    # Third method
    # where ID and SECRET are the Client ID and the Client Secret

    auth = Auth(ID, SECRET)
"""
from .auth import Auth