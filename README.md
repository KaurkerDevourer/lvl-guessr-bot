# author-guessr-bot
A small game written as TG-bot, in which you are trying to guess the author via code example.

## Current Opportunities

- /start - start the game
- /stop - stop the game
- /stats - see your personal statistics
- /scoreboard - see the top among all participants
- /help - show the current capabilities of the bot

The bot saves your session and you will never answer the same question.
But be careful, it also means that if you make a mistake, you can't correct it!

## Current Modes

### HUMAN or AI
In this mode you are given a piece of code and 1 attempt to guess whether it was written by a human or generated by a neural network
A point is awarded for each correct answer

### Guess the level
Guess the level is more of an educational mode than an entertaining one. After each question, you will get a link to the original code and an explanation of the bug. It doesn't have as many examples as AI vs Human, but it allows you to familiarize yourself with the bugs that all of us make.

### Challenge
This mode allows you to generate a static sequence of questions (Challenges) from Guess the Level mode with a unique number.
The Challenge can be solved asynchronously, and at any time you can query the results of all participants in the current Challenge by unique number.

## How to run it

### Prerequisites
1. Create a Telegram bot (here: [@BotFather](https://t.me/botfather)) and get a unique token.
2. Place a unique token in the token.txt file in the root of the project.
3. Install dependencies:
```
python3 -m venv /path/to/venv
source /path/to/venv
pip install -r requirements.txt
python3 main.py
```

### Run
```
python3 main.py
```
