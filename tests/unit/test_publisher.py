from http import HTTPStatus
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.services.publisher import MAX_IMAGENS, PublicadorDevto


def test_init_key_vazia():
    with pytest.raises(ValueError, match="DEVTO_API_KEY"):
        PublicadorDevto("")


def test_init_key_valida():
    publisher = PublicadorDevto("chave-valida")
    assert publisher.api_key == "chave-valida"


def test_extrair_titulo_com_h1():
    publisher = PublicadorDevto("chave")
    conteudo = "# Meu Titulo\n\nConteudo do artigo..."
    assert publisher._extrair_titulo(conteudo) == "Meu Titulo"


def test_extrair_titulo_sem_h1():
    publisher = PublicadorDevto("chave")
    conteudo = "apenas texto sem heading"
    assert publisher._extrair_titulo(conteudo) == "Artigo sem título"


def test_extrair_titulo_ignora_h2():
    publisher = PublicadorDevto("chave")
    conteudo = "## Subtitulo\n\n# Titulo Principal\nmais texto"
    assert publisher._extrair_titulo(conteudo) == "Titulo Principal"


def test_extrair_titulo_com_espacos():
    publisher = PublicadorDevto("chave")
    conteudo = "#    Titulo com espacos    "
    assert publisher._extrair_titulo(conteudo) == "Titulo com espacos"


def test_montar_payload_draft():
    publisher = PublicadorDevto("chave")
    payload = publisher._montar_payload(
        "# Teste\nconteudo", "Teste", publicado=False
    )
    assert payload["article"]["title"] == "Teste"
    assert payload["article"]["body_markdown"] == "# Teste\nconteudo"
    assert payload["article"]["published"] is False


def test_montar_payload_publicado():
    publisher = PublicadorDevto("chave")
    payload = publisher._montar_payload(
        "# Teste\nconteudo", "Teste", publicado=True
    )
    assert payload["article"]["published"] is True


def test_publicar_arquivo_inexistente(tmp_path):
    publisher = PublicadorDevto("chave")
    inexistente = tmp_path / "nao-existe.md"
    with pytest.raises(FileNotFoundError, match="nao-existe"):
        publisher.publicar(inexistente)


@patch("src.services.publisher.httpx.Client")
def test_enviar_sucesso(mock_client_class):
    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.CREATED
    mock_resp.json.return_value = {
        "url": "https://dev.to/user/meu-artigo",
        "id": 123,
    }
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    resultado = publisher._enviar(
        {"article": {"title": "Teste", "body_markdown": "# Teste"}}
    )

    assert resultado["url"] == "https://dev.to/user/meu-artigo"
    assert resultado["id"] == 123
    mock_instance.post.assert_called_once()


@patch("src.services.publisher.httpx.Client")
def test_enviar_401(mock_client_class):
    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.UNAUTHORIZED
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    with pytest.raises(PermissionError, match="Chave API"):
        publisher._enviar({"article": {}})


@patch("src.services.publisher.httpx.Client")
def test_enviar_422(mock_client_class):
    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    mock_resp.json.return_value = {"error": "title can't be blank"}
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    with pytest.raises(ValueError, match="Erro de validação"):
        publisher._enviar({"article": {}})


@patch("src.services.publisher.httpx.Client")
def test_enviar_429(mock_client_class):
    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.TOO_MANY_REQUESTS
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    with pytest.raises(RuntimeError, match="Limite de requisições"):
        publisher._enviar({"article": {}})


@patch("src.services.publisher.httpx.Client")
def test_enviar_timeout(mock_client_class):
    mock_instance = MagicMock()
    mock_instance.post.side_effect = httpx.TimeoutException(
        "timeout", request=MagicMock()
    )
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    with pytest.raises(RuntimeError, match="Timeout"):
        publisher._enviar({"article": {}})


@patch("src.services.publisher.httpx.Client")
def test_enviar_erro_conexao(mock_client_class):
    mock_instance = MagicMock()
    mock_instance.post.side_effect = httpx.RequestError(
        "connection failed", request=MagicMock()
    )
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    with pytest.raises(RuntimeError, match="Erro de conexão"):
        publisher._enviar({"article": {}})


def test_montar_payload_com_meta_completa():
    publisher = PublicadorDevto("chave")
    meta = {
        "title": "Titulo FM",
        "description": "Resumo do artigo",
        "tags": "python, dev",
    }
    payload = publisher._montar_payload("# Conteudo", "Titulo FM", False, meta)
    assert payload["article"]["title"] == "Titulo FM"
    assert payload["article"]["description"] == "Resumo do artigo"
    assert payload["article"]["tags"] == "python, dev"


def test_montar_payload_com_tags_lista():
    publisher = PublicadorDevto("chave")
    meta = {"tags": ["python", "dev", "tutorial"]}
    payload = publisher._montar_payload("# Conteudo", "Titulo", False, meta)
    assert payload["article"]["tags"] == "python, dev, tutorial"


def test_montar_payload_meta_sem_campos_extras():
    publisher = PublicadorDevto("chave")
    payload = publisher._montar_payload("# Conteudo", "Titulo", False, None)
    assert "description" not in payload["article"]
    assert "tags" not in payload["article"]


def test_publicar_arquivo_com_frontmatter(tmp_path):
    arquivo = tmp_path / "artigo-fm.md"
    arquivo.write_text(
        "---\n"
        "title: Artigo com Frontmatter\n"
        "description: Meu resumo legal\n"
        "tags: python, dev, speckit\n"
        "---\n\n"
        "# Artigo com Frontmatter\n\n"
        "Conteudo do artigo com frontmatter."
    )

    publisher = PublicadorDevto("chave-valida")

    titulo = publisher._extrair_titulo("---\ntitle: x\n---\n\n# H1 do corpo")
    assert titulo == "H1 do corpo"


