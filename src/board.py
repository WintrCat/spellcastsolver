from random import randint, choice
from src.tile import Tile, TileModifier

BoardTiles = list[list[Tile]]

class Board:
    tiles: BoardTiles
    gems: int

    def __init__(self, tiles: BoardTiles = [], gems: int = 0):
        self.tiles = tiles
        self.gems = gems


    def __str__(self):
        board_lines = []
        for row in self.tiles:
            board_lines.append(", ".join([
                str(tile) for tile in row
            ]))

        return "\n".join(board_lines)


    def load_file(self, file_path: str): 
        loaded_tiles: BoardTiles = []
        board_file = open(file_path).read().splitlines()

        for row_index, row in enumerate(board_file):
            if row.isdigit():
                self.gems = int(row)
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


    def load_random(self, width: int, height: int, include_triple_letters: bool = False):
        loaded_tiles: BoardTiles = []

        alphabet = list("abcdefghijklmnopqrstuvwxyz")

        # Add random letters to the board
        for y in range(height):
            loaded_row = []
            loaded_tiles.append(loaded_row)

            for x in range(width):
                loaded_row.append(
                    Tile(choice(alphabet), x, y)
                )
        
        # Apply modifiers to random selection of tiles
        loaded_tiles[randint(0, height - 1)][randint(0, width - 1)].modifiers.add(TileModifier.DOUBLE_WORD)

        loaded_tiles[randint(0, height - 1)][randint(0, width - 1)].modifiers.add(TileModifier.DOUBLE_LETTER)

        if include_triple_letters:
            while True:
                target_tile = loaded_tiles[randint(0, height - 1)][randint(0, width - 1)]

                if TileModifier.DOUBLE_LETTER not in target_tile.modifiers:
                    target_tile.modifiers.add(TileModifier.TRIPLE_LETTER)
                    break

        self.tiles = loaded_tiles


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