from PasswordProvider import PasswordProvider
from pathlib import Path

class DictionaryPasswordProvider(PasswordProvider):
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        super().__init__(min_length, max_length)
        self.dictionary_path = None
        self.set_dictionary_path(args[0])

    def get_dictionary_path(self) -> Path:
        return self.dictionary_path

    def set_dictionary_path(self, dictionary_path) -> None:
        self.dictionary_path = dictionary_path

    def get_name(self) -> str:
        return "dictionary attack"

    def generate(self):
        with open(self.get_dictionary_path(), 'r') as dictionary:
            for raw_password in dictionary.readlines():
                password = raw_password.rstrip()

                if self.get_min_length() <= len(password) <= self.get_max_length():
                    yield password

