import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.agent import RunStatus

from src.logger import setup_logger

logger = setup_logger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2


class ArtigoAgent:
    def __init__(self, modelo: str = "gpt-4o"):
        self.modelo = modelo
        self._agent = Agent(
            model=OpenAIChat(id=self.modelo),
            markdown=True,
        )

    async def gerar(self, prompt: str) -> str:
        ultimo_erro = None

        for tentativa in range(1, MAX_RETRIES + 1):
            try:
                resposta = await self._agent.arun(prompt)
                if resposta.status == RunStatus.error:
                    msg = f"Erro do agente: {resposta.content}"
                    logger.error(msg)
                    raise RuntimeError(msg)
                return str(resposta.content)
            except RuntimeError:
                raise
            except Exception as e:
                ultimo_erro = e
                logger.warning(
                    "Tentativa %d/%d falhou: %s",
                    tentativa,
                    MAX_RETRIES,
                    e,
                )
                if tentativa < MAX_RETRIES:
                    await asyncio.sleep(RETRY_DELAY * tentativa)

        msg = f"Falha após {MAX_RETRIES} tentativas: {ultimo_erro}"
        logger.error(msg)
        raise RuntimeError(msg)
