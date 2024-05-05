from typing_extensions import Self
from src.tile import Tile, TileModifier

class SearchNode(Tile):
    parent: Self | None

    letter: str
    x: int
    y: int

    swap: bool

    def __init__(self, parent: Self, letter: str, x: int, y: int, swap: bool = False):
        super().__init__(letter, x, y)

        self.parent = parent
        self.swap = swap


    def __init__(self, parent: Self, tile: Tile, swap: bool = False):
        super().__init__(tile.letter, tile.x, tile.y)
        self.modifiers = tile.modifiers

        self.parent = parent
        self.swap = swap


    def __str__(self):
        return f"{self.word()} - {self.score()} points"


    def chain(self):
        nodes: list[Self] = [self]

        while nodes[0].parent != None:
            nodes.insert(0, nodes[0].parent)

        return nodes
    

    def chain_contains(self, x: int, y: int):
        for chain_node in self.chain():
            if chain_node.x == x and chain_node.y == y:
                return True
            
        return False
    

    def word(self):
        return "".join([
            chain_node.letter
            for chain_node in self.chain()
        ])
    

    def score(self):
        score = 0
        double_word_score = False

        for chain_node in self.chain():
            score += chain_node.value()

            if TileModifier.DOUBLE_WORD in chain_node.modifiers:
                double_word_score = True

        if double_word_score:
            score *= 2

        if len(self.word()) >= 6:
            score += 10

        return score
    

    def swap_count(self):
        return [
            chain_node.swap
            for chain_node in self.chain()
        ].count(True)
