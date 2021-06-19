from typing import *

class PasswordProvider:
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def generate(self) -> str:
        pass

