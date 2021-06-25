from Performer import Performer
from Performer import Performer
from PasswordProvider import PasswordProvider
import questionary
from typing import *
from pathlib import Path
from mimetypes import guess_type

class FilePerformer(Performer):
    def __init__(self, password_providers: List[PasswordProvider], numbers_password_provider_processes: List[int]) -> None:
        super().__init__(password_providers, numbers_password_provider_processes)

        self.messages["unlock"]["has_no_password"] = "Given file is not an encrypted file"

    def equip(self) -> None:
        self.target = questionary.path(
            "Target file",
            validate=lambda text: True if Path(text).is_file() else "Please check the path"
        ).ask()

        self.output_directory= questionary.path(
            "Output directory",
            only_directories=True,
            validate=lambda text: True if Path(text).is_dir() else "Please check the path"
        ).ask()

    def check_mimetype(self, target) -> bool:
        return guess_type(target)[0] == self.mimetype

