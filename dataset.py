import os
import re
from datasets import load_dataset

DATASET_NAME = "wikitext-103-v1"
# DATASET_NAME = "wikitext-2-v1"

TMP_FOLDER = "tmp"

FILE_PATH = os.path.join(TMP_FOLDER, f"{DATASET_NAME}.txt")


def load_words():
    print("start loading")
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH) as f:
            print("open file")
            words = f.read().split()
    else:
        dataset = load_dataset("wikitext", DATASET_NAME)

        words = []
        for line in dataset["train"]["text"]:
            words += re.sub(r"[^\w\s]", "", line.lower()).split()

        os.makedirs(TMP_FOLDER, exist_ok=True)
        with open(FILE_PATH, mode="w") as f:
            f.write(" ".join(words))

    print("return word list")
    return words
