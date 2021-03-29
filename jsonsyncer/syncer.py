import json
from collections.abc import MutableMapping
from functools import wraps
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def dump_json(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        result = func(self, *args, **kw)
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.store, json_file)
        return result

    return wrapper


class JsonSyncer(MutableMapping):
    @dump_json
    def __init__(self, json_file_path, *args, **kwargs):
        self.json_file_path = json_file_path

        if path.exists(json_file_path):
            self.__load_json()
        else:
            self.store = dict()

        self.update(dict(*args, **kwargs))

    @dump_json
    def __setitem__(self, key, value):
        self.store[key] = value

    @dump_json
    def __delitem__(self, key):
        del self.store[key]

    def __load_json(self):
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.store, json_file)

    def __file_watcher(self):
        pass

    def __getitem__(self, key):
        return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
