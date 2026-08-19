from abc import ABC, abstractmethod


class AIBase(ABC):
    @abstractmethod
    async def analyse_message(self, message_content: str):
        pass
