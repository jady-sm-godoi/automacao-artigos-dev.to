from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.agent import RunStatus


class ArtigoAgent:
    def __init__(self, modelo: str = "gpt-4o"):
        self.modelo = modelo
        self._agent = Agent(
            model=OpenAIChat(id=self.modelo),
            markdown=True,
        )

    async def gerar(self, prompt: str) -> str:
        resposta = await self._agent.arun(prompt)
        if resposta.status == RunStatus.error:
            msg = f"Erro do agente: {resposta.content}"
            raise RuntimeError(msg)
        return str(resposta.content)
