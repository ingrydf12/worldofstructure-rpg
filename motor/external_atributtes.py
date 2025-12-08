from abc import ABC, abstractmethod

class Skeleton(ABC):
    def __init__(self, name, life, attributes):
        self.name = name
        self.life = life
        self.attributes = attributes

    @abstractmethod
    def attack(self, target):
        pass
