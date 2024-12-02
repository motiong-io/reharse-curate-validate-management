from abc import ABC, abstractmethod


class BaseRepo(ABC):
    """this class locks that other repos needs to have below methods"""

    @abstractmethod
    def create_one(self): ...
    @abstractmethod
    def patch_one(self): ...
    @abstractmethod
    def get_one(self): ...
    @abstractmethod
    def delete_one(self): ...
