from app.ai.base import AIBase


class MockAIService(AIBase):
    async def analyse_message(self, message_content: str):
        return {"status": "this is mock response"}
