import pytest

from src.services.template import TemplateRenderer


def test_renderizar_com_todos_campos(tmp_path):
    template = tmp_path / "template.md"
    template.write_text("# {{titulo}}\n\n{{conteudo}}\n\nTags: {{tags}}")
    renderer = TemplateRenderer(template)
    resultado = renderer.renderizar(
        conteudo="Meu texto",
        titulo="Meu Artigo",
        tags="python, dev",
    )
    assert "Meu Artigo" in resultado
    assert "Meu texto" in resultado
    assert "python, dev" in resultado


def test_renderizar_valores_default(tmp_path):
    template = tmp_path / "template.md"
    template.write_text("# {{titulo}}\n\n{{conteudo}}\n\nTags: {{tags}}")
    renderer = TemplateRenderer(template)
    resultado = renderer.renderizar(conteudo="texto")
    assert "Artigo sem título" in resultado
    assert resultado.count("texto") == 1
    assert resultado.count("Tags: ") == 1


def test_template_nao_encontrado(tmp_path):
    inexistente = tmp_path / "inexistente.md"
    renderer = TemplateRenderer(inexistente)
    with pytest.raises(FileNotFoundError, match="inexistente"):
        renderer.renderizar(conteudo="texto")


def test_renderizar_sem_variaveis(tmp_path):
    template = tmp_path / "fixo.md"
    template.write_text("Conteúdo fixo sem variáveis")
    renderer = TemplateRenderer(template)
    resultado = renderer.renderizar(conteudo="ignorado")
    assert resultado == "Conteúdo fixo sem variáveis"


def test_renderizar_template_vazio(tmp_path):
    template = tmp_path / "vazio.md"
    template.write_text("")
    renderer = TemplateRenderer(template)
    resultado = renderer.renderizar(conteudo="texto")
    assert resultado == ""


def test_carregar_template_lanca_erro(tmp_path):
    template = tmp_path / "semdiretorio.md"
    renderer = TemplateRenderer(template)
    with pytest.raises(FileNotFoundError):
        renderer._carregar()


def test_renderizar_com_imagens(tmp_path):
    template = tmp_path / "template.md"
    template.write_text("# {{titulo}}\n\n{{imagens}}\n\n{{conteudo}}")
    renderer = TemplateRenderer(template)
    resultado = renderer.renderizar(
        conteudo="texto",
        titulo="Artigo",
        imagens="- `foto.png`\n- `diagrama.jpg`",
    )
    assert "`foto.png`" in resultado
    assert "`diagrama.jpg`" in resultado
