import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from src.config import Config
from src.services.generator import gerar_artigo
from src.services.publisher import PublicadorDevto
from src.services.telegram_bot import TelegramBotService

app = typer.Typer()
console = Console()


@app.callback()
def main():
    pass


@app.command()
def generate(
    source: Path = typer.Option(
        "source", "--source", help="Diretório com anotações"
    ),
    output: Path = typer.Option(
        "artigos", "--output", help="Diretório para artigos"
    ),
    template: Path = typer.Option(
        "templates/prompt_template.md",
        "--template",
        help="Template do prompt Agno",
    ),
    verbose: bool = typer.Option(False, "--verbose", help="Exibir progresso"),
):
    config = Config(
        source_dir=source,
        output_dir=output,
        template_path=template,
        verbose=verbose,
    )

    with console.status("[bold green]Lendo anotações...") as status:
        try:
            status.update("[bold green]Lendo anotações...")
            artigo = gerar_artigo(config)

            status.update("[bold green]Artigo gerado com sucesso!")
            console.print(
                f"\n[green]✓[/] Artigo salvo em: "
                f"{output / artigo.titulo.lower().replace(' ', '-')[:50]}.md"
            )
        except ValueError as e:
            console.print(f"\n[yellow]⚠[/] {e}")
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"\n[red]✗[/] Erro: {e}")
            raise typer.Exit(code=1)


@app.command()
def publish(
    nome: str = typer.Argument(
        ..., help="Nome do arquivo do artigo (com ou sem .md)"
    ),
    published: bool = typer.Option(
        False, "--published", help="Publicar (padrão: rascunho)"
    ),
    devto_key: Optional[str] = typer.Option(
        None,
        "--devto-key",
        help="Chave API Dev.to (ou usar DEVTO_API_KEY env)",
    ),
    output: Path = typer.Option(
        "artigos", "--output", help="Diretório com artigos gerados"
    ),
    source: Path = typer.Option(
        "source", "--source", help="Diretório com imagens das anotações"
    ),
):
    chave = devto_key or os.getenv("DEVTO_API_KEY")
    if not chave:
        console.print(
            "[red]✗[/] DEVTO_API_KEY não configurada. "
            "Defina em .env ou use --devto-key"
        )
        raise typer.Exit(code=1)

    arquivo = _buscar_arquivo(nome, output)
    if arquivo is None:
        _listar_artigos(output)
        raise typer.Exit(code=1)

    try:
        publisher = PublicadorDevto(chave)
        with console.status("[bold green]Publicando no Dev.to..."):
            resultado = publisher.publicar(
                arquivo, publicado=published, source_dir=source
            )

        console.print("\n[green]✓[/] Artigo publicado com sucesso!")
        url = resultado.get("url", "desconhecida")
        console.print(f"   URL: [blue]{url}[/]")
        console.print(f"   ID:  {resultado.get('id', '?')}")
        _limpar_source(source)

    except PermissionError as e:
        console.print(f"\n[red]✗[/] {e}")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"\n[yellow]⚠[/] {e}")
        raise typer.Exit(code=1)
    except (FileNotFoundError, RuntimeError) as e:
        console.print(f"\n[red]✗[/] {e}")
        raise typer.Exit(code=1)


@app.command()
def bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        console.print(
            "[red]✗[/] TELEGRAM_BOT_TOKEN não configurado. Defina em .env"
        )
        raise typer.Exit(code=1)

    try:
        service = TelegramBotService(token)
        console.print("[green]✓[/] Bot iniciado! Pressione Ctrl+C para parar.")
        service.start()
    except Exception as e:
        console.print(f"\n[red]✗[/] Erro ao iniciar bot: {e}")
        raise typer.Exit(code=1)


def _limpar_source(source_dir: Path) -> None:
    if not source_dir.exists():
        return
    for arq in source_dir.glob("*.md"):
        arq.unlink()


def _buscar_arquivo(nome: str, diretorio: Path) -> Optional[Path]:
    caminho = diretorio / nome
    if caminho.exists() and caminho.is_file():
        return caminho

    if not nome.endswith(".md"):
        caminho = diretorio / f"{nome}.md"
        if caminho.exists():
            return caminho

    return None


def _listar_artigos(diretorio: Path) -> None:
    if not diretorio.exists():
        console.print(f"\n[yellow]⚠[/] Diretório não encontrado: {diretorio}")
        return

    arquivos = sorted(diretorio.glob("*.md"))
    if not arquivos:
        console.print(
            f"\n[yellow]⚠[/] Nenhum artigo encontrado em {diretorio}"
        )
        return

    console.print("\n[bold]Artigos disponíveis:[/]")
    for a in arquivos:
        console.print(f"  [cyan]{a.name}[/]")
