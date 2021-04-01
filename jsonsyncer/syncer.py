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


class EventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        pass


class JsonSyncer(MutableMapping):
    ignore_changes = True

    event_handler = EventHandler()
    observer = Observer()

    def __init__(self, json_file_path, *args, **kwargs):
        self.json_file_path = json_file_path

        self.event_handler.on_modified = self.__on_modified

        self.store = dict()

        if path.exists(json_file_path):
            self.__load_json()

        self.update(dict(*args, **kwargs))

        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.store, json_file)

        self.observer.schedule(self.event_handler, path=json_file_path, recursive=False)
        self.observer.start()

    @dump_json
    def __setitem__(self, key, value):
        self.store[key] = value

    @dump_json
    def __delitem__(self, key):
        del self.store[key]

    def __load_json(self):
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.store, json_file)

    def __on_modified(self, event):
        self.__load_json()

    def __getitem__(self, key):
        return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
