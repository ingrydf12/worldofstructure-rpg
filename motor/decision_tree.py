# @docs Arvore de decisão para exploração da narrativa
class Branch:
    def __init__(
        self, titulo, narrativa, opcao_esquerda=None, opcao_direita=None, evento=None
    ):
        self.parent = None
        self.titulo = titulo
        self.narrativa = narrativa

        self.opcao_esquerda = opcao_esquerda
        self.opcao_direita = opcao_direita

        self.left = None
        self.right = None

        self.evento = evento

    def show_tree(self, nivel=0):
        print("  " * nivel + f"• {self.narrativa}")
        if self.left:
            print("  " * (nivel + 1) + f"-> {self.opcao_esquerda}")
            self.left.show_tree(nivel + 2)

        if self.right:
            print("  " * (nivel + 1) + f"-> {self.opcao_direita}")
            self.right.show_tree(nivel + 2)


class DecisionBinaryTree:
    def __init__(self, player):
        self.root = None
        self.player = player


    def insert(self, parent, titulo, narrativa, lado, opcao_texto=None, evento=None):
        novo = Branch(titulo, narrativa, evento=evento)

        if parent is None:
            self.root = novo
            return novo

        if lado == "esquerda":
            if parent.left is not None:
                raise ValueError("O nó à esquerda já existe!")
            parent.left = novo
            novo.parent = parent
            parent.opcao_esquerda = opcao_texto

        elif lado == "direita":
            if parent.right is not None:
                raise ValueError("O nó à direita já existe!")
            parent.right = novo
            novo.parent = parent
            parent.opcao_direita = opcao_texto

        else:
            raise ValueError("O lado deve ser 'esquerda' ou 'direita'.")

        return novo

    