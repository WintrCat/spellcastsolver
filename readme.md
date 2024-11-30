# 🌹 Spellcast Solver

The strongest Discord Spellcast engine in the world (probably).

The program is able to find the best moves on any Spellcast board and supports:
- Tile boosts like double word and letter score etc.
- Frozen tiles for use in the Adventure mode
- Moves that use 1 to 3 tile swaps
- Trading points for gems for a long-term advantage
- Recommending shuffling on low-scoring boards

## 📈 Results
- 2v2's mode team score world record holder with 605 points
- 2v2's game between 4 engines: world record total combined score of 1,206 points
- High score achieved in solo games of 356 points
- Average score of 57 points per 1-swap move, 74 points for 2 swaps

## 🚀 Running
### Prerequisites
- Python 3.10+ installed (older ones *should* be okay too)
- Basic experience with using a terminal

### Setup
- Use a terminal to `cd` to the project directory.
- Run `pip install -r requirements.txt` to install the necessary dependencies.

### Editing the board file
The state of the Spellcast board is stored in `board.txt` and you will need to edit it such that it matches the board in your game. Here is an example board file:
```
t*jfel
i!engv#
tan+lr
iy!nim
n+audo$!
6
3
```
Letters with `$` after them are double word score.
<br>
Letters with `+` after them are double letter score.
<br>
Letters with `*` after them are triple letter score.
<br>
Letters with `#` after them are frozen (cannot be used).
<br>
Letters with `!` after them have a gem attached. If you have gem management disabled, you can ignore this.
<br><br>
You can chain modifiers if you want; e.g `t+$` for a `T` tile with double letter score and double word score at the same time.
<br><br>
There are two numbers that go at the bottom of the file. The first is the number of gems that you have in the position, and the second is the round number. The round number will only be used when gem management is enabled, so you can omit this if you have it disabled.

### Configuration
There is a configuration file `config.json` where you can edit the bot's settings.

- `movesShown` The number of top moves that are shown.<br>
- `verboseOutput` Moves are shown with a grid that highlights the used tiles.
- `gemManagement` Toggles a gem management algorithm that when enabled will recommend moves that score less to collect more gems if it thinks you'll likely profit in the long term.<br>
- `multiProcessing` Spawns multiple Python processes to attempt to improve performance.

### Running
Once you have configured your board file, you can run the program with `python main.py`. You will be given the best moves in the position and the co-ordinates of any swaps necessary to play the move. For best performance, you may use an alternative Python runtime like PyPy.

## 📊 Benchmarking
There is a script called `benchmark.py` which you can use to run various benchmarks for the solver. It takes one command-line argument which is the type of benchmark you want to run; this can be one of the following values:

- `boards` Generates a specified number of random Spellcast boards, and finds the top move on them. Provides data on the average score per move, average gems received etc.
- `games` Generates a specified number of entire Spellcast games. An initial random board is created, and the top moves are simulated therein.

You can configure each benchmark by going into the `src/benchmarks` folder, finding the script behind the particular benchmark and editing the configuration variables at the top of the file.
