from time import time
from json import load
from functools import cmp_to_key
from src.spellcast import Spellcast
from src.searchnode import SearchNode

start_time = time()

config = load(open("config.json"))

game = Spellcast()
game.load_file("board.txt")

def compare_moves(a: SearchNode, b: SearchNode):
    a_score = a.estimated_long_term_score(game)
    b_score = b.estimated_long_term_score(game)

    difference = a_score - b_score
    if difference == 0:
        return a.gem_count() - b.gem_count()
    else:
        return difference


if __name__ == "__main__":
    print("searching for moves...")

    best_moves = game.legal_moves(
        cmp_to_key(compare_moves)
        if config["gemManagement"]
        else SearchNode.score
    )

    if config["logResults"]:
        found_words = [move.word() for move in best_moves]
        found_words.sort(reverse=True, key=len)

        log_file = open("results.log", "w")

        log_file.write("\n".join(found_words))
        log_file.close()

    shuffle_score, shuffle_recommended = game.evaluate_shuffle(best_moves[0])

    if shuffle_recommended:
        print(f"engine recommends shuffling - {shuffle_score} estimated value")

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
