from typing import Any, Callable
import pyperclip
import ollama
import json

def loadConfig(filename: str='./configs.json') -> dict:
    """
    Gets the settings in a JSON file.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from file '{filename}'.")
        return None

def loadModel(prompt: str, list: str, format: dict[str, Any], model: str="gpt-oss:20b", think: str="medium") -> str:
    """
    Loads the data to the LLM and returns the response.
    """
    if not list:
        list = pyperclip.paste()

    print("\033[1;36;40m------------------ Prompt -------------------\033[0m")
    print(prompt, end="\n\n")
    print("\033[1;36;40m------------------- List --------------------\033[0m")
    print(list, end="\n\n")
    print("\033[1;36;40m------------------ Format -------------------\033[0m")
    print(format, end="\n\n")

    try:
        response = ollama.chat(
            model=model,
            messages=[{'role':'user', 'content':prompt+list}],
            format=format,
            options={'temperature':0.1},
            think=think,
            stream=True
        )
        print(f"Loading \033[1;36;40m{model}\033[0m...\n")
    except Exception as e:
        print(f"\033[1;31;40mError during initial load: {e}. Attempting main generation anyway.\033[0m")
        return
    
    fullResponse = ""
    thinking = False
    
    for chunk in response:
        if chunk.message.thinking:
            if not thinking:
                thinking = True
                print("\033[1;33m----------------- Reasoning -----------------\033[0m")
                print("\033[93m", end='', flush=True)
            print(chunk.message.thinking, end='', flush=True)
        elif chunk.message.content:
            if thinking:
                thinking = False
                print("\033[0m", end='\n\n', flush=True)
                print("\033[1;32m------------------ Output -------------------\033[0m")
            content = chunk.message.content
            print(content, end='', flush=True) 
            fullResponse += content
    
    print("\n\n\033[1;32;40m-------- Response Generation Complete -------\033[0m\n")
    return fullResponse

def generateCards(cardClass: str, list: str, format: dict[str, Any], formatCard: Callable[[dict], str]):
    """
    Loads all class data, handles and saves the card generation.
    """
    config = loadConfig()
    if config:
        with open("prompt/"+cardClass+".txt", "r", encoding="utf-8") as promptFile:
            response = loadModel(promptFile.read(), list, format, model=config["model"], think=config["think"])
            with open("output/json/"+cardClass+".json", "w", encoding="utf-8") as outputFile:
                outputFile.write(response)
                print(f"\033[1;32;40mJson response saved in './output/json/{cardClass}.json'.\033[0m")

            cards = formatCard(json.loads(response))
            print("\033[1;36;40m------------------- Cards -------------------\033[0m")
            print(cards)

            with open("output/cards/"+cardClass+".txt", "w", encoding="utf-8") as cardFile:
                cardFile.write(cards)
                print(f"\033[1;32;40mCards saved in './output/cards/{cardClass}.txt'.\033[0m")
                
            with open(config["final output path"], "w", encoding="utf-8") as cardFile:
                cardFile.write(cards)
                print(f"\033[1;32;40mCards saved in '{config["final output path"]}'.\033[0m\n")
