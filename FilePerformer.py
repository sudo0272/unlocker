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
        self.mimetype = None
        self.output_directory = None

        self.set_message("unlock", "has_no_password", "Given file is not an encrypted file")

    def get_mimetype(self) -> str:
        return self.mimetype

    def set_mimetype(self, mimetype: str) -> None:
        self.mimetype = mimetype

    def get_output_directory(self) -> Path:
        return self.output_directory

    def set_output_directory(self, output_directory: str) -> None:
        self.output_directory = Path(output_directory)

    def equip(self) -> None:
        self.set_target(questionary.path(
            "Target file",
            validate=lambda text: True if Path(text).is_file() else "Please check the path"
        ).ask())

        self.set_output_directory(questionary.path(
            "Output directory",
            only_directories=True,
            validate=lambda text: True if Path(text).is_dir() else "Please check the path"
        ).ask())

    def check_mimetype(self, target) -> bool:
        return guess_type(target)[0] == self.get_mimetype()

