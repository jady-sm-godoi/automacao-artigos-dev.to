from pathlib import Path


class TemplateRenderer:
    def __init__(self, template_path: Path):
        self.template_path = template_path

    def _carregar(self) -> str:
        if not self.template_path.exists():
            msg = f"Template não encontrado: {self.template_path}"
            raise FileNotFoundError(msg)
        return self.template_path.read_text(encoding="utf-8")

    def renderizar(
        self,
        conteudo: str,
        titulo: str = "Artigo sem título",
        tags: str = "",
        imagens: str = "",
    ) -> str:
        template = self._carregar()
        return (
            template.replace("{{conteudo}}", conteudo)
            .replace("{{titulo}}", titulo)
            .replace("{{tags}}", tags)
            .replace("{{imagens}}", imagens)
        )
