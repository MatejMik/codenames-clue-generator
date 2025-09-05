import logging
from collections import Counter, defaultdict
from typing import Dict, List, Set

from dataset import load_words
from settings import MIN_FREQUENCY, IGNORE_MOST_COMMON


def count_neighbors(
    all_words: List[str], selected_words: Set[str]
) -> Dict[str, Counter]:
    """
    For each of the selected words counts all words that appear next to it.
    """

    logging.info(
        f"Starting to count neighboring word frequencies for words: {selected_words}"
    )

    neighbors = defaultdict(Counter)
    for previous, current, next in zip(all_words[:-2], all_words[1:-1], all_words[:-2]):
        if current in selected_words:
            neighbors[current].update((previous, next))

    logging.info("Finished counting neighboring word frequencies")

    return neighbors


def frequency(counter: Counter, word: str):
    return counter.get(word, 0) / counter.total()


def weight(word_frequencies):
    """
    Gives weight to words based on how frequently they appear
    next to "target" words over "avoid" words.
    """

    return min(word_frequencies["target_word_frequencies"]) / max(
        word_frequencies["avoid_word_frequencies"] + [MIN_FREQUENCY]
    )


def find_clues(target_words: List[str], avoid_words: List[str]) -> List[str]:
    """
    Returns all words that are candidates for a clue in order of most confidence.
    """
    target_words = [word.lower() for word in target_words]
    avoid_words = [word.lower() for word in avoid_words]

    training_text = load_words()
    input_words = set(target_words + avoid_words)
    neighbor_counts = count_neighbors(training_text, input_words)

    target_word_counters = [neighbor_counts.get(word) for word in target_words]
    avoid_word_counters = [neighbor_counts.get(word) for word in avoid_words]

    logging.info("Computing intersection of potential clues for target words")
    target_word_neighbors = set.intersection(
        *(set(counter.keys()) for counter in target_word_counters)
    )

    logging.info("Sorting potential clue words")
    words_with_frequencies = sorted(
        [
            {
                "word": word,
                "target_word_frequencies": [
                    frequency(counter, word) for counter in target_word_counters
                ],
                "avoid_word_frequencies": [
                    frequency(counter, word) for counter in avoid_word_counters
                ],
            }
            for word in target_word_neighbors
        ],
        key=weight,
        reverse=True,
    )

    logging.info("Counting all words to find most common ones")
    all_word_counts = Counter(training_text)

    most_common_words = {
        word for word, _ in all_word_counts.most_common(IGNORE_MOST_COMMON)
    }
    excluded_clues = most_common_words.union(input_words)

    logging.info("Filtering potential clue words")
    return [
        item["word"]
        for item in words_with_frequencies
        if weight(item) > 1 and item["word"] not in excluded_clues
    ]
