from abc import ABC, abstractmethod

@abstractmethod
class Player(ABC):
    def __init__(self, class_type, name):
        self.class_type = class_type;
        self.name = name
        self.life = 30
        self.history = None;
        self.actions = None;