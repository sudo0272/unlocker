from PasswordProvider import PasswordProvider
from typing import *
import datetime
from halo import Halo
from multiprocessing import Pool

def show_unlock_spinner(func):
    def wrapper(*args):
        spinner = Halo("Unlocking password")
        spinner.start()

        result = func(*args)

        if result[0] is not None:
            spinner.succeed(f"Password found: {result[0]} ({result[1]} elapsed)")

        else:
            spinner.fail(f"Password not found ({result[1]} elapsed)")

        return result

    return wrapper


class Performer:
    def __init__(self, password_providers: List[PasswordProvider], numbers_password_provider_processes: List[int]) -> None:
        self.password_providers = password_providers
        self.numbers_password_provider_processes = numbers_password_provider_processes
        self.mimetype = ""
        self.correct_password = None

    def equip(self) -> None:
        pass

    # ERROR: AssertionError: daemonic processes are not allowed to have children
    @show_unlock_spinner
    def unlock(self) -> Tuple[bool, Union[str, None], datetime.timedelta]:
        start_time = datetime.datetime.now()
        crack_pool = Pool(processes=2)
        crack_results = crack_pool.imap_unordered(self.crack, zip(self.password_providers, self.numbers_password_provider_processes))

        for crack_result in crack_results:
            if crack_result:
                crack_pool.terminate()
                break

        crack_pool.join()

        end_time = datetime.datetime.now()

        return self.correct_password, end_time - start_time

    def crack(self, args) -> bool:
        password_provider = args[0]
        number_password_provider_processes = args[1]
        check_password_pool = Pool(processes=number_password_provider_processes)

        check_password_results = check_password_pool.imap_unordered(self.check_password, password_provider.generate())

        for check_password_result in check_password_results:
            if check_password_result:
                check_password_pool.terminate()
                break

        check_password_pool.join()

    def check_password(self, password: str) -> bool:
        pass

    def post_process_succeed(self) -> None:
        pass

    def post_process_failed(self) -> None:
        pass

