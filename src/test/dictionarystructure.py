from timeit import Timer

trie_timer = Timer("trie_dictionary.has_key('hello')", """
from pygtrie import StringTrie
from pickle import load, dump

def parse_key(key: str):
    return "/".join(list(key))

def get_trie_dictionary():
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
      
trie_dictionary = get_trie_dictionary()
""")

trie_result = trie_timer.timeit()
print(f"dictionary trie took {round(trie_result, 3)}s for 1,000,000 word lookups")

hash_set_timer = Timer("'hello' in hash_set_dictionary", """
hash_set_dictionary = set(
    open("resources/dictionary.txt").read().splitlines()
)
""")

hash_set_result = hash_set_timer.timeit()
print(f"dictionary hash set took {round(hash_set_result, 3)}s for 1,000,000 word lookups")