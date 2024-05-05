from src.spellcast import Spellcast

game = Spellcast()
game.load_file("board.txt")

print("\n".join([
    str(node) for node in game.legal_moves(lambda node : node.score())[:10]
]))
