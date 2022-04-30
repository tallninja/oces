import os


class File:

    @staticmethod
    def read(file):
        data = None
        if os.path.isfile(file):
            with open(file, 'r') as file:
                data = file.read()
        return data

    @staticmethod
    def write(file, data):
        with open(file, 'w') as file:
            file.write(data)

    @staticmethod
    def read_bytes(file):
        data = None
        if os.path.isfile(file):
            with open(file, 'rb') as file:
                data = file.read().decode('utf-8').strip()
        return data

    @staticmethod
    def write_bytes(file, data):
        with open(file, 'wb') as file:
            file.write(bytes(data, encoding='utf-8'))

    @staticmethod
    def is_empty(file):
        return os.stat(file).st_size == 0
