from time import time
from src.spellcast import Spellcast
from src.searchnode import SearchNode

### CONFIGURATION ###
BOARD_COUNT = 5000
TRIPLE_LETTER_TILES = False
GEMS = 3
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

    net_gem_profit_distribution = {}

    for i in range(-9, 11):
        net_gem_profit_distribution[str(i)] = 0

    for move in best_moves:
        net_gem_profit_string = str(move.net_gem_profit())
        net_gem_profit_distribution[net_gem_profit_string] += 1

    best_move = max(*best_moves, key=lambda move: move.score())
    best_move_board = best_move_boards[best_moves.index(best_move)]

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
    print(
        "Net profit gem distribution:\n"
        + "\n".join([
            (
                f"{net_gem_profit} gem profit - "
                + f"{net_gem_profit_distribution[net_gem_profit]} occurences"
            )
            for net_gem_profit in net_gem_profit_distribution
        ])
    )
