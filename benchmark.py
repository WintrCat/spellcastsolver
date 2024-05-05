from time import time
from src.spellcast import Spellcast

### CONFIGURATION ###
BOARD_COUNT = 1000
TRIPLE_LETTER_TILES = True
GEMS = 0
#####################

start_time = time()

total_score = 0
top_score = 0
top_scoring_word = ""
top_scoring_board = None

for i in range(BOARD_COUNT):
    if i % 10 == 0:
        print(f"processed {i} boards...")

    board = Spellcast()
    board.gems = GEMS
    board.load_random(5, 5, TRIPLE_LETTER_TILES)

    top_moves = board.legal_moves(lambda node : node.score())

    top_move_word = top_moves[0].word()
    top_move_score = top_moves[0].score()

    if top_move_score > top_score:
        top_score = top_move_score
        top_scoring_word = top_move_word
        top_scoring_board = board

    total_score += top_move_score
    
### RESULTS ###
benchmark_time = round(time() - start_time, 3)

print(f"\nBENCHMARK RESULTS")
print(f"{BOARD_COUNT} boards were processed")

print("\nPERFORMANCE")
print(f"The entire benchmark took {benchmark_time} seconds")
print(f"with an average time spent per board of {round(benchmark_time / BOARD_COUNT, 3)} seconds")

print("\nSCORES")
print(f"The computer earnt an average of {round(total_score / BOARD_COUNT, 1)} points per move")
print(f"The highest scoring move found was {top_scoring_word} for {top_score} points")
print("which was found on this board:")
print(str(top_scoring_board))