import PyInstaller.__main__
import git
from datetime import datetime
from platform import system
from os import sep, remove, rename

if __name__ == "__main__":
    print("Zabalování aplikace Hacktest 2023")
    repo = git.Repo(search_parent_directories=True)
    version = f"{datetime.fromtimestamp(repo.head.commit.authored_date).strftime('%y%m%d')}-{repo.head.commit.hexsha[:7]}{'+' if repo.is_dirty() else ''}"
    version_file_path = f"src{sep}resources{sep}version.txt"
    timestamp = datetime.now().strftime('%y%m%d-%H%M%S')

    print(f"Verze: {version}{' (VAROVÁNÍ: Verze se liší od posledního commitu)' if repo.is_dirty() else ''}\n")

    with open(version_file_path, mode="w", encoding="utf-8") as version_file:
        version_file.write(version)
    PyInstaller.__main__.run([f"pyinstaller{sep}{system()}.spec"])

    remove(version_file_path)
    rename("build", f"build-{timestamp}")
    if system() == "Windows":
        rename("dist/Hacktest.exe", f"dist/Hacktest2023-{version}+Windows.exe")
    elif system() == "Linux":
        rename("dist/Hacktest", f"dist/Hacktest2023-{version}+Linux")
    rename("dist", f"dist-{timestamp}")
    print(f"\nHotovo, výsledný soubor je uložen v adresáři dist-{timestamp} jako Hacktest2023-{version}+{system()}")
