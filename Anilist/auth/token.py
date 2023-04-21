import requests
import Anilist.utils.consts as consts
from Anilist.auth.code import get_code

def get_token(client_id, client_secret):
    code = get_code(client_id)

    c = requests.post(consts.TOKEN_URI, json={
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://127.0.0.1:8000/',
        'code': code
    }, headers={'Accept': 'application/json'}).json()

    return c["access_token"]    