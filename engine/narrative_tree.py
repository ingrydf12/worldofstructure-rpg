import json
import uuid

class Branch:
    def __init__(self, titulo, narrativa, evento=None):
        self.id = str(uuid.uuid4())
        self.parents = []

        self.titulo = titulo
        self.narrativa = narrativa
        self.evento = evento

        self.choices = {}

    def add_choice(self, key, choice):
        if key in self.choices:
            raise ValueError(f"Escolha '{key}' já existe neste nó")
        self.choices[key] = choice

    def is_leaf(self):
        return len(self.choices) == 0

    def get_child(self, escolha):
        choice = self.choices.get(escolha)
        return choice.target if choice else None

    def emitir_no(self):
        dados = {
            "id": self.id,
            "titulo": self.titulo,
            "narrativa": [
                linha.strip()
                for linha in self.narrativa.strip().split("\n")
                if linha.strip()
            ],
            "opcoes": [
                {"id": key, "texto": choice.texto}
                for key, choice in self.choices.items()
            ],
            "isLeaf": self.is_leaf(),
        }

        print(f"BRANCH_DATA::{json.dumps(dados, ensure_ascii=False)}", flush=True)

class AdaptativeGraphNarrative:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def create_root(self, titulo, narrativa, evento=None):
        root = Branch(titulo, narrativa, evento)
        self.root = root
        self.nodes[root.id] = root
        return root

    def connect(self, origin, key, texto, target=None, evento=None):
        choice = Choice(texto=texto, target=target, evento=evento)
        origin.choices[key] = choice

        if target is not None:
            target.parents.append(origin)

"""
A referência da opção: pode ser passado o target, que é a referência para o próximo point narrativo.
No caso, o target pode "duplicar", entao, dois points podem levar a um mesmo point, fazendo disso, um grafo.

A estrutura narrativa, em sua maior parte, é linear, mas em alguns pontos, próximos dos bosses do jogo, convergem. Por isso, a necessidade de criar algo desse tipo.
"""
class Choice:
    def __init__(self, texto, target=None, condicao=None, evento=None):
        self.texto = texto
        self.target = target
        self.condicao = condicao
        self.evento = evento
