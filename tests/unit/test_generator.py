from pathlib import Path

from src.config import Config
from src.models.artigo import Anotacao
from src.services.generator import (
    EXTENSOES_VALIDAS,
    FORMATOS_IMAGEM,
    GeradorArtigo,
)


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


def test_formatos_imagem():
    assert ".png" in FORMATOS_IMAGEM
    assert ".jpg" in FORMATOS_IMAGEM
    assert ".jpeg" in FORMATOS_IMAGEM
    assert ".gif" in FORMATOS_IMAGEM
    assert ".webp" in FORMATOS_IMAGEM
    assert len(FORMATOS_IMAGEM) == 5


def test_listar_imagens_sem_pasta(tmp_path):
    config = Config(source_dir=tmp_path / "inexistente")
    gerador = GeradorArtigo(config)
    resultado = gerador._listar_imagens()
    assert "Nenhuma imagem" in resultado


def test_listar_imagens_com_arquivos(tmp_path):
    img_dir = tmp_path / "imagens"
    img_dir.mkdir()
    (img_dir / "foto.png").write_bytes(b"x")
    (img_dir / "diagrama.jpg").write_bytes(b"x")
    (img_dir / "nota.txt").write_text("ignorado")

    config = Config(source_dir=tmp_path)
    gerador = GeradorArtigo(config)
    resultado = gerador._listar_imagens()

    assert "foto.png" in resultado
    assert "diagrama.jpg" in resultado
    assert "nota.txt" not in resultado


def test_listar_imagens_vazio(tmp_path):
    img_dir = tmp_path / "imagens"
    img_dir.mkdir()

    config = Config(source_dir=tmp_path)
    gerador = GeradorArtigo(config)
    resultado = gerador._listar_imagens()

    assert "Nenhuma imagem" in resultado


def test_copiar_imagens_para_output(tmp_path):
    img_dir = tmp_path / "source" / "imagens"
    img_dir.mkdir(parents=True)
    (img_dir / "foto.png").write_bytes(b"png")
    (img_dir / "diagrama.jpg").write_bytes(b"jpg")
    (img_dir / "nota.txt").write_text("ignorado")

    config = Config(
        source_dir=tmp_path / "source", output_dir=tmp_path / "artigos"
    )
    gerador = GeradorArtigo(config)
    gerador._copiar_imagens()

    destino = tmp_path / "artigos" / "imagens"
    assert (destino / "foto.png").exists()
    assert (destino / "diagrama.jpg").exists()
    assert not (destino / "nota.txt").exists()


def test_copiar_imagens_sem_pasta(tmp_path):
    config = Config(
        source_dir=tmp_path / "source", output_dir=tmp_path / "artigos"
    )
    gerador = GeradorArtigo(config)
    gerador._copiar_imagens()

    destino = tmp_path / "artigos" / "imagens"
    assert not destino.exists()


def test_listar_imagens_maximo(tmp_path):
    img_dir = tmp_path / "imagens"
    img_dir.mkdir()
    for i in range(10):
        (img_dir / f"img{i}.png").write_bytes(b"x")

    config = Config(source_dir=tmp_path)
    gerador = GeradorArtigo(config)
    resultado = gerador._listar_imagens()

    linhas = resultado.strip().split("\n")
    assert len(linhas) == 5


def test_slug_titulo_50_caracteres():
    config = Config(output_dir=Path("/tmp"))
    gerador = GeradorArtigo(config)
    titulo_longo = "a" * 100
    nome = gerador._nome_arquivo(titulo_longo)
    assert len(nome) <= 53
    assert nome.endswith(".md")


def test_normalizar_frontmatter_sem_wrapper():
    conteudo = '---\ntitle: "Teste"\n---\n\n# Corpo do artigo'
    resultado = GeradorArtigo._normalizar_frontmatter(conteudo)
    assert resultado == conteudo


def test_normalizar_frontmatter_com_wrapper_yaml():
    conteudo = '```yaml\n---\ntitle: "Teste"\n---\n```\n\n# Corpo do artigo'
    resultado = GeradorArtigo._normalizar_frontmatter(conteudo)
    assert resultado.startswith("---")
    assert "```" not in resultado
    assert "# Corpo do artigo" in resultado


def test_normalizar_frontmatter_com_wrapper_sem_yaml():
    conteudo = '```\n---\ntitle: "Teste"\n---\n```\n\n# Corpo'
    resultado = GeradorArtigo._normalizar_frontmatter(conteudo)
    assert resultado.startswith("---")
    assert "```" not in resultado
