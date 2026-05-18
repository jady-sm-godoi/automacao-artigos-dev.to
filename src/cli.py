from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.config import Config
from src.services.generator import gerar_artigo

console = Console()


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

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        disable=not (verbose or True),
    ) as progress:
        progress.add_task(description="Gerando artigo...", total=None)

        try:
            artigo = gerar_artigo(config)
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


def app():
    typer.run(generate)
