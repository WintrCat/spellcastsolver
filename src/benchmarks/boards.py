from time import time
from src.spellcast import Spellcast
from src.searchnode import SearchNode

### CONFIGURATION ###
BOARD_COUNT = 100
TRIPLE_LETTER_TILES = False
GEMS = 0
#####################


def main():
    start_time = time()

    total_score = 0
    top_move: SearchNode = None
    top_move_board: Spellcast = None

    for i in range(BOARD_COUNT):
        if i % 10 == 0:
            print(f"processed {i} boards...")

        board = Spellcast()
        board.gems = GEMS
        board.load_random(5, 5, TRIPLE_LETTER_TILES)

        top_moves = board.legal_moves(lambda node: node.score())

        if top_move is None or top_moves[0].score() > top_move.score():
            top_move = top_moves[0]
            top_move_board = board

        total_score += top_moves[0].score()

    # RESULTS
    benchmark_time = round(time() - start_time, 3)

    print("\nBENCHMARK RESULTS")
    print(f"{BOARD_COUNT} boards were processed")

    print("\nPERFORMANCE")
    print(f"The entire benchmark took {benchmark_time} seconds")
    print(
        "with an average time spent per board of "
        + f"{round(benchmark_time / BOARD_COUNT, 3)} seconds"
    )

    print("\nSCORES")
    print(
        "The computer earnt an average of "
        + f"{round(total_score / BOARD_COUNT, 1)} points per move"
    )
    print(
        "The highest scoring move found: "
        + top_move.to_string(top_move_board)
    )
    print("which was found on this board:")
    print(str(top_move_board))
