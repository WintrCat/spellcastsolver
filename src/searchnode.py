from typing_extensions import Self
from json import load
from src.tile import Tile, TileModifier

config = load(open("config.json"))

# these values are derived from large benchmarks that processed
# 50,000  5,000  500  100  boards respectively
AVERAGE_SCORES = [30.2, 52.7, 65.9, 78.7]
AVERAGE_NET_GEM_PROFITS = [2.8, 1, -0.8, -2.6]


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
    

    def score(self, context = None):
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

        if context is not None and context.match_round == 5:
            score += self.gem_count()

        return score


    def estimated_long_term_score(self, context):
        final_gem_count = min(
            (
                context.gems + self.gem_count()
                - (self.swap_count() * 3)
            ),
            10
        )

        average_next_score = (
            AVERAGE_SCORES[min(final_gem_count // 3, 3)]
            - AVERAGE_SCORES[0]
        )

        gem_bracket = final_gem_count // 3
        leftover_gem_value = int(
            ((final_gem_count % 3) / 3) * (
                AVERAGE_SCORES[min(gem_bracket + 1, 3)]
                - AVERAGE_SCORES[gem_bracket]
            )
        )

        if context.match_round == 5:
            average_next_score = 0

        if context.match_round > 3:
            leftover_gem_value = 0

        return round(
            self.score()
            + average_next_score
            + leftover_gem_value,
            1
        )
    

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
