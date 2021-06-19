from Performer import Performer
from Performer import Performer
from PasswordProvider import PasswordProvider
import questionary
from typing import *
from pathlib import Path

class FilePerformer(Performer):
    def __init__(self, password_providers: List[PasswordProvider]) -> None:
        super().__init__(password_providers)

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
