# Inventário (Árvore binária) do personagem (rascunho)

class ItemNode:
    def __init__(self, item_id, nome, tipo, atributos=None):
        self.item_id = item_id
        self.nome = nome
        self.tipo = tipo
        self.atributos = atributos

        self.left = None
        self.right = None

class InventoryTree:
    def __init__(self):
        self.root = None

    def insert(self, item_node):
        if not self.root:
            self.root = item_node
        else:
            self._insert(self.root, item_node)

    def _insert(self, current, item):
        if item.item_id < current.item_id:
            if current.left:
                self._insert(current.left, item)
            else:
                current.left = item
        else:
            if current.right:
                self._insert(current.right, item)
            else:
                current.right = item

    def listar_itens(self):
        itens = []
        self._in_order(self.root, itens)
        return itens

    def _in_order(self, node, itens):
        if not node:
            return
        self._in_order(node.left, itens)
        itens.append(node.to_dict())
        self._in_order(node.right, itens)