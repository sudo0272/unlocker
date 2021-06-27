from enum import Flag, auto

class BruteForceOption(Flag):
    UPPER_CASE = auto()
    LOWER_CASE = auto()
    NUMBER = auto()
    SPECIAL_CHARACTER = auto()
    SPACE = auto()
    CUSTOM = auto()

