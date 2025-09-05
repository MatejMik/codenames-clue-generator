# Codenames Clue Generator

This is a simple project made to explore how clues (word associations) for the board game Codenames can be generated from english written text data by counting frequencies of neighboring words. The idea is that a word would be a good candidate for a clue if it often appears next to the words we have chosen.

## Usage

After installing dependencies listed in `requirements.txt` you can run the `main.py` script. First run will take longer because a dataset of about 500Mb has to be downloaded.

Use argument `--target` to specify the words you want to find a clue for. Optionally use also `--avoid` to specify words that should not be related to the clue.

## Examples

```
$ python main.py --target fox sun
Found 1 candidate for a clue:
red
```
```
$ python main.py --target fox sun -- avoid army
Could not find a clue for given words
```
```
$ python main.py --target road army wall
Found 2 candidates for a clue:
roman
main
```
```
$ python main.py --target road army wall --avoid man castle
Found 1 candidate for a clue:
roman
```