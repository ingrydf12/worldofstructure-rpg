from skeleton import Skeleton
from class_infos import CLASS_INFOS
from inventory import InventoryTree
import json
from engine_input_reading import emit

class Player(Skeleton):
    def __init__(self, class_type, name):
        if class_type not in CLASS_INFOS:
            raise ValueError(f"Classe inválida: {class_type}")

        stats = CLASS_INFOS[class_type]
        super().__init__(name, stats["life"], stats["attributes"])

        self.class_type = class_type
        self.current_branch = None
        self.current_combat = None

        # Estruturas: Tem duas pilhas, um histórico geral das runs e da atual
        self.history = []
        self.current_run = []
        self.world_state = {}
        
        # Estrutruras: essa lista marca todos as açoes e reaçoes do combate
        self.combat_actions = []

        self.inventory = InventoryTree()
        self.in_battle = False
        self.atributo_selecionado = None

        self.start_run()

    def start_run(self):
        self.current_run = []
        self.world_state = {}

        self.push_history("Run iniciada")

    def end_run(self):
        self.history.append(self.current_run.copy())
        self.current_run = []

    def restart_run(self):
        self.push_history("Você decidiu reiniciar a jornada")
        self.end_run()
        self.start_run()

    def push_history(self, evento):
        self.current_run.append(evento)
        
    def push_combat_actions(self, evento):
            self.combat_actions.append(evento)

    def get_estado(self):
        return {
            "name": self.name,
            "life": self.life,
            "class_type": self.class_type,
            "attributes": self.attributes,
            "inventory": self.inventory.listar_itens(),
            "in_battle": self.in_battle,
        }

    """O histórico é uma pilha, tem duas pilhas dentro do player: a run atual e um histórico das runs.
    Aqui é o state que é passado pro Tauri, que eu monto um json pra o front apenas consumir, já que ele vai ser emitido na engine e o Tauri vai receber e atualizar o context.
    """
    def emitir_runs(self):
        runs_payload = []

        for i, run in enumerate(self.history):
            runs_payload.append(
                {"run_id": i + 1, "class_type": self.class_type, "events": run}
            )

        emit("RUNS", runs_payload)

    # Função pra eu puxar no front do Tauri que puxa o estado do jogador
    def emitir_estado(self):
        print(f"PLAYER_STATE::{json.dumps(self.get_estado())}", flush=True)

    def escolher_atributo(self):
        if self.atributo_selecionado is None:
            return None
        escolhido = self.atributo_selecionado
        self.atributo_selecionado = None
        return escolhido

    def move_to(self, branch):
        if branch is None:
            raise ValueError("Tentativa de mover o jogador para um branch None")

        self.current_branch = branch
        self.push_history(f"Nó visitado: {branch.titulo}")

        self.emitir_estado()

    def status(self):
        print(f"STATUS::{self.name}|HP:{self.life}|CLS:{self.class_type}", flush=True)