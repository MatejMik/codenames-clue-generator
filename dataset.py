import logging
import os
import re
from datasets import load_dataset

DATASET_NAME = "wikitext-103-v1"

# a much smaller dataset that gives worse results, but runs faster
# DATASET_NAME = "wikitext-2-v1"

TMP_FOLDER = "tmp"

FILE_PATH = os.path.join(TMP_FOLDER, f"{DATASET_NAME}.txt")


def load_words():
    if os.path.exists(FILE_PATH):
        logging.info("Loading the dataset from a local file.")
        with open(FILE_PATH) as f:
            words = f.read().split()
    else:
        logging.info(
            "Dataset not found locally. Starting download, this may take a minute."
        )
        dataset = load_dataset("wikitext", DATASET_NAME)

        logging.info("Finished downloading the dataset. Starting to clean it up.")
        words = []
        for line in dataset["train"]["text"]:
            words += re.sub(r"[^\w\s]", "", line.lower()).split()

        logging.info("Finished clean up. Saving the dataset to a local file.")
        os.makedirs(TMP_FOLDER, exist_ok=True)
        with open(FILE_PATH, mode="w") as f:
            f.write(" ".join(words))

    return words
