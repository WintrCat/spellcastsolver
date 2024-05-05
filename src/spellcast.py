from collections import deque
from src.board import Board
from src.tile import TileModifier
from src.searchnode import SearchNode
from src.dictionary import get_dictionary, parse_key

dictionary = get_dictionary()

class Spellcast(Board):
    def legal_moves_from(self, x: int, y: int):
        legal_move_nodes: list[SearchNode] = []

        frontier: deque[SearchNode] = deque()
        frontier.append(
            SearchNode(None, self.tile_at(x, y))
        )

        while len(frontier) > 0:
            current_node = frontier.pop()

            adjacent_tiles = self.adjacent_tiles(current_node.x, current_node.y)

            for adjacent_tile in adjacent_tiles:
                if TileModifier.FROZEN in adjacent_tile.modifiers:
                    continue

                if current_node.chain_contains(adjacent_tile.x, adjacent_tile.y):
                    continue

                adjacent_node = SearchNode(current_node, adjacent_tile)
                adjacent_word = parse_key(adjacent_node.word())

                if not dictionary.has_subtrie(adjacent_word):
                    continue

                if dictionary.has_key(adjacent_word):
                    legal_move_nodes.append(adjacent_node)

                frontier.append(adjacent_node)

        return legal_move_nodes
    

    def legal_moves(self, sort_key = None, sort_reverse: bool = True):
        legal_move_nodes: list[SearchNode] = []

        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                legal_move_nodes += self.legal_moves_from(x, y)

        if sort_key is not None:
            legal_move_nodes.sort(key=sort_key, reverse=sort_reverse)

        return legal_move_nodes