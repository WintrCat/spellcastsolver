class Tile:
    letter: str
    modifiers: list[str]

    def __init__(self, letter: str):
        self.letter = letter
        self.modifiers = []

    
    def __str__(self):
        modifiers_string = "".join(self.modifiers)
        return f"{self.letter.upper()}{modifiers_string}"


class TileModifier:
    DOUBLE_WORD = "$"
    DOUBLE_LETTER = "+"
    TRIPLE_LETTER = "*"
    FROZEN = "#"

    values = list("$+*#")