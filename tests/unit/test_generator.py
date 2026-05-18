from pathlib import Path

from src.config import Config
from src.models.artigo import Anotacao
from src.services.generator import EXTENSOES_VALIDAS, GeradorArtigo


def test_extensoes_validas():
    assert ".md" in EXTENSOES_VALIDAS
    assert ".markdown" in EXTENSOES_VALIDAS
    assert len(EXTENSOES_VALIDAS) == 2


def test_nome_arquivo_slug():
    config = Config(output_dir=Path("/tmp"))
    gerador = GeradorArtigo(config)
    nome = gerador._nome_arquivo("Meu Artigo Legal!")
    assert nome.endswith(".md")
    assert nome.startswith("meu-artigo-legal")


def test_nome_arquivo_artigo_quando_slug_vazio():
    config = Config(output_dir=Path("/tmp"))
    gerador = GeradorArtigo(config)
    nome = gerador._nome_arquivo("   !@#$ ")
    assert nome == "artigo.md"


def test_montar_conteudo_com_anotacoes():
    config = Config()
    gerador = GeradorArtigo(config)
    anotacoes = [
        Anotacao(
            caminho=Path("a.md"),
            nome="a",
            conteudo="conteudo a",
            frontmatter={"titulo": "Teste", "tags": ["python"]},
            tamanho=10,
        ),
        Anotacao(
            caminho=Path("b.md"),
            nome="b",
            conteudo="conteudo b",
            frontmatter={"tags": ["dev", "python"]},
            tamanho=10,
        ),
    ]
    conteudo, titulo, tags_str = gerador._montar_conteudo(anotacoes)
    assert titulo == "Teste"
    assert "python" in tags_str
    assert "dev" in tags_str


def test_montar_conteudo_sem_anotacoes():
    config = Config()
    gerador = GeradorArtigo(config)
    conteudo, titulo, tags_str = gerador._montar_conteudo([])
    assert conteudo == ""
    assert titulo == "Artigo sem título"
    assert tags_str == ""


def test_montar_conteudo_titulo_fallback():
    config = Config()
    gerador = GeradorArtigo(config)
    anotacoes = [
        Anotacao(
            caminho=Path("x.md"),
            nome="x",
            conteudo="texto",
            frontmatter={"title": "Fallback Title"},
            tamanho=5,
        ),
    ]
    _, titulo, _ = gerador._montar_conteudo(anotacoes)
    assert titulo == "Fallback Title"


def test_montar_conteudo_tags_unicas():
    config = Config()
    gerador = GeradorArtigo(config)
    anotacoes = [
        Anotacao(
            caminho=Path("a.md"),
            nome="a",
            conteudo="x",
            frontmatter={"tags": ["python", "python", "dev"]},
            tamanho=1,
        ),
    ]
    _, _, tags_str = gerador._montar_conteudo(anotacoes)
    assert tags_str.count("python") == 1


def test_slug_titulo_curto():
    config = Config(output_dir=Path("/tmp"))
    gerador = GeradorArtigo(config)
    nome = gerador._nome_arquivo("A")
    assert nome == "a.md"


def test_slug_titulo_50_caracteres():
    config = Config(output_dir=Path("/tmp"))
    gerador = GeradorArtigo(config)
    titulo_longo = "a" * 100
    nome = gerador._nome_arquivo(titulo_longo)
    assert len(nome) <= 53
    assert nome.endswith(".md")
