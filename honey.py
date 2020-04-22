from collections import defaultdict
from itertools import combinations
from typing import Tuple, List, Dict


Honeycomb = Tuple[str, str]
Honeycombs = List[Honeycomb]
Mapping = Dict
Word = str
Wordlist = List[Word]


def all_letters(word: Word) -> bool:
    return len(set(word)) == 7


def word_score(word: Word) -> int:
    bonus = 7 if all_letters(word) else 0
    return (1 if len(word) is 4 else len(word) + bonus)


def in_honeycomb(word: Word, honeycomb: Honeycomb) -> bool:
    centre, letters = honeycomb
    return (centre in word) and all(l in letters for l in word)


def score(honeycomb: Honeycomb, words: Wordlist) -> int:
    vw = lambda x: in_honeycomb(x, honeycomb)
    valid_words = filter(vw, words)
    return sum(map(word_score, valid_words))


def gen_honeycomb(words: Wordlist) -> Honeycombs:
    letters = {fingerprint(word) for word in words if all_letters(word)}
    return [(c, lett) for lett in letters for c in lett]


def fingerprint(word: Word) -> str:
    return "".join(sorted(set(word)))


def map_fingerprint(words: Wordlist) -> Mapping:
    dict_map = defaultdict(int)
    for word in words:
        dict_map[fingerprint(word)] += word_score(word)
    return dict_map


def sub_honeycomb(honeycomb: Honeycomb) -> Wordlist:
    centre, letters = honeycomb
    return [fingerprint(word) for i in range(8)
            for word in combinations(letters, i) if centre in word]


def score_honeycomb(dict_map: Mapping, honeycomb: Honeycomb) -> int:
    return sum(dict_map[sub] for sub in sub_honeycomb(honeycomb))


def best_honeycomb(words: Wordlist, honeycombs: Honeycombs) -> Honeycomb:
    dict_map = map_fingerprint(words)
    return max(honeycombs, key=lambda x: score_honeycomb(dict_map, x))


if __name__ == "__main__":

    with open("data/enable1.txt", "r") as f:
        words = [w for w in f.read().split() if len(w) > 3]

    # calculate score of this honeycomb
    honeycomb = ("g", "galpemx")
    print(score(honeycomb, words))

    # calculate highest scoring honeycomb
    honeycombs = gen_honeycomb(words)
    print(best_honeycomb(words, honeycombs))
