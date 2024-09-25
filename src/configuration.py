import sys
from os import path, sep, remove
from csv import reader
from json import load as jsonload, loads as jsonloads
from argparse import ArgumentParser

#konstanty
DEBUG = False
DEFAULT_SERVER_IP = "127.0.0.1"
DEFAULT_SERVER_PORT = 20231
FERNET_KEY = b'hrfJf9oImpCNcVKVcQo8KwI4CeHKBEZXwDPD9VUj3is=' # dummy fernet key - 25/09/2024
USERFILE_NAME = path.expanduser("~") + sep + "htest.save"
#pozor - IP a port lze přepsat argumenty z příkazové řádky
#debug mode se automaticky vypne, pokud je aplikace zabalená PyInstallerem

#zpracování argumentů z příkazové řádky
def port(value: str, max: int=65535) -> str:
    """Určí, zda je zadaný řetězec platný port."""
    if not 0 < int(value) < max:
        raise ValueError("Neplatný port.")
    return value

parser = ArgumentParser(prog="Hacktest 2023", description="Úloha")
parser.add_argument("--offline", "--offine-mode", "-o", help="Spustí aplikaci offline.", action="store_true")
parser.add_argument("--reset-save", "--delete-save", "-r", help="Vymaže uložené údaje.", action="store_true")
parser.add_argument("--ip", "--server-ip", help=f"IP adresa serveru, která se použije místo výchozí ({DEFAULT_SERVER_IP}).", default=DEFAULT_SERVER_IP)
parser.add_argument("--port", "--server-port", help=f"Port serveru, který se použije místo výchozího ({DEFAULT_SERVER_PORT}).", type=port, default=DEFAULT_SERVER_PORT)
args = vars(parser.parse_known_args()[0])

#argumenty z příkazové řádky
OFFLINE_MODE = True
USERFILE_RESET = args["reset_save"]
SERVER_IP = args["ip"]
SERVER_PORT = args["port"]

if USERFILE_RESET and path.isfile(USERFILE_NAME):
    remove(USERFILE_NAME)

#PyInstaller
if getattr(sys, 'frozen', False):
    APPLICATION_PATH = sys._MEIPASS
    DEBUG = False
else:
    APPLICATION_PATH = path.dirname(path.abspath(__file__))

def relpath(path: str, application_path=APPLICATION_PATH) -> str:
    """Převádí relativní cesty na absolutní podle toho, jestli je aplikace zabalená použitím PyInstalleru.
    Je nutné použít pro všechny cesty k souborům, které jsou zabalené s aplikací."""
    return application_path + sep + "resources" + sep + path.replace("/", sep)

#určení verze
try:
    with open(relpath("version.txt"), mode="r", encoding="utf-8") as version_file:
        RELEASE_VERSION = "rel-" + version_file.read()
except FileNotFoundError:
    RELEASE_VERSION = "(live)"

#porovnání řetězců s postupem
def get_progress_highest(*progress_strings: str) -> str:
    """Porovná postupy všech zadaných řetězců (2 a více) a vrátí nejvyšší dosažený postup."""
    if len(progress_strings) < 2:
        raise ValueError("Musí být zadány alespoň 2 řetězce.")
    else:
        progress = ""
        for i in range(len(progress_strings[0])):
            progress += str(max([int(x[i]) for x in progress_strings]))
        return progress

def get_progress_requirement(progress_string: str, required_progress_string: str = "################", maximum_progress_string: str = "################") -> bool:
    """Zkontroluje, zda je postup v rozsahu mezi minimální a maximální hodnotou."""
    for i in range(len(progress_string)):
        if required_progress_string[i] != "#":
            if int(progress_string[i]) < int(required_progress_string[i]):
                return False
        if maximum_progress_string[i] != "#":
            if int(progress_string[i]) >= int(maximum_progress_string[i]):
                return False
    return True

#nastavení řetězce s postupem
def set_progress_index(progress_string: str, index: int, value: int) -> str:
    """Nastaví hodnotu na daném indexu."""
    if int(progress_string[index]) > value:
        return progress_string
    return progress_string[:index] + str(value) + progress_string[index + 1:]

def set_progress_increment(progress_string: str, index: int, value: int = 1) -> str:
    """Zvýší hodnotu na daném indexu."""
    if int(progress_string[index]) + value > 9:
        return progress_string
    return progress_string[:index] + str(int(progress_string[index]) + value) + progress_string[index + 1:]

#načtení souboru level.json, který slouží k tomu, aby všechno nebylo "natvrdo" v kódu
with open(relpath("level.json"), "r", encoding="utf-8") as f:
    LEVEL_DATA = jsonload(f)

#načtení seznamu účastníků ze souboru
with open(relpath("contestants/ucastnici.csv"), mode="r", encoding="utf-8") as attendee_file:
    ATTENDEES = {x[0]: x[1] for x in list(reader(attendee_file, delimiter=";"))[1:]}
