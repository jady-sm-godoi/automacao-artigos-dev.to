from agno import Agent, Model


class ArtigoAgent:
    def __init__(self, modelo: str = "gpt-4o"):
        self.modelo = modelo
        self._agent = Agent(
            model=Model(model_name=self.modelo),
            markdown=True,
        )

    async def gerar(self, prompt: str) -> str:
        resposta = await self._agent.arun(prompt)
        return resposta.content
