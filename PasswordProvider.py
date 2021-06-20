from typing import *

class PasswordProvider:
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def get_name(self) -> str:
        pass

    def generate(self) -> Generator[str, None, None]:
        pass