@patch("src.services.publisher.httpx.Client")
def test_publicar_com_arquivo_real(mock_client_class, tmp_path):
    arquivo = tmp_path / "meu-artigo.md"
    arquivo.write_text("# Meu Artigo Publicado\n\nConteudo do artigo aqui.")

    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.CREATED
    mock_resp.json.return_value = {
        "url": "https://dev.to/user/meu-artigo-123",
        "id": 456,
    }
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave-valida")
    resultado = publisher.publicar(arquivo)

    assert resultado["id"] == 456
    assert resultado["url"] == "https://dev.to/user/meu-artigo-123"

    chamada = mock_instance.post.call_args
    payload = chamada[1]["json"]
    assert payload["article"]["title"] == "Meu Artigo Publicado"


@patch("src.services.publisher.httpx.Client")
def test_publicar_com_frontmatter(mock_client_class, tmp_path):
    arquivo = tmp_path / "frontmatter.md"
    arquivo.write_text(
        "---\n"
        "title: Artigo com Frontmatter\n"
        "description: Meu resumo legal\n"
        "tags: python, dev, speckit\n"
        "---\n\n"
        "# Artigo com Frontmatter\n\n"
        "Conteudo do artigo com frontmatter."
    )

    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.CREATED
    mock_resp.json.return_value = {
        "url": "https://dev.to/user/artigo-fm",
        "id": 789,
    }
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave-valida")
    resultado = publisher.publicar(arquivo)

    assert resultado["id"] == 789
    assert resultado["url"] == "https://dev.to/user/artigo-fm"

    chamada = mock_instance.post.call_args
    payload = chamada[1]["json"]
    article = payload["article"]

    assert article["title"] == "Artigo com Frontmatter"
    assert article["description"] == "Meu resumo legal"
    assert article["tags"] == "python, dev, speckit"
    assert "---" not in article["body_markdown"][:5]


def test_processar_imagens_substitui_por_placeholder(tmp_path):
    publisher = PublicadorDevto("chave")
    conteudo = "texto com ![img1](imagens/foo.png) e ![img2](imagens/bar.jpg)"
    source_dir = tmp_path
    (source_dir / "imagens").mkdir()
    (source_dir / "imagens" / "foo.png").write_bytes(b"foto")
    (source_dir / "imagens" / "bar.jpg").write_bytes(b"foto2")

    resultado = publisher._processar_imagens(conteudo, source_dir)

    assert "IMAGEM: imagens/foo.png" in resultado
    assert "IMAGEM: imagens/bar.jpg" in resultado
    assert "faça upload manual" in resultado
    assert 'alt: "img1"' in resultado
    assert 'alt: "img2"' in resultado


def test_processar_imagens_ignora_urls_externas(tmp_path):
    publisher = PublicadorDevto("chave")
    conteudo = "![local](imagens/a.png) ![web](https://exemplo.com/img.png)"
    source_dir = tmp_path
    (source_dir / "imagens").mkdir()
    (source_dir / "imagens" / "a.png").write_bytes(b"foto")

    resultado = publisher._processar_imagens(conteudo, source_dir)

    assert "IMAGEM: imagens/a.png" in resultado
    assert "https://exemplo.com/img.png" in resultado


def test_processar_imagens_limita_maximo(tmp_path):
    publisher = PublicadorDevto("chave")
    caminhos = " ".join(f"![img{i}](imagens/img{i}.png)" for i in range(10))
    conteudo = f"texto {caminhos}"
    source_dir = tmp_path
    (source_dir / "imagens").mkdir()
    for i in range(10):
        (source_dir / "imagens" / f"img{i}.png").write_bytes(b"x")

    resultado = publisher._processar_imagens(conteudo, source_dir)

    placeholders = resultado.count("IMAGEM:")
    assert placeholders == MAX_IMAGENS


def test_processar_imagens_sem_caminhos_locais(tmp_path):
    publisher = PublicadorDevto("chave")
    conteudo = "![web1](https://img.com/a.png) ![web2](http://img.com/b.jpg)"
    resultado = publisher._processar_imagens(conteudo, tmp_path)
    assert resultado == conteudo


@patch("src.services.publisher.httpx.Client")
def test_publicar_com_imagens_placeholders(mock_client_class, tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    img_dir = source_dir / "imagens"
    img_dir.mkdir()
    (img_dir / "diagrama.png").write_bytes(b"png")

    artigo = tmp_path / "artigo.md"
    artigo.write_text(
        "---\ntitle: Com Imagens\ndescription: Teste\n"
        "tags: dev\n---\n\n"
        "# Com Imagens\n\n"
        "![Diagrama](imagens/diagrama.png)"
    )

    mock_instance = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = HTTPStatus.CREATED
    mock_resp.json.return_value = {
        "url": "https://dev.to/u/artigo",
        "id": 999,
    }
    mock_instance.post.return_value = mock_resp
    mock_client_class.return_value.__enter__.return_value = mock_instance

    publisher = PublicadorDevto("chave")
    resultado = publisher.publicar(artigo, source_dir=source_dir)

    assert resultado["id"] == 999
    chamada = mock_instance.post.call_args
    payload = chamada[1]["json"]
    body = payload["article"]["body_markdown"]
    assert "IMAGEM:" in body
    assert "faça upload manual" in body
    assert 'alt: "Diagrama"' in body
