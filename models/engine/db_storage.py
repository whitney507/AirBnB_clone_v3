```python
#!/usr/bin/python3
""" Database Engine Module """

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user

class DBStorage:
    """Manages long-term storage of all class instances"""

    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine self.__engine"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.CNC.get(cls)).all()
            for item in obj_class:
                key = f"{item.__class__.__name__}.{item.id}"
                obj_dict[key] = item
            return obj_dict
        for class_name in self.CNC:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.CNC.get(class_name)).all()
            for item in obj_class:
                key = f"{item.__class__.__name__}.{item.id}"
                obj_dict[key] = item
        return obj_dict

    def new(self, obj):
        """Adds objects to the current database session"""
        self.__session.add(obj)

    def get(self, cls, id):
        """
        Fetches a specific object
        :param cls: Class name of the object as a string
        :param id: ID of the object as a string
        :return: Found object or None
        """
        all_class = self.all(cls)

        for obj in all_class.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        Counts how many instances of a class exist
        :param cls: Class name
        :return: Count of instances of a class
        """
        return len(self.all(cls))

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database & session from the engine"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
        Calls remove() on the private session attribute (self.__session)
        """
        self.__session.remove()
```
