from random import randint, choice
from src.tile import Tile, TileModifier
from src.searchnode import SearchNode
import src.dictionary as dictionary

BoardTiles = list[list[Tile]]

class Board:
    tiles: BoardTiles
    gems: int = 0
    match_round: int = 0


    def flat_packed_tiles(tiles: BoardTiles):
        flat_packed_tiles = []
        for row in tiles:
            for tile in row:
                flat_packed_tiles.append(tile)

        return flat_packed_tiles


    def __init__(self, tiles: BoardTiles = [], gems: int = 0):
        self.tiles = tiles
        self.gems = gems


    def __str__(self):
        board_lines = []
        for row in self.tiles:
            board_lines.append(", ".join([
                str(tile) for tile in row
            ]))

        return (
            "\n".join(board_lines)
            + f"\n{self.gems} gems"
        )


    def load_file(self, file_path: str): 
        loaded_tiles: BoardTiles = []
        board_file = open(file_path).read().splitlines()
        
        digit_row_index = 0

        for row_index, row in enumerate(board_file):
            if row.isdigit():
                if digit_row_index == 0:
                    self.gems = int(row)
                elif digit_row_index == 1:
                    self.match_round = int(row)

                digit_row_index += 1
                continue

            loaded_row = []
            loaded_tiles.append(loaded_row)

            for char in row:
                if char in TileModifier.values:
                    if len(loaded_row) == 0:
                        continue
                    
                    loaded_row[-1].modifiers.add(char)
                else:
                    loaded_row.append(
                        Tile(char.lower(), len(loaded_row), row_index)
                    )

        self.tiles = loaded_tiles


    def load_random(
        self,
        width: int,
        height: int,
        include_triple_letters: bool = False
    ):
        loaded_tiles: BoardTiles = []

        # Add random letters to the board
        for y in range(height):
            loaded_row = []
            loaded_tiles.append(loaded_row)

            for x in range(width):
                loaded_row.append(
                    Tile(choice(dictionary.alphabet), x, y)
                )

        # Apply modifiers to random selection of tiles
        word_boost_tile = loaded_tiles[randint(0, height - 1)][randint(0, width - 1)]
        word_boost_tile.modifiers.add(TileModifier.DOUBLE_WORD)

        letter_boost_tile = loaded_tiles[randint(0, height - 1)][randint(0, width - 1)]
        letter_boost_tile.modifiers.add(
            TileModifier.TRIPLE_LETTER
            if include_triple_letters
            else TileModifier.DOUBLE_LETTER
        )

        # Apply gems to 10 random tiles
        flat_packed_tiles = Board.flat_packed_tiles(loaded_tiles)

        for _ in range(10):
            selected_tile = choice(flat_packed_tiles)
            selected_tile.modifiers.add(TileModifier.GEM)

            flat_packed_tiles.remove(selected_tile)

        # Set tiles to randomised board
        self.tiles = loaded_tiles
        
       
    def play_move(self, move: SearchNode):
        tile_chain = [
            self.tile_at(node.x, node.y) for node in move.chain()
        ]
        
        gem_count = move.gem_count()
        
        # Change letters and redistribute letter boost
        held_letter_boost = None
        
        for tile in tile_chain:
            tile.letter = choice(dictionary.alphabet)
            tile.modifiers.discard(TileModifier.GEM)
            
            if TileModifier.DOUBLE_LETTER in tile.modifiers:
                held_letter_boost = TileModifier.DOUBLE_LETTER
            elif TileModifier.TRIPLE_LETTER in tile.modifiers:
                held_letter_boost = TileModifier.TRIPLE_LETTER
                
            tile.modifiers.discard(TileModifier.DOUBLE_LETTER)
            tile.modifiers.discard(TileModifier.TRIPLE_LETTER)
            
        if held_letter_boost is not None:
            selected_tile = choice(Board.flat_packed_tiles(self.tiles))
            selected_tile.modifiers.add(held_letter_boost)
            
        # Redistribute gems to return to 10 total
        for _ in range(gem_count):
            selected_tile = choice(tile_chain)
            selected_tile.modifiers.add(TileModifier.GEM)
            
            tile_chain.remove(selected_tile)
            
        # Remove double word boost and redistribute
        flat_packed_tiles = Board.flat_packed_tiles(self.tiles)
        
        for tile in flat_packed_tiles:
            if TileModifier.DOUBLE_WORD in tile.modifiers:
                tile.modifiers.discard(TileModifier.DOUBLE_WORD)
                break
                
        choice(flat_packed_tiles).modifiers.add(
            TileModifier.DOUBLE_WORD
        )
        
        # Add gems, increment match round
        self.gems += gem_count - (move.swap_count() * 3)
        self.match_round += 1
        

    def tile_at(self, x: int, y: int):
        try:
            return self.tiles[y][x]
        except:
            return None
    

    def adjacent_tiles(self, x: int, y: int):
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue

                adjacent_x = x + x_offset
                adjacent_y = y + y_offset
                if adjacent_x < 0 or adjacent_y < 0:
                    continue

                adjacent_tile = self.tile_at(adjacent_x, adjacent_y)
                if adjacent_tile is not None:
                    yield adjacent_tile