import logging
from collections import Counter, defaultdict
from typing import Dict, List, Set

from dataset import load_words
from settings import MIN_FREQUENCY, IGNORE_MOST_COMMON


def count_neighbors(
    all_words: List[str], selected_words: Set[str]
) -> Dict[str, Counter]:
    logging.info(
        f"Starting to count neighboring word frequencies for words: {selected_words}"
    )

    neighbors = defaultdict(Counter)
    for previous, current, next in zip(all_words[:-2], all_words[1:-1], all_words[:-2]):
        if current in selected_words:
            neighbors[current].update((previous, next))

    logging.info("Finished counting neighboring word frequencies")

    return neighbors


def find_clues(selected_words: List[str], anti_words: List[str]) -> List[str]:
    words = load_words()
    neighbors = count_neighbors(words, set(selected_words + anti_words))

    word_counter = Counter(words)
    all_words = set(words)
    all_counters = []

    for word in selected_words:
        selected_neighbors = neighbors.get(word)
        all_counters.append(selected_neighbors)
        all_words = all_words.intersection(set(selected_neighbors.keys()))

    for word in anti_words:
        all_counters.append(neighbors.get(word))

    l = len(selected_words) + 1

    def weight(frequencies):
        return min(frequencies[1:l]) / max(frequencies[l:] + (MIN_FREQUENCY,))

    final_choices = sorted(
        [
            (
                w,
                *(counts.get(w, 0) / counts.total() for counts in all_counters),
            )
            for w in all_words
        ],
        key=weight,
        reverse=True,
    )

    correct_choices = [choice for choice in final_choices if weight(choice) > 1]

    most_common_words = {
        item[0] for item in word_counter.most_common(IGNORE_MOST_COMMON)
    }
    excluded_hints = most_common_words + selected_words

    correct_choices = [
        choice[0] for choice in correct_choices if choice[0] not in excluded_hints
    ]

    return correct_choices
