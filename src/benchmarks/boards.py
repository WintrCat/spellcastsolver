from time import time
import matplotlib.pyplot as plt
from src.spellcast import Spellcast
from src.searchnode import SearchNode

### CONFIGURATION ###
BOARD_COUNT = 100
TRIPLE_LETTER_TILES = False
GEMS = 9
#####################


def main():
    start_time = time()

    best_moves: list[SearchNode] = []
    best_move_boards: list[Spellcast] = []

    for i in range(BOARD_COUNT):
        if i % 10 == 0:
            print(f"processed {i} boards...")

        board = Spellcast()

        board.gems = GEMS
        board.load_random(5, 5, TRIPLE_LETTER_TILES)

        top_moves = board.legal_moves(lambda node: node.estimated_long_term_score(board))

        best_moves.append(top_moves[0])
        best_move_boards.append(board)

    # calculate results
    benchmark_time = round(time() - start_time, 3)

    average_score = round(
        sum([move.score() for move in best_moves]) 
        / BOARD_COUNT,
        1
    )

    average_net_gem_profit = round(
        sum([move.net_gem_profit() for move in best_moves]) 
        / BOARD_COUNT,
        1
    )

    best_move = max(*best_moves, key=lambda move: move.score())
    best_move_board = best_move_boards[best_moves.index(best_move)]

    # plot distribution graphs
    # score distribution
    plt.xlabel("Score (Truncated)")
    plt.ylabel("Frequency")

    best_move_scores = [node.score() for node in best_moves]
    unique_best_move_scores = list(set(best_move_scores))

    plt.bar(
        unique_best_move_scores,
        [
            best_move_scores.count(score)
            for score in unique_best_move_scores
        ]
    )

    plt.savefig("src/benchmarks/scores.png")
    plt.clf()

    # net gem profit distribution
    plt.xlabel("Net Gem Profit")
    plt.ylabel("Frequency")

    best_move_gem_profits = [node.net_gem_profit() for node in best_moves]
    unique_best_move_gem_profits = list(set(best_move_gem_profits))

    plt.bar(
        unique_best_move_gem_profits,
        [
            best_move_gem_profits.count(gem_profit)
            for gem_profit in unique_best_move_gem_profits
        ]
    )

    plt.savefig("src/benchmarks/net_gem_profits.png")
    plt.clf()

    # display results
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
        + f"{average_score} points per move"
    )
    print(
        "The highest scoring move found: "
        + best_move.to_string(best_move_board)
    )
    print("which was found on this board:")
    print(str(best_move_board))

    print("\nGEMS")
    print(
        "The average net gem profit per move was "
        + str(average_net_gem_profit)
    )
