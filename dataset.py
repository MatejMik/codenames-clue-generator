import logging
import os
import re

from datasets import load_dataset
from settings import DATASET_FILE_PATH, DATASET_NAME, TMP_FOLDER


def load_words():
    if os.path.exists(DATASET_FILE_PATH):
        logging.info("Loading the dataset from a local file.")
        with open(DATASET_FILE_PATH) as f:
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
        with open(DATASET_FILE_PATH, mode="w") as f:
            f.write(" ".join(words))

    return words
