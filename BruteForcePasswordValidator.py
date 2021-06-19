import questionary
from questionary import Validator, ValidationError, prompt

class BruteForcePasswordValidator(Validator):
    def validate(self, document):
        temp = ''
        is_ranged = False
        is_escaped = False
        is_valid = True
        i = 0

        while i < len(document):
            is_escaped = False

            if document[i] == '\\':
                if i + 1 < len(document):
                    if document[i + 1] not in '\\-':
                        is_valid = False
                        break

                    is_escaped = True
                    i += 1

                else:
                    is_valid = False
                    break

            if is_escaped is False and document[i] == '-':
                if is_ranged:
                    is_valid = True
                    break

                is_ranged = True

            else:
                if temp == '':
                    temp = document[i]

                else:
                    if is_ranged:
                        is_ranged = False
                        temp = ''

                    else:
                        temp = document[i]

            i += 1

        if is_ranged:
            is_valid = False

        return True if is_valid else "Please check your pattern"

