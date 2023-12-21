from config_reader import config
import os
import json


class Admin:
    def __init__(self, **kwargs):
        self.id = config.admin_id
        self.storage = os.path.abspath(os.path.join('admin.json'))

        if not os.path.isfile(self.storage):
            with open(self.storage, 'w') as file:
                json.dump({}, file)

    def check_admin(self, message):
        status = False

        if message.from_user.id == self.id:
            status = True

        return status

    def save_value(self, data: dict):
        try:
            with open(self.storage, 'r+') as file:
                storage = json.load(file)
                file.seek(0)

                for el in data.keys():
                    storage[el] = data[el]

                json.dump(storage, file)
                file.truncate()
        except (FileNotFoundError, json.JSONDecodeError):
            return

    def get_value(self, name: str):
        try:
            with open(self.storage, 'r') as file:
                storage = json.load(file)
                value = storage.get(name)
                return value
        except (FileNotFoundError, json.JSONDecodeError):
            return


admin = Admin()