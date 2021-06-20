from FilePerformer import FilePerformer
from typing import *
from PasswordProvider import PasswordProvider
from pathlib import Path
from zipfile import ZipFile
import zlib
from halo import Halo
import datetime
import questionary

class ZipPerformer(FilePerformer):
    def __init__(self, password_providers: List[PasswordProvider]) -> None:
        super().__init__(password_providers)
        self.target = None
        self.output_directory = None
        self.correct_password = None

    def equip(self) -> None:
        self.target = questionary.path(
            "Target zip file",
            validate=lambda text: True if Path(text).is_file() and text.split('.')[-1] == "zip" else "Please check the path",
            file_filter=lambda text: True if Path(text).is_dir() or (Path(text).is_file() and text.split('.')[-1] == "zip") else False
        ).ask()

        self.output_directory= questionary.path(
            "Output directory",
            only_directories=True,
            validate=lambda text: True if Path(text).is_dir() else "Please check the path"
        ).ask()

    def unlock(self) -> Tuple[bool, Union[str, None], datetime.timedelta]:
        self.correct_password = None

        start_time = datetime.datetime.now()

        # BUG: BadZipFile CRC-32 even for valid zip file
        with ZipFile(self.target, mode='r') as target_zip:
            for password_provider in self.password_providers:
                spinner = Halo(text=f"Unlocking password with {password_provider.get_name()}", spinner="dots")
                spinner.start()

                for password in password_provider.generate():
                    try:
                        target_zip.extractall(self.output_directory, pwd=password.encode('utf8'))

                        self.correct_password = password

                        break

                    except (zlib.error, RuntimeError):
                        pass

                spinner.stop()

                if self.correct_password is not None:
                    break

        end_time = datetime.datetime.now()

        return self.correct_password, end_time - start_time

