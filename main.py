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

targetType = questionary.select(
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

minLength = questionary.text(
    "Minimum length of the password",
    validate=lambda text: True if re.match(r"^\d+$", text) and int(text) > 0 else "Please input number greater than 0"
).ask()
minLength = int(minLength)

maxLength = questionary.text(
    "Maximum length of the password (input nothing for infinity)",
    validate=lambda text: True if (re.match(r"^\d+$", text) and int(text) >= minLength) or text == '' else "Please input number greater than minimum length or nothing"
).ask()
maxLength = int(maxLength) if maxLength != '' else math.inf

