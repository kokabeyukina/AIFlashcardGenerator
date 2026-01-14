import json
import re
import sys
from pydantic import BaseModel

class SentenceWords(BaseModel):
    word: str
    meanings: list[str]

class Card(BaseModel):
    word: str
    hiragana_reading: str
    word_meaning: str
    example_sentence: str
    example_sentence_hiragana_reading: str
    example_sentence_translation: str
    explanation: list[SentenceWords]

class Cards(BaseModel):
    cards: list[Card]

def formatCard(data: dict) -> str:
    """
    Converts a JSON Object into the japanese_word class format.
    """
    if not isinstance(data, dict):
        data = json.loads(data)
    
    return "\n".join([re.sub(r'\s{2,}', '', f"""
        <h1 style="font-weight:100">{card["word"]}</h1>
        <br>
        <br>{card["example_sentence"]}
        |{getKanjiReading(card["word"])}
        <br>{card["word_meaning"]}
        <br>
        <br>{furiganaHTML(card["example_sentence"])}
        <br>{card["example_sentence_translation"]}
        <br>
        <br>{"<br>".join([o["word"]+" = "+"; ".join(o["meanings"]) for o in card["explanation"]])}
        <br>
        <br>
        <br>AI given reading:
        <br>{card["hiragana_reading"]}
        <br>{card["example_sentence_hiragana_reading"]}
    """) for card in data["cards"]])

    #cardList = []
    #for card in data["cards"]:
    #    cardList.append(re.sub(r'\s{2,}', '', f"""
    #        ...
    #    """))
    #return "\n".join(cardList)

if __name__ == "__main__":
    from tools.furigana import furiganaHTML, getKanjiReading
    if len(sys.argv) > 1:
        file = sys.argv[1] #"output/json/japanese_word.json"
        with open(file, "r", encoding="utf-8") as outputFile:
            data = json.load(outputFile)
            print(formatCard(data))
    else:
        print("Error: Please, enter the absolute path to the desired JSON file.")
else:
    from card_format.tools.furigana import furiganaHTML, getKanjiReading