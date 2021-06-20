from PasswordProvider import PasswordProvider
from typing import *
import datetime
from halo import Halo
from mimetypes import guess_type

class Performer:
    def __init__(self, password_providers: List[PasswordProvider]) -> None:
        self.password_providers = password_providers
        self.mimetype = ""

    def equip(self) -> None:
        pass

    def unlock(self) -> Tuple[bool, Union[str, None], datetime.timedelta]:
        pass

    def post_process_succeed(self) -> None:
        pass

    def post_process_failed(self) -> None:
        pass

    def check_mimetype(self, target) -> bool:
        return guess_type(target)[0] == self.mimetype

def show_unlock_spinner(func):
    def wrapper(*args):
        spinner = Halo("Unlocking password")
        spinner.start()

        result = func(*args)

        if result[0] is not None:
            spinner.succeed(f"Password found: {result[0]} ({result[1]} elapsed)")

        else:
            spinner.fail(f"Password not found ({result[1]} elapsed)")

        return result

    return wrapper

