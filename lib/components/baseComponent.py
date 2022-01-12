from abc import ABC, abstractmethod

class BaseComponent(ABC):
    
    @staticmethod
    @abstractmethod
    def connect(rotation,intersectionVertices):
        pass