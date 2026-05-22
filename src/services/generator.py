import asyncio
import re
import shutil
from datetime import datetime
from pathlib import Path

from src.agent import ArtigoAgent
from src.config import Config
from src.logger import setup_logger
from src.models.artigo import Artigo
from src.services.reader import MarkdownReader
from src.services.template import TemplateRenderer

logger = setup_logger(__name__)

EXTENSOES_VALIDAS = {".md", ".markdown"}
FORMATOS_IMAGEM = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


class GeradorArtigo:
    def __init__(self, config: Config | None = None):
        self.config = config or Config()

    def _garantir_diretorios(self) -> None:
        self.config.source_dir.mkdir(parents=True, exist_ok=True)
        (self.config.source_dir / "imagens").mkdir(parents=True, exist_ok=True)
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        self.config.template_path.parent.mkdir(parents=True, exist_ok=True)

    def _validar_extensao(self, caminho: Path) -> None:
        if caminho.suffix.lower() not in EXTENSOES_VALIDAS:
            msg = f"Extensão não suportada: {caminho.suffix}"
            raise ValueError(msg)

    def _nome_arquivo(self, titulo: str) -> str:
        slug = titulo.lower()[:50]
        slug = "".join(c if c.isalnum() or c in "-_" else "-" for c in slug)
        slug = slug.strip("-")

        if not slug:
            slug = "artigo"

        caminho_base = self.config.output_dir / f"{slug}.md"
        if not caminho_base.exists():
            return f"{slug}.md"

        contador = 1
        while True:
            caminho = self.config.output_dir / f"{slug}-{contador}.md"
            if not caminho.exists():
                return caminho.name
            contador += 1

    def _montar_conteudo(self, anotacoes) -> tuple[str, str, str]:
        partes: list[str] = []
        tags: set[str] = set()

        for a in anotacoes:
            if a.frontmatter:
                tags.update(a.frontmatter.get("tags", []))
            partes.append(f"---\nFonte: {a.caminho}\n---\n{a.conteudo}")

        titulo = "Artigo sem título"
        if anotacoes:
            first_fm = anotacoes[0].frontmatter
            titulo = first_fm.get("titulo") or first_fm.get("title") or titulo

        return "\n\n".join(partes), titulo.strip(), ", ".join(sorted(tags))

    def _copiar_imagens(self) -> None:
        source_img = self.config.source_dir / "imagens"
        if not source_img.exists():
            return

        dest_img = self.config.output_dir / "imagens"
        dest_img.mkdir(parents=True, exist_ok=True)

        for img in source_img.iterdir():
            if img.is_file() and img.suffix.lower() in FORMATOS_IMAGEM:
                destino = dest_img / img.name
                if not destino.exists():
                    shutil.copy2(img, destino)
                    logger.info("Imagem copiada: %s", destino)

    def _listar_imagens(self) -> str:
        img_dir = self.config.source_dir / "imagens"
        if not img_dir.exists():
            return "Nenhuma imagem disponível."

        imagens = sorted(
            p
            for p in img_dir.iterdir()
            if p.is_file() and p.suffix.lower() in FORMATOS_IMAGEM
        )

        if not imagens:
            return "Nenhuma imagem disponível."

        linhas = [f"- `{p.name}`" for p in imagens[:5]]
        return "\n".join(linhas)

    @staticmethod
    def _normalizar_frontmatter(conteudo: str) -> str:
        padrao = re.compile(
            r"^```(?:yaml)?\s*\n(---\n.*?\n---)\n```\s*\n?(.*)",
            re.DOTALL,
        )
        match = padrao.match(conteudo)
        if match:
            logger.info("Frontmatter normalizado: removido wrapper ```yaml")
            return match.group(1) + "\n\n" + match.group(2)
        return conteudo

    async def gerar(self) -> Artigo:
        self._garantir_diretorios()
        self._copiar_imagens()

        reader = MarkdownReader(self.config.source_dir)
        anotacoes, ignorados = reader.ler_todas()

        if not anotacoes:
            msg = "Nenhuma anotação encontrada em"
            raise ValueError(f"{msg} {self.config.source_dir}")

        logger.info(
            "Total de anotações: %d | Ignorados: %d",
            len(anotacoes),
            ignorados,
        )

        conteudo, titulo, tags_str = self._montar_conteudo(anotacoes)
        imagens_str = self._listar_imagens()

        renderer = TemplateRenderer(self.config.template_path)
        prompt = renderer.renderizar(
            conteudo=conteudo,
            titulo=titulo,
            tags=tags_str,
            imagens=imagens_str,
        )

        agent = ArtigoAgent(modelo=self.config.modelo)
        logger.info("Gerando artigo com modelo: %s", self.config.modelo)
        artigo_gerado = await agent.gerar(prompt)

        artigo_gerado = self._normalizar_frontmatter(artigo_gerado)

        nome_arquivo = self._nome_arquivo(titulo)
        caminho_saida = self.config.output_dir / nome_arquivo
        caminho_saida.write_text(artigo_gerado, encoding="utf-8")

        logger.info("Artigo salvo em: %s", caminho_saida)

        return Artigo(
            titulo=titulo,
            conteudo=artigo_gerado,
            tags=list(anotacoes[0].frontmatter.get("tags", []))
            if anotacoes and anotacoes[0].frontmatter
            else [],
            data_criacao=datetime.now(),
            fontes=[a.caminho for a in anotacoes],
        )


def gerar_artigo(config: Config | None = None) -> Artigo:
    gerador = GeradorArtigo(config)
    return asyncio.run(gerador.gerar())
