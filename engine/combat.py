# A estrutura de combate é que o jogador possa ecsolher usar o atributo pra bater de frente com o inimigo
# Todas as classes de player tem 3 atributos mínimos e o jogador pode escolher um deles para bater de frente com o atributo máximo do inimigo
# Terá um cálculo baseado em um dado de 6 + valor do atributo para bater de frente com sucesso ou derrota
# A derrota fará que o jogador tente novamente o combate ou recomece toda a narrativa

import random
from engine_input_reading import emit


class CombatState:
    def __init__(self, enemy):
        self.enemy = enemy
        self.turn = 0
        self.finished = False
        self.result = None
        self.last_turn = None


class CombatLoop:
    def __init__(self, enemy):
        self.enemy = enemy
        self.turn = 0
        self.finished = False
        self.branch_vitoria = None

    def start(self, player):
        player.current_combat = self
        player.in_battle = True
        player.push_history(f"Combate iniciado contra {self.enemy.name}")
        player.push_combat_actions(f"Combate iniciado contra {self.enemy.name}")

        self.emit_state(player)
        emit("EXPECTED_INPUT", "COMBAT_CHOICE")

    def step(self, player, atributo, acao):
        if self.finished:
            return

        self.turn += 1
        valor_jogador = player.attributes.get(atributo, 0)
        dado = random.randint(1, 6)
        poder = valor_jogador + dado

        _, valor_inimigo = self.enemy.max_attribute()

        if poder > valor_inimigo:
            dano = dado
            if acao == "ATAQUE":
                # o dano tem bonus pelo valor do dado
                dano += 1 * dado
                msg = f"Ataque certeiro! Causou {dano} de dano."
            else:
                msg = f"Defesa sólida! Contra-ataque causou {dano} de dano."

            self.enemy.life -= dano
            resultado = "SUCESSO"
            player.push_combat_actions(msg)
        else:
            dano_recebido = 2
            if acao == "DEFESA":
                dano_recebido = 1
                msg = "Falha, mas você se protegeu! Recebeu apenas 1 de dano."
            else:
                msg = "Tentativa de ataque frustrada! Recebeu 2 de dano."

            player.life -= dano_recebido
            resultado = "FALHA"
            player.push_combat_actions(msg)

        emit("DADO", dado)
        emit("RESULTADO_TURNO", resultado)

        self.emit_state(player)

        if not player.is_alive() or not self.enemy.is_alive():
            self.end(player)
        else:
            emit("EXPECTED_INPUT", "COMBAT_CHOICE")

    def emit_state(self, player):
        emit("GAME_STATE", "EM_COMBATE")
        emit("PLAYER_STATE", player.get_estado())
        emit("ENEMY_STATE", self.enemy.get_estado())
        emit(
            "COMBAT_STATE",
            {
                "turn": self.turn,
                "player": player.get_estado(),
                "enemy": self.enemy.get_estado(),
            },
        )

    def end(self, player):
        self.finished = True
        player.in_battle = False

        if player.is_alive():
            player.push_history(f"Vitória épica contra {self.enemy.name}!")

            emit("RESULTADO_COMBATE", "VITORIA")
            emit("GAME_STATE", "NARRATIVE")

            if self.branch_vitoria:
                player.push_history(f"Vitória. Você não deixa ninguém escapar. Matou {self.enemy.name}")
                self.branch_vitoria(player)
            else:
                player.push_combat_history(
                    "A jornada continua, mas o caminho é incerto (sem branch)."
                )
        else:
            player.push_history(
                f"Fim da linha: derrotado por {self.enemy.name} no turno {self.turn}."
            )
            emit("RESULTADO_COMBATE", "DERROTA")
