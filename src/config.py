from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    source_dir: Path = Path("source")
    output_dir: Path = Path("artigos")
    template_path: Path = Path("templates/prompt_template.md")
    modelo: str = "gpt-4o"
    verbose: bool = True
    telegram_token: str | None = None
