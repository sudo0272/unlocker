import pikepdf
from pikepdf import Pdf
from FilePerformer import FilePerformer
from Performer import show_unlock_spinner
from PasswordProvider import PasswordProvider
from pathlib import Path
import questionary
from typing import *
import datetime
from halo import Halo
from mimetypes import guess_type

class PdfPerformer(FilePerformer):
    def __init__(self, password_providers: List[PasswordProvider]) -> None:
        super().__init__(password_providers)
        self.target = None
        self.output_file = None
        self.correct_password = None
        self.mimetype = "application/pdf"

    def equip(self) -> None:
        self.target = questionary.path(
            "Target pdf file",
            validate=lambda text: True if self.check_mimetype(text) else "Please check the path",
            file_filter=lambda text: True if Path(text).is_dir() or self.check_mimetype(text) else False
        ).ask()

        self.output_file = questionary.path(
            "Output file",
            validate=lambda text: True if not Path(text).is_dir() else "Please check the path",
            file_filter=lambda text: True if Path(text).is_dir() or self.check_mimetype(text) else False
        ).ask()

    @show_unlock_spinner
    def unlock(self) -> Tuple[bool, Union[str, None], datetime.timedelta]:
        start_time = datetime.datetime.now()
        for password_provider in self.password_providers:
            for password in password_provider.generate():
                try:
                    Pdf.open(self.target, password=password)
                    self.correct_password = password

                    break

                except pikepdf._qpdf.PasswordError:
                    pass

            if self.correct_password is not None:
                break

        end_time = datetime.datetime.now()

        return self.correct_password, end_time - start_time

    def post_process_succeed(self) -> None:
        spinner = Halo(text="Generating output file")
        spinner.start()

        try:
            target_pdf = Pdf.open(self.target, password=self.correct_password)
            output_pdf = Pdf.new()

            output_pdf.pages.extend(target_pdf.pages)

            output_pdf.save(self.output_file)

            spinner.succeed("Output file generated")

        except:
            spinner.fail("Output file could not be generated")

