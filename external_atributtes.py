from abc import ABC, abstractmethod

class_torm_types = [warrior: 'Warrior', archer: 'Archer', magician: 'Magician'];

@abstractmethod
class Skeleton(ABC):
    def __init__(self, life, atributtes):
        self.life = None;

    def constructor_persona(class_type):
        class_type = class_torm_types.warrior