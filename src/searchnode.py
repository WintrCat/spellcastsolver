from typing_extensions import Self
from json import load
from src.tile import Tile, TileModifier

config = load(open("config.json"))

AVERAGE_SCORES = [33, 57, 71, 83]

class SearchNode(Tile):
    parent: Self | None

    letter: str
    x: int
    y: int

    swap: bool

    def __init__(self, parent: Self, tile: Tile, swap: bool = False):
        super().__init__(tile.letter, tile.x, tile.y)
        self.modifiers = tile.modifiers

        self.parent = parent
        self.swap = swap


    def to_string(self, context = None):
        swap_strings = []
        for chain_node in self.chain():
            if not chain_node.swap:
                continue

            swap_strings.append(
                f"swap to {chain_node.letter} at (x: {chain_node.x + 1}, y: {chain_node.y + 1})"
            )

        swap_details = ", ".join(swap_strings)

        return (
            f"{self.word()} - {self.score()} points, "
            + f"{self.gem_count()} gems"
            + (" - " if len(swap_strings) > 0 else "")
            + swap_details
            + (
                (
                    "\nestimated long term value: "
                    + str(self.estimated_long_term_score(context))
                )
                if (
                    config["gemManagement"]
                    and context is not None
                    and context.match_round < 5
                )
                else ""
            )
        )


    def chain(self):
        nodes: list[Self] = [self]

        while nodes[0].parent is not None:
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


    def estimated_long_term_score(self, context):
        final_gem_count = (
            context.gems + self.gem_count()
            - (self.swap_count() * 3)
        )

        average_next_score = (
            AVERAGE_SCORES[int(final_gem_count / 3)]
            - AVERAGE_SCORES[0]
        )

        if context.match_round == 5:
            average_next_score = 0

        return self.score() + average_next_score


    def gem_count(self):
        return [
            TileModifier.GEM in chain_node.modifiers
            for chain_node in self.chain()
        ].count(True)


    def swap_count(self):
        return [
            chain_node.swap
            for chain_node in self.chain()
        ].count(True)
