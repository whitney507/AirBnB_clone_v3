#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
from models import *
import os
from models.base_model import Base
from models.engine.db_storage import DBStorage

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing FileStorage documentation"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """Checks documentation for the file"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage "
                    "of all class instances\n")
        actual = models.file_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Checks documentation for the class"""
        expected = 'handles long term storage of all class instances'
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """Checks documentation for all function"""
        expected = 'returns private attribute: __objects'
        actual = FileStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """Checks documentation for new function"""
        expected = ("sets / updates in __objects the obj with key <obj class "
                    "name>.id")
        actual = FileStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """Checks documentation for save function"""
        expected = 'serializes __objects to the JSON file (path: __file_path)'
        actual = FileStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """Checks documentation for reload function"""
        expected = ("if file exists, deserializes JSON file to __objects, "
                    "else nothing")
        actual = FileStorage.reload.__doc__
        self.assertEqual(expected, actual)

class TestBmFsInstances(unittest.TestCase):
    """Testing class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def setUp(self):
        """Initializes new storage object for testing"""
        self.storage = FileStorage()
        self.bm_obj = BaseModel()

    def test_instantiation(self):
        """Checks proper FileStorage instantiation"""
        self.assertIsInstance(self.storage, FileStorage)

    def test_storage_file_exists(self):
        """Checks if storage file exists"""
        os.remove(F)
        self.bm_obj.save()
        self.assertTrue(os.path.isfile(F))

    def test_obj_saved_to_file(self):
        """Checks if object is saved to file"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_to_json(self):
        """Checks if to_json returns serializable dict object"""
        my_model_json = self.bm_obj.to_json()
        actual = 1
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    def test_reload(self):
        """Checks proper usage of reload function"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_save_reload_class(self):
        """Checks proper usage of class attribute in file storage"""
        os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = 1
        self.assertTrue(1 == actual)

class TestUserFsInstances(unittest.TestCase):
    """Testing class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes new user for testing"""
        self.user = User()
        self.bm_obj = BaseModel()

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_storage_file_exists(self):
        """Checks if storage file exists"""
        os.remove(F)
        self.user.save()
        self.assertTrue(os.path.isfile(F))

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_obj_saved_to_file(self):
        """Checks if object is saved to file"""
        os.remove(F)
       
