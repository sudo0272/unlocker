from typing import *

class PasswordProvider:
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        self.set_min_length(min_length)
        self.set_max_length(max_length)

    def equip(self) -> None:
        pass

    def get_min_length(self) -> int:
        return self.min_length

    def set_min_length(self, min_length) -> None:
        self.min_length = min_length

    def get_max_length(self) -> int:
        return self.max_length

    def set_max_length(self, max_length) -> None:
        self.max_length = max_length

    def get_name(self) -> str:
        pass

    def generate(self) -> Generator[str, None, None]:
        pass

