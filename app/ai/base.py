from abc import ABC, abstractmethod


class AIBase(ABC):
    @abstractmethod
    async def generate_analysis(self, message_content: str):
        pass
