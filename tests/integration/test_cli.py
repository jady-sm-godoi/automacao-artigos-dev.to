from typer.testing import CliRunner

from src.cli import app

runner = CliRunner()


def test_generate_source_dir_inexistente(tmp_path):
    result = runner.invoke(
        app,
        [
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
        ["--source", str(source), "--output", str(tmp_path / "out")],
    )
    assert result.exit_code == 1


def test_generate_com_arquivo_curto(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "curta.md").write_text("curto demais")
    result = runner.invoke(
        app,
        ["--source", str(source), "--output", str(tmp_path / "out")],
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
            "--source",
            str(source),
            "--output",
            str(out),
            "--verbose",
        ],
    )
    assert result.exit_code == 1
