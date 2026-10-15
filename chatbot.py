"""Rule-based response engine for the Smart Chatbot."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


DEFAULT_RULES: dict[str, Any] = {
    "intents": [
        {
            "name": "wellbeing",
            "patterns": ["how are you", "how are you doing"],
            "responses": ["I'm doing well, thanks for asking! How can I help you?"]
        },
        {
            "name": "morning_greeting",
            "patterns": ["good morning"],
            "responses": ["Good morning! How may I assist you?"]
        },
        {
            "name": "afternoon_greeting",
            "patterns": ["good afternoon"],
            "responses": ["Good afternoon! How may I help you?"]
        },
        {
            "name": "evening_greeting",
            "patterns": ["good evening"],
            "responses": ["Good evening! How may I help you?"]
        },
        {
            "name": "greeting",
            "patterns": [
                "hello", "hi", "hey",
            ],
            "responses": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! Ask me a question or type /help to see what I know.",
            ],
        },
        {
            "name": "goodbye",
            "patterns": ["bye", "goodbye", "see you", "see you later", "exit", "quit"],
            "responses": ["Goodbye! Have a great day!"],
        },
        {
            "name": "thanks",
            "patterns": ["thank you", "thanks", "many thanks", "thanks a lot"],
            "responses": ["You're welcome! Is there anything else I can help with?"],
        },
        {
            "name": "name",
            "patterns": ["what is your name", "what's your name", "who are you", "your name"],
            "responses": ["I'm ChatPal, a friendly rule-based chatbot built with Python."],
        },
        {
            "name": "capabilities",
            "patterns": ["what can you do", "your features", "available features", "what do you do"],
            "responses": [
                "I can answer a few questions about Python, chatbots, support, and my features. Type /help for the topic list."
            ],
        },
        {
            "name": "creator",
            "patterns": ["who created you", "who made you", "who built you", "your creator"],
            "responses": ["I was created as a Python rule-based chatbot project."],
        },
        {
            "name": "python",
            "patterns": ["what is python", "tell me about python", "explain python", "python programming"],
            "responses": [
                "Python is a readable, general-purpose programming language used for applications, automation, data science, and more."
            ],
        },
        {
            "name": "chatbot",
            "patterns": ["what is a chatbot", "define chatbot", "how does a chatbot work"],
            "responses": [
                "A chatbot is a program that communicates with people. I use predefined text rules to choose a response; I don't use machine learning or an AI service."
            ],
        },
        {
            "name": "support",
            "patterns": ["contact support", "how can i contact support", "support contact", "help desk"],
            "responses": [
                "This demo has no connected support team. Please contact the person or organization that provided this application."
            ],
        },
        {
            "name": "help",
            "patterns": ["can you help me", "help me", "i need help", "help"],
            "responses": [
                "Of course! I can answer questions about my name, features, creator, Python, chatbots, and support. Type /help for a quick list."
            ],
        },
    ]
}


def normalize_input(message: str) -> str:
    """Make a message case-insensitive and remove punctuation/extra spaces."""
    text = message.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def handle_unknown_message() -> str:
    """Return a friendly response when no rule matches."""
    return "I'm not sure how to answer that yet. Try asking about Python, chatbots, my features, or type /help."


class RuleBasedChatbot:
    """Match normalized user messages against patterns loaded from JSON."""

    def __init__(self, rules_path: str | Path | None = None) -> None:
        self.rules_path = Path(rules_path) if rules_path else Path(__file__).with_name("responses.json")
        self.rules = self._load_rules()

    def _load_rules(self) -> dict[str, Any]:
        """Load valid response rules, falling back to built-in rules if needed."""
        try:
            with self.rules_path.open("r", encoding="utf-8") as response_file:
                data = json.load(response_file)
            if isinstance(data, dict) and isinstance(data.get("intents"), list):
                intents = [
                    intent for intent in data["intents"]
                    if isinstance(intent, dict)
                    and isinstance(intent.get("patterns"), list)
                    and isinstance(intent.get("responses"), list)
                    and intent["patterns"]
                    and intent["responses"]
                ]
                if intents:
                    return {"intents": intents}
        except (OSError, json.JSONDecodeError):
            pass
        return DEFAULT_RULES

    @staticmethod
    def _pattern_matches(message: str, pattern: str) -> bool:
        """Match a whole normalized phrase, not an accidental substring."""
        normalized_pattern = normalize_input(pattern)
        if not normalized_pattern:
            return False
        return f" {normalized_pattern} " in f" {message} "

    def get_response(self, message: str) -> str:
        """Return a predefined response for a message, or a helpful fallback."""
        normalized = normalize_input(message)
        if not normalized:
            return "Please type a message so I can try to help."

        if message.strip().lower() == "/help":
            return (
                "Try asking: What's your name? What can you do? Who created you? "
                "What is Python? What is a chatbot? How can I contact support?"
            )

        for intent in self.rules["intents"]:
            for pattern in intent["patterns"]:
                if isinstance(pattern, str) and self._pattern_matches(normalized, pattern):
                    responses = [item for item in intent["responses"] if isinstance(item, str) and item.strip()]
                    if responses:
                        # Stable selection keeps behavior predictable for demos and tests.
                        return responses[0]

        return handle_unknown_message()


def get_response(message: str) -> str:
    """Convenience function for callers that don't need a chatbot instance."""
    return RuleBasedChatbot().get_response(message)
