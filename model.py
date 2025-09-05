from collections import Counter

from dataset import load_words

MIN_FREQ = 0.001
MOST_COMMON_WORDS_TO_IGNORE = 200


def count_neighbors(all_words, selected_words):
    neighbors = {}
    # print("start counting")
    for previous, current, next in zip(all_words[:-2], all_words[1:-1], all_words[:-2]):
        if current in selected_words:
            if current in neighbors:
                neighbors[current].update((previous, next))
            else:
                neighbors[current] = Counter((previous, next))

    # print("return neighbour counts")
    return neighbors


def find_clues(selected_words, anti_words):
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
        return min(frequencies[1:l]) / max(frequencies[l:] + (MIN_FREQ,))

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

    # print(
    #     *(
    #         " ".join(f"{x:.5f}" for x in numbers) + " " + word
    #         for (word, *numbers) in correct_choices
    #     ),
    #     sep="\n",
    # )

    excluded_hints = {
        key for key, _ in word_counter.most_common(MOST_COMMON_WORDS_TO_IGNORE)
    }
    correct_choices = [
        choice[0] for choice in correct_choices if choice[0] not in excluded_hints
    ]

    return correct_choices
