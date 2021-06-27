from typing import *
from PasswordProvider import PasswordProvider
from BruteForcePasswordValidator import BruteForcePasswordValidator
import questionary
from questionary import Choice
from enum import Flag, auto
from BruteForceOption import BruteForceOption

class BruteForcePasswordProvider(PasswordProvider):
    def __init__(self, min_length, max_length, *args, **kargs) -> None:
        super().__init__(min_length, max_length)
        self.pattern = None

    def equip(self) -> None:
        options = questionary.checkbox(
            "Brute force attack options",
            choices=[
                Choice("Uppercase letters", value=BruteForceOption.UPPER_CASE),
                Choice("Lowercase letters", value=BruteForceOption.LOWER_CASE),
                Choice("Numbers", value=BruteForceOption.NUMBER),
                Choice("Special Characters", value=BruteForceOption.SPECIAL_CHARACTER),
                Choice("Space", value=BruteForceOption.SPACE),
                Choice("Custom", value=BruteForceOption.CUSTOM)
            ],
            validate=lambda selected: True if len(selected) > 0 else "Please check at least one option"
        ).ask()

        pattern: str = ""

        if BruteForceOption.UPPER_CASE in options:
            pattern += "A-Z"

        if BruteForceOption.LOWER_CASE in options:
            pattern += "a-z"

        if BruteForceOption.NUMBER in options:
            pattern += "0-9"

        if BruteForceOption.SPECIAL_CHARACTER in options:
            pattern += "!-/:-@[-`{-~"

        if BruteForceOption.SPACE in options:
            pattern += " "

        if BruteForceOption.CUSTOM in options:
            pattern += questionary.text(
                "Custom brute force attack options",
                validate=BruteForcePasswordValidator
            ).ask()

        self.set_pattern(pattern)

    def get_pattern(self) -> str:
        return self.pattern

    def set_pattern(self, pattern) -> None:
        self.pattern = pattern

    def get_name(self) -> str:
        return "brute force attack"

    def generate(self):
        candidate: str = ''
        is_ranged: bool = False
        is_escaped: bool = False
        i: int = 0
        candidates: List[str] = []

        while i < len(self.get_pattern()):
            is_escaped = False

            if self.get_pattern()[i] == '\\':
                is_escaped = True
                i += 1

            if is_escaped is False and self.get_pattern()[i] == '-':
                is_ranged = True

            else:
                if candidate == '':
                    candidate = self.get_pattern()[i]

                else:
                    if is_ranged:
                        candidates.extend([chr(j) for j in range(ord(candidate), ord(self.get_pattern()[i]) + 1)])
                        is_ranged = False
                        candidate = ''

                    else:
                        candidates.append(candidate)
                        candidate = self.get_pattern()[i]

            i += 1

        if candidate != '':
            candidates.append(candidate)

        candidates = list(set(candidates))
        candidates.sort()

        carry: bool = False
        update_index: int = 0
        password_data: List[int] = [-1] + [0] * (self.get_min_length()- 1)
        password: List[str] = [candidates[0]] * self.get_min_length()

        while True:
            if carry:
                if update_index == len(password_data):
                    if len(password_data) < self.get_max_length():
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

