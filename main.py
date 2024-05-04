from src.board import Board

board = Board()
board.load_file("board.txt")

print(str(board))
print("\n")
print([str(tile) for tile in board.adjacent_tiles(1, 0)])
