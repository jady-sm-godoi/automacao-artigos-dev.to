from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Anotacao:
    caminho: Path
    nome: str
    conteudo: str
    frontmatter: dict = field(default_factory=dict)
    tamanho: int = 0


@dataclass
class Artigo:
    titulo: str
    conteudo: str
    tags: list[str] = field(default_factory=list)
    data_criacao: datetime = field(default_factory=datetime.now)
    fontes: list[Path] = field(default_factory=list)
