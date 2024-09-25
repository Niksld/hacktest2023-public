import requests
from hashlib import sha512

from configuration import SERVER_IP, SERVER_PORT

def create_hash(text: str) -> str:
    """Vytvoří hash pro rádoby bezpečnější přenos dat."""
    text += "aaaa"
    return sha512(text.encode("utf-8")).hexdigest()

def server_set(username: str, progress_str: str) -> tuple[bool, str|None]:
    """Odešle postup na server."""
    try:
        r = requests.put(f"http://{SERVER_IP}:{SERVER_PORT}/?username={username}&progress={progress_str}&hash={create_hash(username+str(progress_str))}", timeout=(10,15))
        if r.status_code in range(200, 300):
            return True, None
        return False, r.text
    except requests.exceptions.ConnectionError as e:
        return False, e

def server_get(username: str) -> tuple[str|None, str|None]:
    """Načte postup ze serveru."""
    try:
        r = requests.get(f"http://{SERVER_IP}:{SERVER_PORT}/?username={username}&hash={create_hash(username)}", timeout=(10,15))
        if r.status_code in range(200, 300):
            return str(r.text), None
        return None, r.text
    except requests.exceptions.ConnectionError as e:
        return None, e
