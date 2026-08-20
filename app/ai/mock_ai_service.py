from app.ai.base import AIBase


class MockAIService(AIBase):
    async def generate_analysis(self, message_content: str):
        return {"status": "this is mock response"}
