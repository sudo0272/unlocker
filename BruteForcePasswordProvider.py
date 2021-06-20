from typing import *
from PasswordProvider import PasswordProvider

class BruteForcePasswordProvider(PasswordProvider):
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        super().__init__(min_length, max_length)
        self.pattern = args[0]

    def get_name(self) -> str:
        return "brute force attack"

    def generate(self):
        candidate: str = ''
        is_ranged: bool = False
        is_escaped: bool = False
        i: int = 0
        candidates: List[str] = []

        while i < len(self.pattern):
            is_escaped = False

            if self.pattern[i] == '\\':
                is_escaped = True
                i += 1

            if is_escaped is False and self.pattern[i] == '-':
                is_ranged = True

            else:
                if candidate == '':
                    candidate = self.pattern[i]

                else:
                    if is_ranged:
                        candidates.extend([chr(j) for j in range(ord(candidate), ord(self.pattern[i]) + 1)])
                        is_ranged = False
                        candidate = ''

                    else:
                        candidates.append(candidate)
                        candidate = self.pattern[i]

            i += 1

        if candidate != '':
            candidates.append(candidate)

        candidates = list(set(candidates))
        candidates.sort()

        carry: bool = False
        update_index: int = 0
        password_data: List[int] = [-1] + [0] * (self.min_length - 1)
        password: List[str] = [candidates[0]] * self.min_length

        while True:
            if carry:
                if update_index == len(password_data):
                    if len(password_data) < self.max_length:
                        password_data.append(-1)
                        password.append(candidates[0])

                    else:
                        break

            password_data[update_index] += 1
            if password_data[update_index] == len(candidates):
                carry = True
                password_data[update_index] = 0
                password[update_index] = candidates[password_data[update_index]]
                update_index += 1

            else:
                carry = False
                password[update_index] = candidates[password_data[update_index]]
                update_index = 0

                yield ''.join(password)

