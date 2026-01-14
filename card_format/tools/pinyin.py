from pypinyin import pinyin, Style
import opencc
import sys
import re

def pinzhuHTML(text: str, style: str="font-size: 22pt; line-height: 70px", sep: str="　") -> str:
    """
    Returns the text formatted in HTML, with pinyin above and zhuyin under.
    """
    pinyin_list = pinyin(text, style=Style.TONE)
    bopomofo_list = pinyin(text, style=Style.BOPOMOFO)
    
    out = []
    for i in range(len(pinyin_list)):
        if re.match(r'[\u4e00-\u9fe6]', text[i]):
            out.append(f'<ruby><ruby style="ruby-position: under;">{text[i]}<rt>{bopomofo_list[i][0]}</rt></ruby><rt>{pinyin_list[i][0]}</rt></ruby>')

    return "<style>ruby{"+style+"}</style>"+sep.join(out)

def pinzhu(text: str) -> tuple[str, str]:
    """
    Returns the text reading in a tuple where the first item is in pinyin and the second one in zhuyin.
    """
    return (
        " ".join([item[0] for item in pinyin(text, style=Style.TONE)]), 
        "".join([item[0] for item in pinyin(text, style=Style.BOPOMOFO)])
    )


def hanziStyle(text: str) -> dict:
    """
    Returns a dictionary with information about the text, such as:
    \{
        identified_format,
        traditional,
        simplified
    }
    """
    if not text:
        return {
            "identified_format": "None",
            "traditional": "",
            "simplified": ""
        }
    
    cc_t2s = opencc.OpenCC('t2s.json')
    simplified_result = cc_t2s.convert(text)

    if simplified_result != text:
        return {
            "identified_format": "Traditional",
            "traditional": text,
            "simplified": simplified_result
        }

    cc_s2t = opencc.OpenCC('s2t.json')
    traditional_result = cc_s2t.convert(text)

    if traditional_result != text:
        return {
            "identified_format": "Simplified",
            "traditional": traditional_result,
            "simplified": text
        }

    return {
        "identified_format": "Ambiguous",
        "traditional": text,
        "simplified": text
    }


if __name__ == "__main__":
    sentence = sys.argv[1] if len(sys.argv) > 1 else "这是一个例句。"

    pin, zhu = pinzhu(sentence)
    print("-------- pinyin --------")
    print(pin, end="\n\n")
    print("-------- zhuyin --------")
    print(zhu, end="\n\n")

    print("------ hanziStyle ------")
    for key, value in hanziStyle(sentence).items():
        print(f"{key:<17}: {value}")
    print()

    print("------ pinzhuHTML ------")
    print(pinzhuHTML(sentence), end="\n\n")