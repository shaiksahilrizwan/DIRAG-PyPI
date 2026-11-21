from datetime import datetime
import json
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from Exceptions.exceptions import SessionSaveError, InvalidSession


class Chat:
    """Handle chat history and persistent sessions."""

    def __init__(self, system_prompt: str | None = None):
        self.chat_hist = []
        self.writable_chat_hist = []
        if system_prompt:
            self.chat_hist = [("system", system_prompt)]
            self.writable_chat_hist = [{"system": system_prompt}]
        self.human_message = None
        self.ai_message = None
        self.session_id = None

    def add_human_message(self, human_message: str):
        self.chat_hist.append(("human", human_message))
        self.human_message = human_message
        self.writable_chat_hist.append({"human": human_message})

    def add_ai_message(self, ai_message: str):
        self.chat_hist.append(("ai", ai_message))
        self.ai_message = ai_message
        self.writable_chat_hist.append({"ai": ai_message})

    def get_chat_history(self):
        return self.chat_hist

    def get_chat_prompt(self):
        return ChatPromptTemplate.from_messages(self.get_chat_history())

    def save_new_session(self):
        sessions_dir = Path.cwd() / "sessions"
        sessions_dir.mkdir(exist_ok=True)
        session_id = self.session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        session_path = sessions_dir / f"{session_id}.json"
        try:
            session_path.write_text(
                json.dumps(self.writable_chat_hist, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            raise SessionSaveError("Unable to save session") from exc

    def load_session(self, session_id: str):
        session_path = Path.cwd() / "sessions" / f"{session_id}.json"
        try:
            data = json.loads(session_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise InvalidSession("Session not found") from exc
        except json.JSONDecodeError as exc:
            raise InvalidSession("Corrupt session data") from exc

        if not data:
            raise InvalidSession("No session data found")

        for element in data:
            for key, value in element.items():
                if key == "system":
                    self.chat_hist.append(("system", value))
                    self.writable_chat_hist.append({"system": value})
                elif key == "ai":
                    self.add_ai_message(value)
                elif key == "human":
                    self.add_human_message(value)
        self.session_id = session_id