import pikepdf
from pikepdf import Pdf
from FilePerformer import FilePerformer
from PasswordProvider import PasswordProvider
from pathlib import Path
import questionary
from typing import *
import datetime
from halo import Halo
from mimetypes import guess_type
from multiprocessing import Pool

class PdfPerformer(FilePerformer):
    def __init__(self, password_providers: List[PasswordProvider], numbers_password_provider_processes: List[int]) -> None:
        super().__init__(password_providers, numbers_password_provider_processes)
        self.target = None
        self.output_file = None
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

    def has_password(self) -> bool:
        try:
            # try opening file without password
            Pdf.open(self.target)

            return False

        except pikepdf._qpdf.PasswordError:
            return True

    def check_password(self, password: str) -> bool:
        try:
            Pdf.open(self.target, password=password)
            self.correct_password = password

            return True

        except pikepdf._qpdf.PasswordError:
            return False

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

