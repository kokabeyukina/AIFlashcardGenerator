import re
import fugashi
from html import escape
import sys

def katakanaToHiragana(text: str) -> str:
    """
    Converts from katakana to hiragana.
    """
    if not text:
        return
    return "".join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in text)

def getKanjiReading(word: str) -> str:
    """
    Returns the word reading.
    """
    result = []
    tagger = fugashi.Tagger()
    for token in tagger(word):
        surface = token.surface
        reading = token.feature.kana
        if not reading or reading == surface or reading == '*':
            result.append(surface)
        else:
            result.append(katakanaToHiragana(reading))
    return "".join(result)

def formatOkurigana(input: str, keys: list[4]=['<ruby>', '<rt>', '</rt>', '</ruby>']) -> str:
    """
    When provided with a furigana token formatted as <token(furigana)>, this functions returns a set of tokens where the furigana matches its kanji, with borders defined by the keys list.
    """
    match = re.match(r"^<(.+?)\((.+?)\)>$", input)
    if not match:
        return input

    surface = list(match.group(1))
    reading = list(match.group(2))

    result = []
    reading_index = 0
    surface_index = 0
    while surface_index < len(surface):
        char = surface[surface_index]
        if re.match(r'[\u4e00-\u9fe6]', char):
            surface_chunk = [char]
            kanji_index = surface_index + 1
            while kanji_index < len(surface) and re.match(r'[\u4e00-\u9fe6]', surface[kanji_index]):
                surface_chunk.append(surface[kanji_index])
                kanji_index += 1
            
            reading_chunk = []
            next_kana = surface[kanji_index] if kanji_index < len(surface) else None
            while reading_index < len(reading):
                if next_kana and next_kana == reading[reading_index]:
                    break
                reading_chunk.append(reading[reading_index])
                reading_index += 1

            result.append(f"{keys[0]}{"".join(surface_chunk)}{keys[1]}{"".join(reading_chunk)}{keys[2]}{keys[3]}")
            surface_index = kanji_index
        else:
            if reading_index < len(reading) and reading[reading_index] == char:
                reading_index += 1
            
            result.append(char)
            surface_index += 1

    return "".join(result)

def furiganaHTML(sentence: str) -> str:
    """
    Returns the input with its furigana formatted in HTML.
    """
    result = []
    tagger = fugashi.Tagger()
    for token in tagger(sentence):
        surface = token.surface
        reading = token.feature.kana
        reading_hira = katakanaToHiragana(reading)
        if not reading or reading == surface or reading_hira == surface or reading == '*':
            result.append(escape(surface))
        else:
            result.append(formatOkurigana(f'<{escape(surface)}({reading_hira})>'))

    return "".join(result)

if __name__ == "__main__":
    sentence = sys.argv[1] if len(sys.argv) > 1 else "コレは只の例文です"
    print("---- getKanjiReading ---")
    print(getKanjiReading(sentence), end="\n\n")
    print("----- furiganaHTML -----")
    print(furiganaHTML(sentence), end="\n\n")