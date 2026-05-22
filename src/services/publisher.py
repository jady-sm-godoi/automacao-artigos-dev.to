import re
from http import HTTPStatus
from pathlib import Path
from typing import Any

import frontmatter
import httpx

from src.logger import setup_logger

logger = setup_logger(__name__)

DEVTO_API_URL = "https://dev.to/api/articles"
TIMEOUT_SEGUNDOS = 30
MAX_IMAGENS = 5


class PublicadorDevto:
    def __init__(self, api_key: str):
        if not api_key:
            msg = "DEVTO_API_KEY não configurada"
            raise ValueError(msg)
        self.api_key = api_key

    def publicar(
        self,
        arquivo: Path,
        publicado: bool = False,
        source_dir: Path | None = None,
    ) -> dict[str, Any]:
        if not arquivo.exists():
            msg = f"Arquivo não encontrado: {arquivo}"
            raise FileNotFoundError(msg)

        raw = frontmatter.load(arquivo)
        conteudo = raw.content.strip()
        meta: dict[str, Any] = dict(raw.metadata)

        if source_dir:
            conteudo = self._processar_imagens(conteudo, source_dir)

        titulo = meta.get("title") or self._extrair_titulo(conteudo)
        payload = self._montar_payload(conteudo, titulo, publicado, meta)

        logger.info(
            "Publicando artigo '%s' no Dev.to (publicado=%s)",
            titulo,
            publicado,
        )
        return self._enviar(payload)

    def _extrair_titulo(self, conteudo: str) -> str:
        for linha in conteudo.splitlines():
            if linha.startswith("# ") and not linha.startswith("## "):
                return linha.lstrip("# ").strip()
        return "Artigo sem título"

    def _montar_payload(
        self,
        conteudo: str,
        titulo: str,
        publicado: bool,
        meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        article: dict[str, Any] = {
            "title": titulo,
            "body_markdown": conteudo,
            "published": publicado,
        }

        if meta:
            descricao = meta.get("description", "")
            if descricao:
                article["description"] = descricao

            tags = meta.get("tags", "")
            if tags:
                if isinstance(tags, list):
                    article["tags"] = ", ".join(tags)
                else:
                    article["tags"] = str(tags)

        return {"article": article}

    def _processar_imagens(self, conteudo: str, source_dir: Path) -> str:
        padrao = re.compile(r"!\[(.*?)\]\(([^)]+)\)")
        substituicoes: list[tuple[str, str]] = []
        detalhes: list[str] = []

        for match in padrao.finditer(conteudo):
            alt = match.group(1)
            caminho = match.group(2)
            if caminho.startswith(("http://", "https://", "data:")):
                continue
            placeholder = (
                f"[⚠ IMAGEM: {caminho}"
                " — faça upload manual no Dev.to"
                f' — alt: "{alt}"]'
            )
            substituicoes.append((match.group(0), placeholder))
            detalhes.append(f'{caminho} (alt: "{alt}")')

        if not substituicoes:
            return conteudo

        if len(substituicoes) > MAX_IMAGENS:
            logger.warning(
                "Artigo com %d imagens locais, exibindo %d",
                len(substituicoes),
                MAX_IMAGENS,
            )
            substituicoes = substituicoes[:MAX_IMAGENS]
            detalhes = detalhes[:MAX_IMAGENS]

        resultado = conteudo
        for original, placeholder in substituicoes:
            resultado = resultado.replace(original, placeholder)

        logger.warning(
            "Dev.to API não suporta upload de imagens. "
            "%d imagem(ns) substituída(s) por placeholders:\n  %s",
            len(substituicoes),
            "\n  ".join(detalhes),
        )

        return resultado

    def _enviar(self, payload: dict[str, Any]) -> dict[str, Any]:
        with httpx.Client(timeout=TIMEOUT_SEGUNDOS) as client:
            try:
                resp = client.post(
                    DEVTO_API_URL,
                    json=payload,
                    headers={"api-key": self.api_key},
                )
            except httpx.TimeoutException:
                msg = "Timeout ao conectar com Dev.to"
                logger.error(msg)
                raise RuntimeError(msg)
            except httpx.RequestError as e:
                msg = f"Erro de conexão com Dev.to: {e}"
                logger.error(msg)
                raise RuntimeError(msg)

            if resp.status_code == HTTPStatus.UNAUTHORIZED:
                msg = "Chave API Dev.to inválida"
                logger.error(msg)
                raise PermissionError(msg)

            if resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
                erros = resp.json()
                detalhes = erros.get("error", str(erros))
                msg = f"Erro de validação no Dev.to: {detalhes}"
                logger.error(msg)
                raise ValueError(msg)

            if resp.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                msg = "Limite de requisições excedido no Dev.to"
                logger.error(msg)
                raise RuntimeError(msg)

            resp.raise_for_status()

            dados = resp.json()
            logger.info(
                "Artigo publicado: %s",
                dados.get("url", "URL desconhecida"),
            )
            return dados
