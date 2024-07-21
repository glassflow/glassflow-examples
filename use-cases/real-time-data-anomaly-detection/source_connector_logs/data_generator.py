from faker import Faker
import random


class DataGenerator:
    def __init__(self):
        # Define a list of actions/events
        self.actions = [
            "logged in",
            "accessed file",
            "executed command",
            "accessed directory",
        ]
        self.fake = Faker()

    def generate_log(self):
        log = ""
        timestamp = self.fake.date_time_this_year().strftime("[%d/%b/%Y %H:%M:%S]")
        ip_address = self.fake.ipv4()
        user = self.fake.user_name()
        action = random.choice(self.actions)
        if action == "logged in":
            log = f"{timestamp} {ip_address} {user} {action} successfully"
        elif action == "accessed file":
            file_name = self.fake.file_name()
            log = f"{timestamp} {ip_address} {user} {action} '{file_name}'"
        elif action == "executed command":
            command = self.fake.word()
            log = f"{timestamp} {ip_address} {user} executed command '{command}'"
        elif action == "accessed directory":
            directory = self.fake.file_path(depth=random.randint(1, 3))
            log = f"{timestamp} {ip_address} {user} accessed directory '{directory}'"
        return log


if __name__ == "__main__":
    data_gen = DataGenerator()
    print(data_gen.generate_log())