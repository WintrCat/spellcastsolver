# Spellcast Solver

A program that can find the top moves in any Discord Spellcast position. It supports the different tile score boosts, frozen tiles for Singleplayer levels, and can find moves that utilise swap boosts.

## 🚀 Running
### Prerequisites
- Python installed (3.12.1 was used in development)
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

`movesShown` The number of top moves that are shown. Defaults to 10.
`gemManagement` Toggles a gem management algorithm that when enabled will recommend moves that score less to collect more gems if it thinks you'll likely profit in the long term.

### Running
Once you have configured your board file, you can run the program with `python main.py`. You will be given the best moves in the position and the co-ordinates of any swaps necessary to play the move.

## 📊 Benchmarking
There is a script called `benchmark.py` which you can run to test the solver against a large
number of randomised Spellcast boards. You will be given a small report on how it performed, and can configure the benchmark at the top section of the script that it runs.