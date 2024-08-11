from time import time
from src.spellcast import Spellcast

### CONFIGURATION ###
GAME_COUNT = 100
#####################

def main():
    start_time = time()

    total_score = 0

    best_game_score = 0
    best_game_moves = []

    for i in range(GAME_COUNT):
        print(f"processing {i} games...")

        game = Spellcast()

        # Keep track of score and moves
        game_score = 0
        game_moves = []

        # Setup initial state
        game.gems = 3
        game.match_round = 1
        game.load_random(5, 5)

        # Play game
        for _ in range(5):
            moves = game.legal_moves(
                sort_key=lambda node: node.estimated_long_term_score(game),
                sort_reverse=True
            )

            game_score += moves[0].score()
            game_moves.append(moves[0].to_string())

            game.play_move(moves[0])

        if game_score > best_game_score:
            best_game_score = game_score
            best_game_moves = game_moves

        total_score += game_score

    print("BENCHMARK COMPLETE")
    print(f"it took {round(time() - start_time, 3)}s to complete.")

    print(
        f"\non average, {round(total_score / GAME_COUNT, 1)}"
        + " points were scored per game."
    )
    print(f"the best game recorded achieved {best_game_score} points.")
    print("with the following moves:")
    print("\n".join(best_game_moves))
