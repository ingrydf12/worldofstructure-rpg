# Still working
from decision_tree import DecisionBinaryTree
from player import Player
from class_stats import CLASS_STATS

# Evento de exemplo
def evento_batalha(player):
    print("Um inimigo aparece! Prepare-se para a batalha!")

def main():
    print("Bem-vindo ao TormStructure RPG!")

    # Criar jogador
    nome = input("Digite o nome do seu herói: ")
    print("Escolha sua classe:")
    for c in CLASS_STATS:
        print(f"- {c}")
    classe = input("Classe: ")

    player = Player(class_type=classe, name=nome)

    tree = DecisionBinaryTree(player)
 
    # MARK: - RAIZ
    raiz = tree.insert(
        parent=None,
        titulo="Início da Aventura",
        narrativa=f"Em uma vasta floresta amazônica, vinhas esverdeadas e névoas densas preenchem o ambiente. você, {player.name}, é um {player.class_type}, nascido nas Américas, aceitou um desafio de explorar terras estrangeiras, mas por algum motivo, capangas atacaram o seu barco e te levaram a outro local sem que você conseguisse se defender. Ao acordar, uma luz de fim de tarde fracamente ilumina as árvores acima. Para todos os lados, existem vagalumes esverdeados cobertos pela névoa, mas ao final do seu lado esquerdo, você enxerga uma luz amarelada, enquanto que em suas costas parece existir um caminho mais abaixo na floresta, mas levemente escurecido. Para onde você decide ir?",
        lado="esquerda"
    )
    tree.root = raiz

    caminho1 = tree.insert(
        parent=raiz,
        titulo="Seguir a luz",
        narrativa="Você caminha um pouco, com cautela, pois você passa por um pequeno riacho de correnteza calma e pedras lisas. Água limpa corre nele. Do outro lado da margem, você vê uma casa de madeira, a porta está entreaberta e aquela luz anterior certamente vinha dela. Você vai investigar a casa ou seguir a trilha próxima a ela?",
        lado="esquerda",
        opcao_texto="Seguir a luz"
    )

    caminho2 = tree.insert(
        parent=raiz,
        titulo="Caminhar para o fundo",
        narrativa="-",
        lado="direita",
        opcao_texto="Ir pelo caminho do fundo",
        evento=evento_batalha
    )

    player.move_to(raiz)

    if raiz.left:
        print(f"1 - {raiz.opcao_esquerda}")
    if raiz.right:
        print(f"2 - {raiz.opcao_direita}")

if __name__ == "__main__":
    main()