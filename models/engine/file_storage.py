#!/usr/bin/python3
"""
file_storage.py

Contains the FileStorage class for serializing instances to a JSON file 
and deserializing back to instances.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding classes
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """
    Handles serialization of instances to a JSON file and deserialization 
    back to instances.
    """

    # Path to the JSON file
    __file_path = "file.json"
    # Dictionary to store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects currently stored in __objects.

        Args:
        - cls (optional): If specified, filters objects to include only
          instances of the specified class.

        Returns:
        - dict: Dictionary of objects, where keys are <class name>.id and
          values are object instances.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds a new object instance to __objects.

        Args:
        - obj: Instance of a class to be added to __objects.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file specified by __file_path.
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file specified by __file_path back into 
        __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes an object instance from __objects if it exists.

        Args:
        - obj (optional): Instance of a class to be removed from __objects.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() method to deserialize the JSON file back into 
        __objects.
        """
        self.reload()

    @classmethod
    def get(self, cls, id):
        """
        Retrieves a stored object instance based on its specified class 
        and id.

        Args:
        - cls: Class of the object to retrieve.
        - id: ID of the object to retrieve.

        Returns:
        - obj: Instance of the specified class and ID if found, else None.
        """
        key = cls.__name__ + '.' + id
        return FileStorage.__objects.get(key, None)

    @classmethod
    def count(self, cls=None):
        """
        Counts the number of objects stored in __objects.

        Args:
        - cls (optional): If specified, counts only objects of the specified
          class.

        Returns:
        - int: Number of objects stored in __objects.
        """
        if cls is None:
            return len(FileStorage.__objects)
        return len([
            obj for obj in FileStorage.__objects.keys()
            if obj[:len(cls.__name__)] == cls.__name__])
