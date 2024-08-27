from queue import Queue
from typing import Optional, Any

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession


class BotAI(Bot):
    queue: Queue

    def __init__(self, token: str, session: Optional[BaseSession] = None,
                 default: Optional[DefaultBotProperties] = None, **kwargs: Any) -> None:
        super().__init__(token, session, default, **kwargs)


# class BotAI(Bot):
#
#     def __init__(self,
#                  token: str,
#                  session=None,
#                  default=None,
#                  **kwargs) -> None:
#         self.genai = GenAI("models/gemini-1.5-flash")
#         self.chat = self.genai.start_chat()
#         super().__init__(token, session, default, **kwargs)