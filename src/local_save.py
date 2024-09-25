from os import path
from json import loads as jsonloads
from cryptography.fernet import Fernet

from configuration import USERFILE_NAME, FERNET_KEY

fernet = Fernet(FERNET_KEY)

def local_get() -> str:
    """Vrátí data z lokálního souboru. Hodí chybu, pokud soubor neexistuje."""
    with open(USERFILE_NAME, mode="rb") as userfile:
        return jsonloads(str(fernet.decrypt(userfile.read()), encoding="utf-8"))

def local_set(data: dict) -> None:
    """Zapíše data do lokálního souboru."""
    data = fernet.encrypt(bytes(str(data).replace("'", '"'), encoding="utf-8"))
    with open(USERFILE_NAME, mode="wb") as userfile:
        userfile.write(data)

def local_set_progress(progress: str) -> None:
    """Zapíše postup do lokálního souboru."""
    local_data = local_get()
    local_data["progress"] = progress
    local_set(local_data)

#spustí se při každém otevření hry
def local_check() -> int:
    """Zkontroluje, zda lokální soubor existuje. 1 = existuje, 0 = neexistuje, -1 = chyba při čtení."""
    if path.exists(USERFILE_NAME):
        try:
            local_get()
            return 1
        except Exception:
            return -1 #způsobeno např. uživatelskou úpravou šifrovaných dat
    return 0
