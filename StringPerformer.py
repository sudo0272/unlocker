from Performer import Performer
from typing import *
from PasswordProvider import PasswordProvider
import questionary

class StringPerformer(Performer):
    def __init__(self, password_providers: List[PasswordProvider], numbers_password_provider_processes: List[int]) -> None:
        super().__init__(password_providers, numbers_password_provider_processes)
        self.target_password: str = None

    def set_target_password(self, target_password: str) -> None:
        self.target_password = target_password

    def get_target_password(self) -> str:
        return self.target_password

    def equip(self) -> None:
        self.set_target_password(questionary.text(
            "Target password"
        ).ask())

    def has_password(self) -> bool:
        return True

    def check_password(self, password: str) -> bool:
        return self.get_target_password() == password

