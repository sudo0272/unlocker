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

    def post_process_succeed(self) -> None:
        pass

    def post_process_failed(self) -> None:
        pass

