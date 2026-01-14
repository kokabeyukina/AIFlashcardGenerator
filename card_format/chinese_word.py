import json
import re
import sys
from pydantic import BaseModel

class SentenceWords(BaseModel):
    word: str
    meanings: list[str]
    classifiers: list[str]

class Card(BaseModel):
    word: str
    example_sentence: str
    pinyin_reading: str
    word_meanings: list[str]
    example_sentence_translation: str
    sentence_words: list[SentenceWords]
    grammar_explanations: list[str]

class Cards(BaseModel):
    cards: list[Card]   

def formatCard(data: dict) -> str:
    """
    Converts a JSON Object into the chinese_word class format.
    """
    if not isinstance(data, dict):
        data = json.loads(data)
        
    cardList = []
    for card in data["cards"]:
        word = hanziStyle(card["word"])
        wordH1 = f"{word["traditional"]}" if word["identified_format"] == "Ambiguous" \
            else f"{word["traditional"]}<br>{word["simplified"]}"

        sentence = hanziStyle(card["example_sentence"])
        sentences = f"{sentence["traditional"]}" if sentence["identified_format"] == "Ambiguous" \
               else f"{sentence["traditional"]}<br>{sentence["simplified"]}"
        
        pin_word, zhu_word = pinzhu(card["word"])

        sentence_words = []
        for item in card["sentence_words"]:
            classifier = []
            for cl in item["classifiers"]:
                hanzi = hanziStyle(cl)
                if hanzi["identified_format"] == "Ambiguous":
                    classifier.append(cl)
                else:
                    classifier.append(hanzi["traditional"]+" / "+hanzi["simplified"])
            sentence_words.append(f"{item["word"]} = {"; ".join(item["meanings"])}{"; CL: "+", ".join(classifier) if item["classifiers"] else ""}")
        
        cardList.append(re.sub(r'\s{2,}', '', f"""
            <h1 style=\"font-weight:100\">{wordH1}</h1>
            <br>
            <br>{sentences}
            |{zhu_word}
            <br>{pin_word}
            <br>{"; ".join(card["word_meanings"])}
            <br>
            <br>{pinzhuHTML(sentence["traditional"])}
            <br>{card["example_sentence_translation"]}
            <br>
            <br>{"<br>".join(sentence_words)}
            <br>
            <br>{"<br>".join(card["grammar_explanations"])}
            <br>
            <br>
            <br>AI given pinyin:
            <br>{card["pinyin_reading"]}
        """))
    return "\n".join(cardList)
        
if __name__ == "__main__":
    from tools.pinyin import pinzhuHTML, hanziStyle, pinzhu
    if len(sys.argv) > 1:
        file = sys.argv[1] #".../output/json/chinese_word.json"
        with open(file, "r", encoding="utf-8") as outputFile:
            data = json.load(outputFile)
            print(formatCard(data))
    else:
        print("\033[91mError:\033[0m Please, enter the absolute path to the desired JSON file.")
else:
    from card_format.tools.pinyin import pinzhuHTML, hanziStyle, pinzhu