from collections import deque
from src.board import Board
from src.tile import TileModifier
from src.searchnode import SearchNode
import src.dictionary as dictionary

class Spellcast(Board):
    def legal_moves_from(self, x: int, y: int):
        legal_move_nodes: deque[SearchNode] = deque()

        frontier: deque[SearchNode] = deque()

        root_tile = self.tile_at(x, y)
        if self.gems >= 3:
            for letter in dictionary.alphabet:
                swapped_node = SearchNode(
                    None,
                    root_tile,
                    letter != root_tile.letter
                )
                swapped_node.letter = letter

                frontier.append(swapped_node)
        else:
            frontier.append(
                SearchNode(None, root_tile)
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

                # Create search node from adjacent tile
                adjacent_node = SearchNode(current_node, adjacent_tile)
                adjacent_word = adjacent_node.word()

                # If the adjacent node makes a valid word, record it
                if dictionary.has_word(adjacent_word):
                    legal_move_nodes.append(adjacent_node)

                # If no words start with this branch, add possible swaps
                if dictionary.has_prefix(adjacent_word):
                    frontier.append(adjacent_node)
                elif self.gems >= (current_node.swap_count() + 1) * 3:                    
                    for letter in dictionary.alphabet:
                        if letter == adjacent_node.letter:
                            continue

                        current_word = adjacent_word[:-1]
                        if not dictionary.has_prefix(current_word + letter):
                            continue

                        swap_node = SearchNode(
                            current_node,
                            adjacent_tile,
                            True
                        )
                        swap_node.letter = letter
                        
                        frontier.append(swap_node)

        return list(legal_move_nodes)
    

    def legal_moves(self, sort_key = None, sort_reverse: bool = True):
        legal_move_nodes: list[SearchNode] = []

        # Record all legal moves from all root tiles on the board
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if TileModifier.FROZEN in self.tile_at(x, y).modifiers:
                    continue
                
                legal_move_nodes += self.legal_moves_from(x, y)

        # Remove duplicates, only keeping the best copies of each word
        unique_move_map: dict[str, SearchNode] = {}
        for legal_move_node in legal_move_nodes:
            legal_move_word = legal_move_node.word()
            existing_move_node = unique_move_map.get(legal_move_word)

            if existing_move_node is None:
                unique_move_map[legal_move_word] = legal_move_node
            elif (
                legal_move_node.score() > existing_move_node.score()
                or (
                    legal_move_node.score() == existing_move_node.score()
                    and legal_move_node.swap_count() < existing_move_node.swap_count()
                )
            ):
                unique_move_map[legal_move_word] = legal_move_node

        legal_move_nodes = list(unique_move_map.values())

        # Sort the moves list by a provided key
        if sort_key is not None:
            legal_move_nodes.sort(key=sort_key, reverse=sort_reverse)

        return legal_move_nodes