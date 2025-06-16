# To-Do List Telegram Bot

A simple Telegram bot to help you create, delete, and manage your to-do tasks with reminders.

---

## Features

- `/start` — start interaction with the bot  
- Add tasks to your to-do list  
- Delete tasks from your list  
- View your current tasks  
- Set reminders for tasks  

---

## Technologies

- Python 3.10+  
- [Aiogram](https://docs.aiogram.dev/en/latest/) — Telegram Bot API framework  
- `python-dotenv` for environment variable management  

---

This bot is **not hosted** anywhere.  
This repository contains only the source code.  
To use the bot, you need to run it locally or deploy it on your own server.

## Setup & Running

1. Clone the repository:
    ```bash
    git clone https://github.com/bytebitt/To-Do-Bot.git
    cd To-Do-Bot
    ```
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    ```
    Linux/macOS
    ```bash
    source .venv/bin/activate
    ```
    Windows
    ```bash
    .\.venv\Scripts\activate
    ```
3. Install dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
    ```