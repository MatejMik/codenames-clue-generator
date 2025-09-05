import logging
import os

LOG_LEVEL = logging.INFO

# minimal frequency for a word to be considered as clue
#  (to avoid noise - misspelled or random words - from the dataset)
MIN_FREQUENCY = 0.001

# how many most common words will not be considered as clues
#  (to avoid vague clues like "the", "and", "on", ...)
IGNORE_MOST_COMMON = 200

# large english written text taken from wikipedia articles
DATASET_NAME = "wikitext-103-v1"
# a much smaller alternative that gives much worse results, but runs faster
# DATASET_NAME = "wikitext-2-v1"

TMP_FOLDER = "tmp"
DATASET_FILE_PATH = os.path.join(TMP_FOLDER, f"{DATASET_NAME}.txt")
