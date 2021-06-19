from PasswordProvider import PasswordProvider
from typing import *

class Performer:
    def __init__(self, password_providers: List[PasswordProvider]) -> None:
        self.password_providers = password_providers

    def equip(self) -> None:
        pass

    def unlock(self) -> bool:
        pass

    def post_process(self) -> None:
        pass

    def perform(self) -> List[Union[bool, None]]:
        self.equip()
        self.unlock()
        self.post_process()

