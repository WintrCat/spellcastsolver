alphabet = list("abcdefghijklmnopqrstuvwxyz")

dictionary = set(
    open("resources/dictionary.txt").read().splitlines()
)

cut_dictionaries = [
    set(
        open(f"resources/wordlists/dictionary{word_length}.txt").read().splitlines()
    )
    for word_length in range(2, 23)
]

def has_word(word: str):
    return word in dictionary


def has_prefix(prefix: str):
    prefix_length = len(prefix)

    if prefix_length < 2:
        return True

    return prefix in cut_dictionaries[prefix_length - 2]