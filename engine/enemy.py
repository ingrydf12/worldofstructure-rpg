from skeleton import Skeleton
from enemy_infos import ENEMY_INFOS
import json

class Enemy(Skeleton):
    def __init__(self, nome):
        if nome not in ENEMY_INFOS:
            raise ValueError(f"Inimigo '{nome}' não existe")

        info = ENEMY_INFOS[nome]

        super().__init__(
            name=nome, life=info["life"], attributes=info["attributes"].copy()
        )

    def get_estado(self):
        return {
            "name": self.name,
            "life": self.life,
            "attributes": self.attributes,
        }

    def emitir_estado(self):
        print(f"ENEMY_STATE::{json.dumps(self.get_estado())}", flush=True)

    def max_attribute(self):
        if not self.attributes:
            return None, 0
        atributo_max = max(self.attributes, key=self.attributes.get)
        return atributo_max, self.attributes[atributo_max]
