import sys

from argparse import ArgumentParser
from input_output import load_wordlist, write_wordsearch
from generator import generate_wordsearch


def main():
    parser = ArgumentParser()
    parser.add_argument("wordlist",
                        help="Path to line delimited file containing the wordlist")
    parser.add_argument("--answer_key", help="Path to file to write the answer key to")
    parser.add_argument("--grid_size",
                        help="Multiplier length of longest word for starting grid size",
                        default=1,
                        type=int)

    args = parser.parse_args()

    print "== Loading wordlist"
    with open(args.wordlist, "r") as wordlist_file:
        wordlist = load_wordlist(wordlist_file)

    print "== Generating wordsearch"
    wordsearch, answer_key = generate_wordsearch(wordlist, difficulty=args.grid_size)

    print "== Writing wordsearch"
    write_wordsearch(sys.stdout, wordsearch, wordlist)

    if args.answer_key:
        with open(args.answer_key, "w") as answer_key_file:
            write_wordsearch(answer_key_file, answer_key, wordlist)
