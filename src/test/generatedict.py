dictionary = open("resources/dictionary.txt").read().splitlines()

cut_dictionaries: list[set[str]] = []

for i in range(2, 23):
    words = set()

    for word in dictionary:
        if (not word.isalpha()) or " " in word:
            continue

        words.add(word[:i].lower())

    cut_dictionaries.append(words)

for i, cut_dictionary in enumerate(cut_dictionaries):
    open(f"resources/wordlists/dictionary{i + 2}.txt", "w").write(
        "\n".join(list(cut_dictionary))
    )
