from loadModel import generateCards
from card_format.japanese_word import formatCard, Cards
import sys

if __name__ == "__main__":
    list = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    generateCards("japanese_word", list, Cards.model_json_schema(), formatCard)