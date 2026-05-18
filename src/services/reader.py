from pathlib import Path

import frontmatter

from src.logger import setup_logger
from src.models.artigo import Anotacao

logger = setup_logger(__name__)

TAMANHO_MINIMO = 100


class MarkdownReader:
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir

    def listar_arquivos(self) -> list[Path]:
        if not self.source_dir.exists():
            logger.info("Diretório não encontrado: %s", self.source_dir)
            return []

        arquivos = sorted(self.source_dir.rglob("*.md"))
        logger.info(
            "Encontrados %d arquivos .md em %s",
            len(arquivos),
            self.source_dir,
        )
        return arquivos

    def ler_anotacao(self, caminho: Path) -> Anotacao | None:
        if caminho.stat().st_size == 0:
            logger.warning("Arquivo vazio ignorado: %s", caminho)
            return None

        raw = frontmatter.load(caminho)
        conteudo = raw.content.strip()

        if len(conteudo) < TAMANHO_MINIMO:
            logger.warning(
                "Conteúdo muito curto (%d chars) ignorado: %s",
                len(conteudo),
                caminho,
            )
            return None

        return Anotacao(
            caminho=caminho,
            nome=caminho.stem,
            conteudo=conteudo,
            frontmatter=dict(raw.metadata),
            tamanho=len(conteudo),
        )

    def ler_todas(self) -> tuple[list[Anotacao], int]:
        arquivos = self.listar_arquivos()
        anotacoes: list[Anotacao] = []
        ignorados = 0

        for arquivo in arquivos:
            anotacao = self.ler_anotacao(arquivo)
            if anotacao:
                anotacoes.append(anotacao)
            else:
                ignorados += 1

        logger.info(
            "Lidas %d anotações, %d ignoradas",
            len(anotacoes),
            ignorados,
        )
        return anotacoes, ignorados
