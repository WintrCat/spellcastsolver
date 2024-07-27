letter_values = {
    "a": 1,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 1,
    "f": 5,
    "g": 3,
    "h": 4,
    "i": 1,
    "j": 7,
    "k": 6,
    "l": 3,
    "m": 4,
    "n": 2,
    "o": 1,
    "p": 4,
    "q": 8,
    "r": 2,
    "s": 2,
    "t": 2,
    "u": 4,
    "v": 5,
    "w": 5,
    "x": 7,
    "y": 4,
    "z": 8
}


class Tile:
    letter: str
    modifiers: set[str]
    x: int
    y: int

    def __init__(self, letter: str, x: int, y: int):
        self.letter = letter
        self.modifiers = set()
        self.x = x
        self.y = y

    
    def __str__(self):
        modifiers_string = "".join(self.modifiers)
        return f"{self.letter.upper()}{modifiers_string}"
    

    def value(self):
        value = letter_values[self.letter]

        for modifier in self.modifiers:
            match modifier:
                case TileModifier.DOUBLE_LETTER:
                    value *= 2
                    break
                case TileModifier.TRIPLE_LETTER:
                    value *= 3
                    break

        return value


class TileModifier:
    DOUBLE_WORD = "$"
    DOUBLE_LETTER = "+"
    TRIPLE_LETTER = "*"
    FROZEN = "#"
    GEM = "!"

    values = list("$+*#!")
