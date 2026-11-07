# Introduction

Hello there! Ever wanted a free and open source version of GrokBot that you, yes you, can control? Introducing **OpenAuto**, an application using Qwen, a local open-source model and some python libraries like `pyautogui` for controlling your system, `os` for other operating system operations, and `yt-dlp` for searching YouTube.

**WARNING! THIS IS MADE WITH THE HELP OF ARTIFICIAL INTELLIGENCE!**

# Installation

This section is for setting up OpenAuto in your computer.

You must download Ollama first from https://ollama.com/download.

## Terminal for Techies

Believe it or not, the terminal (in form of Command Prompt, Powershell, Linux Terminal, MacOS Terminal, etc.) can only be safely used if you are techy enough (and we apologize for anyone not familiar with technology in the modern age). 

### EXE

Here are the steps to set up the EXE:
1. Download the EXE from the latest release
2. Open the EXE and you are good to go!

### Advanced (Command Line)

This is more advanced, but I believe you can do it!

1. Download python from https://www.python.org/downloads/. (It is recomended that you get the standalone installer)
2. Install python.
3. Download the source code. (either clone via `git clone https://github.com/OpenBotsForThePeople/OpenAuto` or Download the ZIP then extract it)
4. Open your operating system's terminal.
5. Navigate the folder to where you downloaded it to (via `cd` to change directory and `dir` for listing the directory's contents).
6. (Optional but recommended) Move the folder into a safe place.
7. (Optional but recommended) Make a virtual environment via `python -m venv .venv`. 
8. If you have made a venv, activate it via `.venv\scripts\activate`. Otherwise, skip this step.
9. Install all requirements by running `pip install -r requirements.txt`.
10. Type `playwright install` to install playwright and its libraries.
11. Run `main.py` and you are good to go!

# Usage

Once you have started the app, it is reccomended to type `help` as your first command so that you can see all the other commands available.

## Creation of Models

If you ran `create`, you are in the model creation wizard! Just type in your desired model's name, appearance in the form of a hex color (similar to GrokBot's appearance of bots but more flexible), job, permissions (what it can do), and that model has now been created!

## Usage of Models

You can talk to your model via `talk <model name>`. Once in the chat menu, you can tell or ask it anything. The message will then go to local model Qwen, and Qwen will request to use a function, which depending on your permissions for the model, it may or may not ask you whether it can use the requested function.

If you want to exit the chat, type `/exit`.