import json
from collections.abc import MutableMapping
from functools import wraps
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


def dump_json(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        result = func(self, *args, **kw)
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.store, json_file)
        return result

    return wrapper


class JsonSyncer(MutableMapping):
    __ignore_changes = False

    __event_handler = FileSystemEventHandler()
    __observer = Observer()

    def __init__(self, json_file_path, *args, **kwargs):
        self.json_file_path = json_file_path

        self.__event_handler.on_modified = self.__on_modified

        self.store = dict()

        if path.exists(json_file_path):
            self.__load_json()

        self.update(dict(*args, **kwargs))

        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.store, json_file)

        self.stat = os.stat(self.json_file_path)

        self.__observer.schedule(self.__event_handler, path=json_file_path, recursive=False)
        self.__observer.start()

    @dump_json
    def __setitem__(self, key, value):
        self.__ignore_changes = True
        self.store[key] = value

    @dump_json
    def __delitem__(self, key):
        del self.store[key]

    def __load_json(self):
        with open(self.json_file_path) as json_file:
            self.store = json.load(json_file)

    def __on_modified(self, event):
        if event.src_path == self.json_file_path and os.stat(self.json_file_path).st_ctime > self.stat.st_ctime:
            self.stat = os.stat(self.json_file_path)
            if not self.__ignore_changes:
                self.__load_json()
            self.__ignore_changes = False

    def __getitem__(self, key):
        return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return self.store.__len__()

    def __repr__(self):
        return str(self.store)

    def __str__(self):
        return str(self.store)
