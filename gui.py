"""Tkinter graphical interface for the Smart Rule-Based Chatbot."""

from __future__ import annotations

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from chatbot import RuleBasedChatbot


class ChatbotApp:
    """A lightweight chat window built with Python's standard Tkinter library."""

    COLORS = {
        "window": "#F4F7FB",
        "surface": "#FFFFFF",
        "header": "#172554",
        "header_subtitle": "#C7D2FE",
        "text": "#172033",
        "muted": "#778198",
        "user_bubble": "#DCEBFF",
        "bot_bubble": "#FFFFFF",
        "accent": "#3867E8",
        "accent_hover": "#2855D4",
        "border": "#E2E8F0",
        "input": "#FFFFFF",
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.bot = RuleBasedChatbot()
        self.history: list[tuple[str, str, str]] = []
        self.root.title("ChatPal — Rule-Based Chatbot")
        self.root.geometry("760x700")
        self.root.minsize(520, 520)
        self.root.configure(bg=self.COLORS["window"])
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self._build_interface()
        self.add_message(
            "bot",
            "Welcome! I'm ChatPal. Ask me about Python, chatbots, or what I can do. Type /help for topics.",
        )
        self.entry.focus_set()

    def _build_interface(self) -> None:
        """Create the header, scrollable chat history, and message composer."""
        colors = self.COLORS
        header = tk.Frame(self.root, bg=colors["header"], padx=24, pady=18)
        header.pack(fill="x")

        title_area = tk.Frame(header, bg=colors["header"])
        title_area.pack(side="left", fill="x", expand=True)
        tk.Label(
            title_area,
            text="ChatPal",
            bg=colors["header"],
            fg="white",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            title_area,
            text="A friendly, rule-based Python chatbot",
            bg=colors["header"],
            fg=colors["header_subtitle"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 0))

        clear_button = tk.Button(
            header,
            text="Clear chat",
            command=self.clear_chat,
            bg="#263968",
            fg="white",
            activebackground="#344879",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
        )
        clear_button.pack(side="right", padx=(12, 0))

        chat_area = tk.Frame(self.root, bg=colors["window"], padx=18, pady=16)
        chat_area.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(
            chat_area,
            bg=colors["window"],
            highlightthickness=0,
            borderwidth=0,
        )
        scrollbar = ttk.Scrollbar(chat_area, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.message_frame = tk.Frame(self.canvas, bg=colors["window"])
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.message_frame, anchor="nw"
        )
        self.message_frame.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_message_frame)
        self.canvas.bind("<Enter>", self._enable_mousewheel)
        self.canvas.bind("<Leave>", self._disable_mousewheel)

        composer = tk.Frame(self.root, bg=colors["surface"], padx=18, pady=14)
        composer.pack(fill="x", side="bottom")
        tk.Frame(composer, bg=colors["border"], height=1).pack(fill="x", pady=(0, 13))
        entry_row = tk.Frame(composer, bg=colors["surface"])
        entry_row.pack(fill="x")

        self.entry = tk.Entry(
            entry_row,
            bg=colors["input"],
            fg=colors["text"],
            insertbackground=colors["text"],
            relief="solid",
            bd=1,
            highlightthickness=0,
            font=("Segoe UI", 11),
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=11, padx=(0, 10))
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<KP_Enter>", self._on_enter)

        self.send_button = tk.Button(
            entry_row,
            text="Send  ➤",
            command=self.send_message,
            bg=colors["accent"],
            fg="white",
            activebackground=colors["accent_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10,
        )
        self.send_button.pack(side="right")
        tk.Label(
            composer,
            text="Press Enter to send · This chatbot uses predefined rules",
            bg=colors["surface"],
            fg=colors["muted"],
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(8, 0))

    def _update_scroll_region(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_message_frame(self, event: tk.Event[tk.Misc]) -> None:
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def _enable_mousewheel(self, _event: tk.Event[tk.Misc]) -> None:
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _disable_mousewheel(self, _event: tk.Event[tk.Misc]) -> None:
        self.root.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event[tk.Misc]) -> None:
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def add_message(self, sender: str, text: str) -> None:
        """Add a timestamped, aligned message bubble to the chat window."""
        if not text.strip():
            return
        colors = self.COLORS
        is_user = sender == "user"
        timestamp = datetime.now().strftime("%I:%M %p").lstrip("0")
        self.history.append((sender, text, timestamp))

        row = tk.Frame(self.message_frame, bg=colors["window"])
        row.pack(fill="x", padx=5, pady=6)
        row.grid_columnconfigure(0, weight=1)
        bubble_color = colors["user_bubble"] if is_user else colors["bot_bubble"]
        bubble = tk.Frame(row, bg=bubble_color, padx=13, pady=9, highlightthickness=1)
        bubble.configure(highlightbackground=colors["border"])
        max_width = max(200, min(560, self.canvas.winfo_width() - 170))
        message_label = tk.Label(
            bubble,
            text=text,
            bg=bubble_color,
            fg=colors["text"],
            justify="left",
            anchor="w",
            wraplength=max_width,
            font=("Segoe UI", 10),
        )
        message_label.pack(anchor="w")
        tk.Label(
            bubble,
            text=f"{'You' if is_user else 'ChatPal'}  ·  {timestamp}",
            bg=bubble_color,
            fg=colors["muted"],
            font=("Segoe UI", 8),
        ).pack(anchor="e" if is_user else "w", pady=(6, 0))
        bubble.grid(row=0, column=0, sticky="e" if is_user else "w")

        self.root.after_idle(self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def _on_enter(self, _event: tk.Event[tk.Misc]) -> str:
        self.send_message()
        return "break"

    def send_message(self) -> None:
        """Display the user's message and the matching rule-based reply."""
        message = self.entry.get().strip()
        if not message:
            return
        self.entry.delete(0, tk.END)
        self.add_message("user", message)
        try:
            response = self.bot.get_response(message)
        except Exception:
            # Keep the GUI usable if a custom response file has unexpected data.
            response = "Sorry, I couldn't process that message. Please try again."
        self.add_message("bot", response)

    def clear_chat(self) -> None:
        """Remove conversation bubbles and restore the opening welcome message."""
        for child in self.message_frame.winfo_children():
            child.destroy()
        self.history.clear()
        self.add_message(
            "bot",
            "Chat cleared. Welcome back! Ask me about Python, chatbots, or type /help.",
        )
        self.entry.focus_set()

    def close(self) -> None:
        """Close the application cleanly."""
        self.root.destroy()


def run_app() -> None:
    """Create and run the Tkinter application."""
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()
