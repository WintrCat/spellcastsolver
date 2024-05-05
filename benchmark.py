from time import time
from src.spellcast import Spellcast
from src.searchnode import SearchNode

### CONFIGURATION ###
BOARD_COUNT = 20
TRIPLE_LETTER_TILES = True
GEMS = 6
#####################

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

    top_moves = board.legal_moves(lambda node : node.score())

    if top_move is None or top_moves[0].score() > top_move.score():
        top_move = top_moves[0]
        top_move_board = board

    total_score += top_moves[0].score()
    
### RESULTS ###
benchmark_time = round(time() - start_time, 3)

print(f"\nBENCHMARK RESULTS")
print(f"{BOARD_COUNT} boards were processed")

print("\nPERFORMANCE")
print(f"The entire benchmark took {benchmark_time} seconds")
print(f"with an average time spent per board of {round(benchmark_time / BOARD_COUNT, 3)} seconds")

print("\nSCORES")
print(f"The computer earnt an average of {round(total_score / BOARD_COUNT, 1)} points per move")
print(f"The highest scoring move found: {str(top_move)}")
print("which was found on this board:")
print(str(top_move_board))