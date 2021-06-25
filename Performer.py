from PasswordProvider import PasswordProvider
from typing import *
import datetime
from halo import Halo
from multiprocessing import Pool, Event, Process, Value, Manager
from ctypes import c_char_p
from time import sleep

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

    @show_unlock_spinner
    def unlock(self) -> Tuple[bool, Union[str, None], datetime.timedelta]:
        # TODO: check if file is already unlocked
        start_time = datetime.datetime.now()
        password_found_event = Event()
        manager = Manager()
        password = manager.Value(c_char_p, "")

        crack_pool = [Process(target=self.crack, args=(self.password_providers[i], self.numbers_password_provider_processes[i], password_found_event, password)) for i in range(len(self.password_providers))]

        for process in crack_pool:
            process.start()

        for process in crack_pool:
            process.join()

        if password.value != "":
            self.correct_password = password.value

        end_time = datetime.datetime.now()

        return self.correct_password, end_time - start_time

    def crack(self, password_provider: list[PasswordProvider], number_password_provider_processes: list[int], password_found_event: Event, password: Value) -> None:
        test_password_pool = Pool(processes=number_password_provider_processes)

        test_password_results = test_password_pool.imap_unordered(self.test_password, password_provider.generate())

        for test_password_result in test_password_results:
            if password_found_event.is_set():
                break

            if test_password_result[0]:
                password.value = test_password_result[1]
                password_found_event.set()

                break

        test_password_pool.terminate()
        test_password_pool.join()

    def test_password(self, password: str) -> [bool, str]:
        is_password_correct = self.check_password(password)

        return is_password_correct, password

    def check_password(self, password: str) -> bool:
        pass

    def post_process_succeed(self) -> None:
        pass

    def post_process_failed(self) -> None:
        pass

