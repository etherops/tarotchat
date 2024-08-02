# Tarot Card Drawing Game

This Python script is a tarot card drawing game that uses the Rider-Waite deck. It allows users to draw one or three cards and optionally provide a question for interpretation. The script interacts with the OpenAI API to provide an interpretation of the drawn cards based on the user's question.

## Features

- Draw one or three tarot cards from the Rider-Waite deck.
- Optionally, specify a question for card interpretation.
- Option to draw clarifying cards if one card is drawn.
- Uses OpenAI's GPT-3.5-turbo model to interpret the drawn cards based on the provided question.

## Requirements

- Python 3.x
- `openai` package
- OpenAI API key

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages using pip:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install openai
   ```
3. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

## Usage
### Command Line Interface
You can run the script from the command line with the following options:

Draw one or three cards:
```bash
python tarot_game.py --num-cards 1
Provide a question for interpretation:
```

```bash
python tarot_game.py --num-cards 3 --question "What should I focus on this week?"
```
`
### Interactive Mode
If you don't specify the number of cards as a command-line argument, the script will prompt you to choose between drawing one or three cards.
```bash
python tarot_game.py
Follow the on-screen prompts to draw cards and provide a question.
```

## Note
Ensure you have set the OpenAI API key in your environment variables before running the script. The script will raise an error if the API key is not found.

## License
This project is licensed under the MIT License.



