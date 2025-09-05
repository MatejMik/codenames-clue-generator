import settings

import argparse
import logging

from model import find_clues


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="[%(asctime)s] %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find a clue word that is close to "target" words but not to "avoid" words.'
    )
    parser.add_argument(
        "--target", nargs="+", required=True, help="Finds a clue for these words"
    )
    parser.add_argument(
        "--avoid", nargs="*", default=[], help="Ensures the clue is not for these words"
    )
    args = parser.parse_args()

    clues = find_clues(args.target, args.avoid)

    if not clues:
        print("Could not find a clue for the given words")
    else:
        print(
            f"Found {len(clues)} candidate"
            + ("s" if len(clues) > 1 else "")
            + " for a clue:"
        )
        print(*clues, sep="\n")
