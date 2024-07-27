from time import time
from json import load
from src.spellcast import Spellcast

config = load(open("config.json"))

start_time = time()

game = Spellcast()
game.load_file("board.txt")

best_moves = game.legal_moves(lambda node: (
    node.estimated_long_term_score(game)
    if config["gemManagement"]
    else node.score()
))

print("\n".join([
    f"{i + 1} > {node.to_string(game)}"
    for i, node in enumerate(
        best_moves[:config["movesShown"]]
    )
]))

print(
    f"found {len(best_moves)} words"
    + f" in {round(time() - start_time, 2)} seconds."
)
