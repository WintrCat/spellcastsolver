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
                # If the adjacent tile is frozen, do not create branch to it
                if TileModifier.FROZEN in adjacent_tile.modifiers:
                    continue

                # If the adjacent node is part of the current node's chain, skip it
                if current_node.chain_contains(adjacent_tile.x, adjacent_tile.y):
                    continue

                adjacent_node = SearchNode(current_node, adjacent_tile)
                adjacent_word = parse_key(adjacent_node.word())

                # Skip this branch if no words can be started with it
                if not dictionary.has_subtrie(adjacent_word):
                    continue

                # If the adjacent node makes a valid word, record it
                if dictionary.has_key(adjacent_word):
                    legal_move_nodes.append(adjacent_node)

                frontier.append(adjacent_node)

        return legal_move_nodes
    

    def legal_moves(self, sort_key = None, sort_reverse: bool = True):
        legal_move_nodes: list[SearchNode] = []

        # Record all legal moves from all root tiles on the board
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                legal_move_nodes += self.legal_moves_from(x, y)

        # Remove duplicates, only keeping the best copies of each word
        unique_move_map = {}
        for legal_move_node in legal_move_nodes:
            legal_move_word = legal_move_node.word()
            existing_move_node = unique_move_map.get(legal_move_word)

            if existing_move_node is None:
                unique_move_map[legal_move_word] = legal_move_node
            elif legal_move_node.score() > existing_move_node.score():
                unique_move_map[legal_move_word] = legal_move_node
            elif (
                legal_move_node.score() == existing_move_node.score()
                and legal_move_node.swap_count() < existing_move_node.swap_count()
            ):
               unique_move_map[legal_move_word] = legal_move_node

        legal_move_nodes = list(unique_move_map.values())

        # Sort the moves list by a provided key
        if sort_key is not None:
            legal_move_nodes.sort(key=sort_key, reverse=sort_reverse)

        return legal_move_nodes