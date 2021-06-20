import questionary
from questionary import Choice
import re
import math
from PasswordProvider import PasswordProvider
from BruteForcePasswordProvider import BruteForcePasswordProvider
from BruteForcePasswordValidator import BruteForcePasswordValidator
from typing import List
from ZipPerformer import ZipPerformer
from Performer import Performer

print(r" _   _       _            _             ")
print(r"| | | |     | |          | |            ")
print(r"| | | |_ __ | | ___   ___| | _____ _ __ ")
print(r"| | | | '_ \| |/ _ \ / __| |/ / _ \ '__|")
print(r"| |_| | | | | | (_) | (__|   <  __/ |   ")
print(r" \___/|_| |_|_|\___/ \___|_|\_\___|_|   ")
print(r"                                        ")

target_type = questionary.select(
    "Type of the target",
    choices=[
        "zip",
        #  "wifi",
    ]
).ask()

methods = questionary.checkbox(
    "Attack methods",
    choices=[
        "Brute force attack",
        #  "Dictionary attack"
    ],
    validate=lambda selected: True if len(selected) > 0 else "Please choose attack method"
).ask()

min_length = questionary.text(
    "Minimum length of the password",
    validate=lambda text: True if re.match(r"^\d+$", text) and int(text) > 0 else "Please input number greater than 0"
).ask()
min_length = int(min_length)

max_length = questionary.text(
    "Maximum length of the password (input nothing for infinity)",
    validate=lambda text: True if (re.match(r"^\d+$", text) and int(text) >= min_length) or text == '' else "Please input number greater than minimum length or nothing"
).ask()
max_length = int(max_length) if max_length != '' else math.inf

password_providers: List[PasswordProvider] = []
if "Brute force attack" in methods:
    brute_force_options = questionary.checkbox(
        "Brute force attack options",
        choices=[
            Choice("Uppercase letters", value="A"),
            Choice("Lowercase letters", value="a"),
            Choice("Numbers", value="1"),
            Choice("Special Characters", value="!"),
            Choice("Space", value="s"),
            Choice("Custom", value="custom")
        ],
        validate=lambda selected: True if len(selected) > 0 else "Please check at least one option"
    ).ask()

    brute_force_pattern: str = ""

    if "A" in brute_force_options:
        brute_force_pattern += "A-Z"

    if "a" in brute_force_options:
        brute_force_pattern += "a-z"

    if "1" in brute_force_options:
        brute_force_pattern += "0-9"

    if "!" in brute_force_options:
        brute_force_pattern += "!-/:-@[-`{-~"

    if "s" in brute_force_options:
        brute_force_pattern += " "

    if "custom" in brute_force_options:
        brute_force_pattern += questionary.text(
            "Custom brute force attack options",
            validate=BruteForcePasswordValidator
        ).ask()

    password_providers.append(BruteForcePasswordProvider(min_length, max_length, brute_force_pattern))

performer: Performer = None
if target_type == 'zip':
    performer = ZipPerformer(password_providers)

print("--------- Equipment ---------")
print("----------- Done ------------")
performer.equip()
print("--------- Unlocking ---------")
print("----------- Done ------------")
unlock_result = performer.unlock()

# succeed
if unlock_result[0] is not None:
    print(f"Unlocked successfully ({unlock_result[1]} elapsed)")
    print(f"Password: {unlock_result[0]}")

    print("------ Post-processing ------")
    performer.post_process_succeed()
    print("----------- Done ------------")

# failed
else:
    print("Unlocking failed ({unlock_result[1]} elapsed)")
    print("------ Post-processing ------")
    performer.post_process_failed()
    print("----------- Done ------------")

