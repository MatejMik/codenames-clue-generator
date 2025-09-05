import logging

LOG_LEVEL = logging.DEBUG

# minimal frequency for a word to be considered as clue
#  (to avoid noise - misspelled or random words - from the dataset)
MIN_FREQUENCY = 0.001

# how many most common words will not be considered as clues
#  (to avoid vague clues like "the", "and", "on", ...)
IGNORE_MOST_COMMON = 200
