```python
#!/usr/bin/python3
"""Unit Test for BaseModel Class"""

import unittest
from datetime import datetime
from models import *
import os
from models.base_model import Base
from models.engine.db_storage import DBStorage

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestDBStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ' Database engine '
        actual = db_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'handles long term storage of all class instances'
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """... documentation for all function"""
        expected = ' returns a dictionary of all objects '
        actual = DBStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """... documentation for new function"""
        expected = ' adds objects to current database session '
        actual = DBStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """... documentation for save function"""
        expected = ' commits all changes of current database session '
        actual = DBStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """... documentation for reload function"""
        expected = ' creates all tables in database & session from engine '
        actual = DBStorage.reload.__doc__
        self.assertEqual(expected, actual)

    def test_doc_delete(self):
        """... documentation for delete function"""
        expected = ' deletes obj from current database session if not None '
        actual = DBStorage.delete.__doc__
        self.assertEqual(expected, actual)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStateDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage .;.......')
        print('........ For State Class ........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new BaseModel object for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()

    def test_state_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_state_objs = storage.all('State')

        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_state_delete(self):
        state_id = self.state.id
        storage.delete(self.state)
        self.state = None
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)

if __name__ == '__main__':
    unittest.main()
```
