from typing_extensions import Self
from json import load
from src.tile import Tile, TileModifier
from src.gems import AVERAGE_SCORES, gem_value

config = load(open("config.json"))


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
            f"{self.word()} - {self.score(context)} points, "
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
            + (
                f"\n{self.pretty_word()}\n"
                if config["prettyPrint"]
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
    

    def pretty_word(self):
        # ANSI escape codes for colors
        RED = '\033[91m'
        RESET = '\033[0m'
        board = [(['█'] * 5) for _ in range(5)]

        for chain_node in self.chain():
            x, y = chain_node.x, chain_node.y

            if chain_node.swap:
                board[y][x] = f"{RED}{chain_node.letter}{RESET}"
            else:
                board[y][x] = chain_node.letter

        return "\n".join([
            " ".join(row)
            for row in board
        ])


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
        long_term_score = self.score(context)

        final_gem_count = min(10, context.gems + self.net_gem_profit())

        if context.match_round < 5:  
            long_term_score += AVERAGE_SCORES[final_gem_count // 3]

        if context.match_round < 4:
            long_term_score += gem_value(final_gem_count)

        return long_term_score


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
