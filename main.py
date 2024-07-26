from time import time
from json import load
from src.spellcast import Spellcast

config = load(open("config.json"))

start_time = time()

game = Spellcast()
game.load_file("board.txt")

best_moves = game.legal_moves(lambda node : node.score())

print("\n".join([
    f"{i + 1} > {str(node)}"
    for i, node in enumerate(
        best_moves[:config["movesShown"]]
    )
]))

print(f"found {len(best_moves)} words in {round(time() - start_time, 2)} seconds.")
        