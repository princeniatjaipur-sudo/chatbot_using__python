# Smart Rule-Based Chatbot

A beginner-friendly desktop chatbot built with Python and Tkinter. It uses predefined text rules to answer common user questions without external APIs or machine learning.

## Demo

This project is a local chat application that responds to greetings, FAQs, help requests, and goodbye messages in a simple rule-based way.

## Features

- Modern Tkinter GUI with message bubbles and timestamps
- Send button and Enter-to-send interaction
- Scrollable chat area and clear-chat option
- Case-insensitive message matching
- `/help` command support
- Built-in fallback for unknown questions
- Editable response patterns in `responses.json`
- Automated unit tests with Python's standard `unittest`

## Tech Stack

- Python 3.9+
- Tkinter
- JSON for configurable chatbot rules
- unittest for testing

## Project Structure

- `main.py` — starts the application
- `gui.py` — chat window and UI logic
- `chatbot.py` — rule matching and normalization
- `responses.json` — chatbot intents and response data
- `tests/test_chatbot.py` — automated tests

## Installation

Clone the repository:

```bash
git clone https://github.com/princeniatjaipur-sudo/chatbot_using_python.git
cd chatbot_using_python
```

Run the app:

```powershell
py main.py
```

If `py` is not available, use:

```powershell
python main.py
```

## Testing

Run the test suite:

```powershell
py -m unittest discover -s tests -v
```

## Example Conversation

- User: `Hello!`
- Bot: `Hello! How can I help you today?`
- User: `What is Python?`
- Bot: `Python is a readable, general-purpose programming language used for applications, automation, data science, and more.`
- User: `/help`
- Bot: `Try asking: What's your name? What can you do? ...`

## Notes

The chatbot is intentionally simple and deterministic. It matches normalized phrases and returns the first matching response from the configured rule set. This keeps the project beginner-friendly and easy to customize.

## License

This project is open for educational and personal use.
