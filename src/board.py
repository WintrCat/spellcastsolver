from src.utils import clamp
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

        for row in board_file:
            if row.isdigit():
                self.gems = int(row)
                continue

            loaded_row = []
            loaded_tiles.append(loaded_row)

            for char in row:
                if char in TileModifier.values:
                    if len(loaded_row) == 0:
                        continue
                    
                    loaded_row[-1].modifiers.append(char)
                else:
                    loaded_row.append(
                        Tile(char.lower())
                    )

        self.tiles = loaded_tiles


    def tile_at(self, x: int, y: int):
        try:
            return self.tiles[max(y, 0)][max(x, 0)]
        except:
            return None
    

    def adjacent_tiles(self, x: int, y: int):
        adjacent_tiles = []

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
                    adjacent_tiles.append(adjacent_tile)
        
        return adjacent_tiles