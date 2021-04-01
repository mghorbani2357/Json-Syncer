from unittest import TestCase
from os import path
from jsonsyncer import JsonSyncer
import os


class TestJsonSyncer(TestCase):
    def tearDown(self):
        if path.exists('test.json'):
            os.remove('test.json')

    def test_file_creation(self):
        JsonSyncer('test.json')

        if not path.exists('test.json'):
            raise FileNotFoundError
