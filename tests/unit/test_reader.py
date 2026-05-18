from src.services.reader import TAMANHO_MINIMO, MarkdownReader


def test_listar_arquivos_dir_inexistente(tmp_path):
    inexistente = tmp_path / "nada"
    reader = MarkdownReader(inexistente)
    assert reader.listar_arquivos() == []


def test_listar_arquivos_ignora_nao_md(tmp_path):
    (tmp_path / "nota.txt").write_text("conteudo")
    (tmp_path / "foto.png").write_bytes(b"123")
    reader = MarkdownReader(tmp_path)
    assert reader.listar_arquivos() == []


def test_listar_arquivos_apenas_md(tmp_path):
    (tmp_path / "a.md").write_text("conteudo")
    (tmp_path / "b.md").write_text("conteudo")
    reader = MarkdownReader(tmp_path)
    arquivos = reader.listar_arquivos()
    assert len(arquivos) == 2
    assert all(f.suffix == ".md" for f in arquivos)


def test_listar_arquivos_recursivo(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "a.md").write_text("x")
    (sub / "b.md").write_text("x")
    reader = MarkdownReader(tmp_path)
    assert len(reader.listar_arquivos()) == 2


def test_ler_anotacao_vazia_retorna_none(tmp_path):
    caminho = tmp_path / "vazio.md"
    caminho.write_text("")
    reader = MarkdownReader(tmp_path)
    assert reader.ler_anotacao(caminho) is None


def test_ler_anotacao_curta_retorna_none(tmp_path):
    caminho = tmp_path / "curto.md"
    caminho.write_text("a" * (TAMANHO_MINIMO - 1))
    reader = MarkdownReader(tmp_path)
    assert reader.ler_anotacao(caminho) is None


def test_ler_anotacao_valida(tmp_path):
    caminho = tmp_path / "valida.md"
    conteudo = "a" * TAMANHO_MINIMO
    caminho.write_text(conteudo)
    reader = MarkdownReader(tmp_path)
    anotacao = reader.ler_anotacao(caminho)
    assert anotacao is not None
    assert anotacao.conteudo == conteudo
    assert anotacao.caminho == caminho
    assert anotacao.nome == "valida"


def test_ler_anotacao_com_frontmatter(tmp_path):
    caminho = tmp_path / "com_fm.md"
    caminho.write_text(
        "---\ntitle: Test\ntags: [python, dev]\n---\n" + "a" * TAMANHO_MINIMO
    )
    reader = MarkdownReader(tmp_path)
    anotacao = reader.ler_anotacao(caminho)
    assert anotacao is not None
    assert anotacao.frontmatter["title"] == "Test"
    assert anotacao.frontmatter["tags"] == ["python", "dev"]


def test_ler_todas_com_mistura(tmp_path):
    (tmp_path / "a.md").write_text("a" * TAMANHO_MINIMO)
    (tmp_path / "b.md").write_text("")
    (tmp_path / "c.md").write_text("curto")
    reader = MarkdownReader(tmp_path)
    anotacoes, ignorados = reader.ler_todas()
    assert len(anotacoes) == 1
    assert ignorados == 2


def test_ler_todas_sem_arquivos(tmp_path):
    reader = MarkdownReader(tmp_path)
    anotacoes, ignorados = reader.ler_todas()
    assert anotacoes == []
    assert ignorados == 0


def test_tamanho_propriedade_anotacao(tmp_path):
    caminho = tmp_path / "tamanho.md"
    conteudo = "x" * 200
    caminho.write_text(conteudo)
    reader = MarkdownReader(tmp_path)
    anotacao = reader.ler_anotacao(caminho)
    assert anotacao is not None
    assert anotacao.tamanho == 200
