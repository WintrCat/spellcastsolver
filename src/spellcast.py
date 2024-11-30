from collections import deque
from src.board import Board
from src.tile import TileModifier
from src.searchnode import SearchNode
from src.gems import AVERAGE_SCORES, AVERAGE_NET_GEM_PROFITS, gem_value
import src.dictionary as dictionary
from json import load
from multiprocessing import Pool

config = load(open("config.json"))


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

            # cache current node information
            current_node_cache = {
                "word": "",
                "positions": set(),
                "swap_count": 0
            }

            for node in current_node.chain():
                current_node_cache["positions"].add(
                    "".join([str(node.x), str(node.y)])
                )
                current_node_cache["word"] += node.letter
                
                if node.swap:
                    current_node_cache["swap_count"] += 1

            # get tiles adjacent to current tile
            adjacent_tiles = self.adjacent_tiles(current_node.x, current_node.y)

            for adjacent_tile in adjacent_tiles:
                # If the adjacent tile is frozen, do not create branch to it
                if TileModifier.FROZEN in adjacent_tile.modifiers:
                    continue

                # If the adjacent node is part of the current node's chain, skip it
                serialised_position = "".join([str(adjacent_tile.x), str(adjacent_tile.y)])
                if serialised_position in current_node_cache["positions"]:
                    continue

                # Create search node from adjacent tile
                adjacent_node = SearchNode(current_node, adjacent_tile)
                adjacent_word = current_node_cache["word"] + adjacent_node.letter

                # If the adjacent node makes a valid word, record it
                if dictionary.has_word(adjacent_word):
                    legal_move_nodes.append(adjacent_node)

                # add branch if words can begin with this prefix
                if dictionary.has_prefix(adjacent_word):
                    frontier.append(adjacent_node)

                # add possible swaps if there are enough gems
                if self.gems < (current_node_cache["swap_count"] + 1) * 3:
                    continue

                for swap_letter in dictionary.alphabet:
                    if swap_letter == adjacent_node.letter:
                        continue

                    if not dictionary.has_prefix(current_node_cache["word"] + swap_letter):
                        continue

                    swap_node = SearchNode(
                        current_node,
                        adjacent_tile,
                        True
                    )
                    swap_node.letter = swap_letter
                    
                    frontier.append(swap_node)        

        return list(legal_move_nodes)
    

    def legal_moves(self, sort_key = None, sort_reverse: bool = True):
        legal_move_nodes: list[SearchNode] = []

        # Record all legal moves from all root tiles on the board
        pool = Pool()
        pool_results = []

        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if TileModifier.FROZEN in self.tile_at(x, y).modifiers:
                    continue

                if config["multiProcessing"]:
                    pool_results.append(
                        pool.apply_async(self.legal_moves_from, (x, y))
                    )
                else:
                    legal_move_nodes.extend(
                        self.legal_moves_from(x, y)
                    )

        for pool_result in pool_results:
            legal_move_nodes.extend(pool_result.get())

        pool.terminate()

        # Remove duplicates, only keeping the best copies of each word
        unique_move_map: dict[str, SearchNode] = {}
        for legal_move_node in legal_move_nodes:
            # cache legal move node attributes
            legal_move_cache = {
                "word": "",
                "swap_count": 0
            }

            for node in legal_move_node.chain():
                legal_move_cache["word"] += node.letter
                
                if node.swap:
                    legal_move_cache["swap_count"] += 1

            legal_move_score = legal_move_node.score()

            # assert that a move with this word already exists
            existing_move_node = unique_move_map.get(legal_move_cache["word"])

            if existing_move_node is None:
                unique_move_map[legal_move_cache["word"]] = legal_move_node
                continue

            existing_move_score = existing_move_node.score()
            existing_move_swap_count = existing_move_node.swap_count()

            # if the score of this move is better than existing one
            if legal_move_score > existing_move_score:
                unique_move_map[legal_move_cache["word"]] = legal_move_node
                continue
            elif legal_move_score < existing_move_score:
                continue
            
            # replace if this move requires less swaps
            if legal_move_cache["swap_count"] < existing_move_swap_count:
                unique_move_map[legal_move_cache["word"]] = legal_move_node
                continue
            elif legal_move_cache["swap_count"] > existing_move_swap_count:
                continue

            # replace if swaps are same but this move has more gems
            if legal_move_node.gem_count() > existing_move_node.gem_count():
                unique_move_map[legal_move_cache["word"]] = legal_move_node

        legal_move_nodes = list(unique_move_map.values())

        # Sort the moves list by a provided key
        if sort_key is not None:
            legal_move_nodes.sort(key=sort_key, reverse=sort_reverse)

        return legal_move_nodes
    

    def evaluate_shuffle(self, top_move: SearchNode) -> tuple[int, bool]:
        if self.gems == 0:
            return (0, False)

        simulated_score = 0
        simulated_gems = self.gems - 1
        next_round_gem_count = 0

        # simulate a shuffle and the next round
        for round_index in range(min(2, 6 - self.match_round)):
            simulated_score += AVERAGE_SCORES[int(simulated_gems / 3)]
            simulated_gems += AVERAGE_NET_GEM_PROFITS[int(simulated_gems / 3)]
            
            if round_index == 0:
                next_round_gem_count = simulated_gems

        # add value of leftover gems
        if self.match_round < 4:
            simulated_score += gem_value(next_round_gem_count)

        # add value of remaining gems for last round
        if self.match_round == 5:
            simulated_score += simulated_gems

        # get value of the spent shuffle gem
        shuffle_gem_value = gem_value(self.gems) - gem_value(self.gems - 1)

        # return the estimated long term score and
        # whether a shuffling recommendation should be made
        return (
            simulated_score,
            simulated_score > (
                top_move.estimated_long_term_score(self)
                + shuffle_gem_value
            )
        )