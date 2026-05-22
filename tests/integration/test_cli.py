from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from src.cli import app

runner = CliRunner()


def test_generate_source_dir_inexistente(tmp_path):
    result = runner.invoke(
        app,
        [
            "generate",
            "--source",
            str(tmp_path / "inexistente"),
            "--output",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == 1
    assert "Nenhuma anotação" in result.stdout


def test_generate_sem_arquivos_md(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "nota.txt").write_text("apenas texto")
    result = runner.invoke(
        app,
        [
            "generate",
            "--source",
            str(source),
            "--output",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == 1


def test_generate_com_arquivo_curto(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "curta.md").write_text("curto demais")
    result = runner.invoke(
        app,
        [
            "generate",
            "--source",
            str(source),
            "--output",
            str(tmp_path / "out"),
        ],
    )
    assert result.exit_code == 1


def test_generate_com_verbose_flag(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    out = tmp_path / "out"
    (source / "valida.md").write_text("a" * 200)
    result = runner.invoke(
        app,
        [
            "generate",
            "--source",
            str(source),
            "--output",
            str(out),
            "--verbose",
        ],
    )
    assert result.exit_code == 1


def test_publish_sem_chave(tmp_path, monkeypatch):
    monkeypatch.delenv("DEVTO_API_KEY", raising=False)
    out = tmp_path / "artigos"
    out.mkdir()
    (out / "artigo.md").write_text("# Titulo\n\nconteudo")
    result = runner.invoke(
        app,
        [
            "publish",
            "artigo",
            "--output",
            str(out),
        ],
    )
    assert result.exit_code == 1
    assert "DEVTO_API_KEY" in result.stdout


def test_publish_artigo_inexistente(tmp_path, monkeypatch):
    monkeypatch.setenv("DEVTO_API_KEY", "fake-key")
    (tmp_path / "outro-artigo.md").write_text("# Outro\n\nconteudo")
    (tmp_path / "mais-um.md").write_text("# Mais\n\nconteudo")

    result = runner.invoke(
        app,
        [
            "publish",
            "artigo-invalido",
            "--output",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 1
    assert "Artigos disponíveis" in result.stdout
    assert "outro-artigo.md" in result.stdout
    assert "mais-um.md" in result.stdout


def test_bot_help():
    result = runner.invoke(app, ["bot", "--help"])
    assert result.exit_code == 0


def test_bot_sem_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    result = runner.invoke(app, ["bot"])
    assert result.exit_code == 1
    assert "TELEGRAM_BOT_TOKEN" in result.stdout


def test_bot_com_token_cria_service(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token-123")
    with patch("src.cli.TelegramBotService") as mock_service:
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance

        result = runner.invoke(app, ["bot"])

    assert result.exit_code == 0
