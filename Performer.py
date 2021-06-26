from PasswordProvider import PasswordProvider
from typing import *
from datetime import datetime
from halo import Halo
from multiprocessing import Pool, Event, Process, Value, Manager
from ctypes import c_char_p
from time import sleep

class Performer:
    def __init__(self, password_providers: List[PasswordProvider], numbers_password_provider_processes: List[int]) -> None:
        self.password_providers = password_providers
        self.numbers_password_provider_processes = numbers_password_provider_processes
        self.target = None
        self.correct_password = None
        self.messages = {
            "unlock": {
                "password_found": "Password found: {} ({} elapsed)",
                "password_not_found": "Password not found ({} elapsed)",
                "has_no_password": "It is already not encrypted"
            }
        }

    def get_target(self) -> Any:
        return self.target

    def set_target(self, target: Any) -> None:
        self.target = target

    def get_correct_password(self) -> str:
        return self.correct_password

    def set_correct_password(self, correct_password: str) -> None:
        self.correct_password = correct_password

    def get_message(self, category: str, key: str) -> str:
        return self.messages[category][key]

    def set_message(self, category: str, key: str, value: str) -> None:
        self.messages[category][key] = value

    def equip(self) -> None:
        pass

    def unlock(self) -> Union["password_found", "password_not_found", "has_no_password"]:
        if not self.has_password():
            return "has_no_password"

        password_found_event = Event()
        manager = Manager()
        password = manager.Value(c_char_p, "")

        crack_pool = [Process(target=self.crack, args=(self.password_providers[i], self.numbers_password_provider_processes[i], password_found_event, password)) for i in range(len(self.password_providers))]

        for process in crack_pool:
            process.start()

        for process in crack_pool:
            process.join()

        if password.value != "":
            self.set_correct_password(password.value)

            return "password_found"

        else:
            return "password_not_found"

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

    def has_password(self) -> bool:
        pass

    def check_password(self, password: str) -> bool:
        return True

    def post_process_succeed(self) -> None:
        pass

    def post_process_failed(self) -> None:
        pass

    def perform(self) -> None:
        self.equip()

        spinner = Halo("Unlocking password")
        spinner.start()
        start_time = datetime.now()
        unlock_result = self.unlock()
        elapsed_time = datetime.now() - start_time

        message = self.get_message("unlock", unlock_result)

        if unlock_result == "password_found":
            spinner.succeed(message.format(self.correct_password, elapsed_time))
            self.post_process_succeed()

        elif unlock_result == "password_not_found":
            spinner.fail(message.format(elapsed_time))
            self.post_process_failed()

        elif unlock_result == "has_no_password":
            spinner.fail(message.format(elapsed_time))
            self.post_process_failed()

