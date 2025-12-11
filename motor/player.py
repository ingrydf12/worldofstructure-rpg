from external_atributtes import Skeleton
from class_stats import CLASS_STATS

class Player(Skeleton):
    def __init__(self, class_type, name):
        if class_type not in CLASS_STATS:
            raise ValueError(f"Classe inválida: {class_type}")

        stats = CLASS_STATS[class_type]

        super().__init__(name, stats["life"], stats["attributes"])

        self.class_type = class_type
        # @docs O nó atual (vai ser usado pra mostrar a árvore pro jogador)
        self.current_branch = None
        # @docs LISTA: A lista vinculada ao histórico de açoes e itens (pensando em ser feito de forma nativa)
        self.history = []
        self.itens = None

        self.in_battle = False
        self.enemy = None
        
    def attack(self, target):
        dano = self.attributes.get("forca", 1)
        target.life -= dano
        print(f"{self.name} ataca {target.name} causando {dano} de dano!")

    def move_to(self, branch):
        self.current_branch = branch
        self.history.append(branch)
        print(branch.narrativa)

        if branch.evento:
            branch.evento(self)

    def is_alive(self):
        return self.life > 0

    def status(self):
        print(f"{self.name} - Vida: {self.life} | Classe: {self.class_type}")