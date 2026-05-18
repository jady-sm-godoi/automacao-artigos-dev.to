from pathlib import Path

import typer
from rich.console import Console

from src.config import Config
from src.services.generator import gerar_artigo

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def main(
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
