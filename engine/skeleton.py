from abc import ABC, abstractmethod

class Skeleton(ABC):
    def __init__(self, name, life, attributes):
        self.name = name
        self.life = life
        self.attributes = attributes
        
    def is_alive(self):
        return self.life > 0