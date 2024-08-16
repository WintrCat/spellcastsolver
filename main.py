from time import time
from json import load
from src.spellcast import Spellcast

start_time = time()

config = load(open("config.json"))

game = Spellcast()
game.load_file("board.txt")

print("searching for moves...")

best_moves = game.legal_moves(lambda node: (
    node.estimated_long_term_score(game)
    if config["gemManagement"]
    else node.score()
))

shuffle_score, shuffle_recommended = game.evaluate_shuffle(best_moves[0])

if shuffle_recommended:
    print(f"engine recommends shuffling - {shuffle_score} estimated points")

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
