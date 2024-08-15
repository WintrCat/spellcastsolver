from typing_extensions import Self
from json import load
from src.tile import Tile, TileModifier

config = load(open("config.json"))

# these values are derived from large benchmarks
AVERAGE_SCORES = [32.7, 57.5, 74, 86]
AVERAGE_NET_GEM_PROFITS = [2.8, 1, -0.8, -2.6]


class SearchNode(Tile):
    parent: Self | None

    letter: str
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
    

    def score(self, context = None):
        score = 0
        double_word_score = False

        gem_count = 0
        for chain_node in self.chain():
            score += chain_node.value()

            if TileModifier.DOUBLE_WORD in chain_node.modifiers:
                double_word_score = True

            if TileModifier.GEM in chain_node.modifiers:
                gem_count += 1

        if double_word_score:
            score *= 2

        if len(self.word()) >= 6:
            score += 10

        if context is not None and context.match_round == 5:
            score += gem_count

        return score


    def estimated_long_term_score(self, context):
        # simulate rounds with average scores
        simulated_gems = min(context.gems + self.net_gem_profit(), 10)
        simulated_score = self.score()

        for _ in range(5 - context.match_round):
            available_swaps = int(simulated_gems / 3)

            simulated_score += AVERAGE_SCORES[available_swaps]
            simulated_gems += AVERAGE_NET_GEM_PROFITS[available_swaps]

        # return long term value
        return round(simulated_score, 1)


    def net_gem_profit(self):
        return self.gem_count() - (self.swap_count() * 3)


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
