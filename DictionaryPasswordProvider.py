from PasswordProvider import PasswordProvider

class DictionaryPasswordProvider(PasswordProvider):
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        super().__init__(min_length, max_length)
        self.dictionary_path = args[0]

    def get_name(self) -> str:
        return "dictionary attack"

    def generate(self):
        with open(self.dictionary_path, 'r') as dictionary:
            for raw_password in dictionary.readlines():
                password = raw_password.rstrip()

                if self.min_length <= len(password) <= self.max_length:
                    yield password

