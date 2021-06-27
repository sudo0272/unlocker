import questionary
from questionary import Choice
import re
import math
from PasswordProvider import PasswordProvider
from BruteForcePasswordProvider import BruteForcePasswordProvider
from BruteForcePasswordValidator import BruteForcePasswordValidator
from DictionaryPasswordProvider import DictionaryPasswordProvider
from typing import List
from ZipPerformer import ZipPerformer
from PdfPerformer import PdfPerformer
from Performer import Performer
from pathlib import Path
import mimetypes
from AttackMethod import AttackMethod

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
        "pdf"
        #  "wifi",
    ]
).ask()

methods = questionary.checkbox(
    "Attack methods",
    choices=[
        Choice("Brute force attack", AttackMethod.BRUTE_FORCE),
        Choice("Dictionary attack", AttackMethod.DICTIONARY)
    ],
    validate=lambda selected: True if len(selected) > 0 else "Please choose attack method"
).ask()

min_length = questionary.text(
    "Minimum length of the password",
    validate=lambda text: True if text.isnumeric() else "Please input number greater than 0"
).ask()
min_length = int(min_length)

max_length = questionary.text(
    "Maximum length of the password (input nothing for infinity)",
    validate=lambda text: True if (text.isnumeric() and int(text) >= min_length) or text == '' else "Please input number greater than minimum length or nothing"
).ask()
max_length = int(max_length) if max_length != '' else math.inf

password_providers: List[PasswordProvider] = []
numbers_password_provider_process: List[int] = []

for method in methods:
    if method == AttackMethod.BRUTE_FORCE:
        password_providers.append(BruteForcePasswordProvider(min_length, max_length))

    elif method == AttackMethod.DICTIONARY:
        password_providers.append(DictionaryPasswordProvider(min_length, max_length))

for password_provider in password_providers:
    password_provider.equip()
    numbers_password_provider_process.append(int(questionary.text(
        f"Number of processes to assign for {password_provider.get_name()}",
        validate=lambda text: True if text.isnumeric() else "Please input number"
    ).ask()))

performer: Performer = None
#  if target_type == 'zip':
    #  performer = ZipPerformer(password_providers, numbers_password_provider_process)

if target_type == 'pdf':
    performer = PdfPerformer(password_providers, numbers_password_provider_process)

performer.perform()

