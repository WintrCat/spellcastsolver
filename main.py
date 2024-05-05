from time import time
from src.spellcast import Spellcast

game = Spellcast()
game.load_file("board.txt")

start_time = time()

best_moves = game.legal_moves(lambda node : node.score())

print("\n".join([
    str(node) for node in best_moves[:10]
]))
print(f"found {len(best_moves)} words in {round(time() - start_time, 2)} seconds.")