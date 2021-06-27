from PasswordProvider import PasswordProvider
from pathlib import Path
from mimetypes import guess_type
import questionary

class DictionaryPasswordProvider(PasswordProvider):
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        super().__init__(min_length, max_length)
        self.dictionary_path = None

    def equip(self) -> None:
        dictionary_path = questionary.path(
            "Dictionary path",
            validate=lambda text: True if guess_type(text)[0] == "text/plain" else "Please check the path",
            file_filter=lambda text: Path(text).is_dir() or guess_type(text)[0] == "text/plain"
        ).ask()

        self.set_dictionary_path(dictionary_path)

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

