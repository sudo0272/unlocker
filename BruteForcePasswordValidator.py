import questionary
from questionary import Validator, ValidationError, prompt

class BruteForcePasswordValidator(Validator):
    def validate(self, document) -> None:
        temp = ''
        is_ranged = False
        is_escaped = False
        is_valid = True
        i = 0

        while i < len(document.text):
            is_escaped = False

            if document.text[i] == '\\':
                if i + 1 < len(document.text):
                    if document.text[i + 1] not in '\\-':
                        is_valid = False
                        break

                    is_escaped = True
                    i += 1

                else:
                    is_valid = False
                    break

            if is_escaped is False and document.text[i] == '-':
                if is_ranged:
                    is_valid = True
                    break

                is_ranged = True

            else:
                if temp == '':
                    temp = document.text[i]

                else:
                    if is_ranged:
                        is_ranged = False
                        temp = ''

                    else:
                        temp = document.text[i]

            i += 1

        if is_ranged:
            is_valid = False

        if not is_valid:
            raise ValidationError(
                message="Please check your options",
                cursor_position=len(document.text)
            )

