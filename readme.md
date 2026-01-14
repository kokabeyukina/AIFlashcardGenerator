# AI Flashcard Generator
This is a simple tool that uses Ollama to create Anki flashcards.
<br><br>

## How It works
When provided with a list of words, the program uses a local LLM to generate example sentences, translations, grammar explanations, etc., for each word, in JSON format.
The program then processes this JSON data and converts it into an Anki-compatible format, saved as a `.txt` file for easy importing.

## Usage

### Using The UI
1. Run the `ui.bat` file.
2. Select your desired formatting style (Card Class).
3. Input the words you wish to turn into cards.
4. Once finished, open Anki and import the final output file.

### Using The Terminal
You can bypass the UI and run the generator directly via Python by calling the class file with the word list as arguments:
```
python [class_name]_class.py [word1] [word2] [word3]...
```

## Dependencies

### Ollama
You must have Ollama installed and running on your system.
1. Download Ollama at [ollama.com](https://ollama.com).
2. After installing, pull your preferred model by running `ollama pull [model]`. The default model for this program is `gpt-oss:20b`, which requires at least 16BG of RAM, but other models might work better for you.
3. Ensure the Ollama server is active by opening the app or running `ollama serve`.

### Python Libraries
Ensure you have Python 3.10+ installed. In the program folder, run the following command to install the required libraries:
```
python -m pip install -r requirements.txt
```
It may also be necessary to download a dictionary for Japanese support:
```
python -m unidic download
``` 

## Configuration
The following variables can be customized in `configs.json`: 
* **Model:** Specify which Ollama model to use.
* **Thinking Level:** Choose between **_high_**, **_medium_**, or **_low_** to balance speed and accuracy.
* **Final Output Path:** Change where your cards (final output file) are saved (Default: `./output/cards.txt`).

## Notes
* Prompts and card formatting can be modified in the `prompt/` and `card_format/` folders. Within these folders, files are named according to their respective classes.
* The `ui.bat` script automatically recognizes any file ending in `_class.py`. You can create as many classes as you need by using the two pre-implemented classes as templates.
* To avoid hallucinations, it is recommended to process a maximum of 5 words per request.
* The last output generated for each class is automatically stored in the `output/` folder.
* Other scripts used for formatting are stored in `card_format/tools/`.
* If the formatting did not occur correctly and you don't want to reload the model, it is possible to format the cards directly from a JSON files. Run `python card_format/[class].py [path to JSON]` and the cards will be displayed, but not saved.