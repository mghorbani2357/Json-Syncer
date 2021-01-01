import os
import hashlib
import asyncio
from threading import Thread


class FileWatcher(object):
    hash_md5 = hashlib.md5()
    __watching = False

    def __init__(self, path):
        self.path = path

        asyncio.get_event_loop().run_until_complete(self._file_hash_changed(path))

    def __get_files_and_directories(self):

        directories = list()
        files = list()

        for (directory_path, directory_names, filenames) in os.walk(self.path):
            for directory_name in directory_names:
                directories.append(f'{directory_path}/{directory_name}')

            for filename in filenames:
                files.append(f'{directory_path}/{filename}')

        return files, directories

    @staticmethod
    def __get_file_md5_hash(file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    async def _file_hash_changed(self, file_path):
        file_hash = self.__get_file_md5_hash(file_path)
        while True:
            await asyncio.sleep(0.1)
            current_file_hash = self.__get_file_md5_hash(file_path)
            if current_file_hash != file_hash:
                Thread(target=self.modified, args=(file_path,)).start()
                file_hash = current_file_hash

    async def __watcher(self):
        pass

    def modified(self, file_path):
        pass

    def created(self):
        pass

    def deleted(self):
        pass

    def renamed(self):
        pass
