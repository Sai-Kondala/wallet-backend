import secrets
import time
from config import Config

sessions = {}

def create_session(username):
    token = secrets.token_hex(16)
    expiry = time.time() + Config.SESSION_DURATION
    sessions[token] = (username, expiry)
    return token


def authenticate(token):
    session = sessions.get(token)

    if not session:
        return None

    username, expiry = session

    if time.time() > expiry:
        del sessions[token]
        return None

    return username


def logout(token):
    if token in sessions:
        del sessions[token]
        return True
    return False