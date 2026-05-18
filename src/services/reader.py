from pathlib import Path

import frontmatter

from src.models.artigo import Anotacao

TAMANHO_MINIMO = 100


class MarkdownReader:
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir

    def listar_arquivos(self) -> list[Path]:
        if not self.source_dir.exists():
            return []
        return sorted(self.source_dir.rglob("*.md"))

    def ler_anotacao(self, caminho: Path) -> Anotacao | None:
        if caminho.stat().st_size == 0:
            return None

        raw = frontmatter.load(caminho)
        conteudo = raw.content.strip()

        if len(conteudo) < TAMANHO_MINIMO:
            return None

        return Anotacao(
            caminho=caminho,
            nome=caminho.stem,
            conteudo=conteudo,
            frontmatter=dict(raw.metadata),
            tamanho=len(conteudo),
        )

    def ler_todas(self) -> list[Anotacao]:
        arquivos = self.listar_arquivos()
        anotacoes: list[Anotacao] = []
        ignorados = 0

        for arquivo in arquivos:
            anotacao = self.ler_anotacao(arquivo)
            if anotacao:
                anotacoes.append(anotacao)
            else:
                ignorados += 1

        return anotacoes, ignorados
