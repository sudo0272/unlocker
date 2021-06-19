import questionary
import re
import math

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
        "wifi",
    ]
).ask()

methods = questionary.checkbox(
    "Attack methods",
    choices=[
        "Brute force attack",
        "Dictionary attack"
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
max_length = int(max_length) if max_length!= '' else math.inf

