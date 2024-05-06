from pygtrie import StringTrie
from pickle import load, dump

def parse_key(key: str):
    return "/".join(list(key))


def get_dictionary():
    try:
        dictionaryCache: StringTrie = load(
            open("dictionary.pkl", "rb")
        )
        return dictionaryCache
    except:
        print("no dictionary trie found, generating one...")

    words = open("resources/dictionary.txt", "r").read().splitlines()

    dictionary = StringTrie()
    for word in words:
        dictionary[parse_key(word)] = True

    dump(dictionary, open("dictionary.pkl", "wb"))

    return dictionary