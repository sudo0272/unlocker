from PasswordProvider import PasswordProvider
from typing import *
import datetime

class Performer:
    def __init__(self, password_providers: List[PasswordProvider]) -> None:
        self.password_providers = password_providers

    def equip(self) -> None:
        pass

    def unlock(self) -> Tuple[bool, Union[str, None], datetime.timedelta]:
        pass

    def post_process(self) -> None:
        pass

    def perform(self) -> Tuple[None, Tuple[Union[str, None], datetime.timedelta], None]:
        results = []
        results.append(self.equip())
        results.append(self.unlock())
        results.append(self.post_process())

        return results

