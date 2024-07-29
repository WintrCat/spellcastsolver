from sys import argv
from src.benchmarks.boards import main as boards
from src.benchmarks.games import main as games

benchmark = ""

if len(argv) >= 2:
    benchmark = argv[1]
else:
    benchmark = input("benchmark type (boards/games): ")

if benchmark == "boards":
    boards()
elif benchmark == "games":
    games()
else:
    print("invalid benchmark type provided.")
