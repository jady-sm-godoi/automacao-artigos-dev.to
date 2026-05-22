import asyncio
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.logger import setup_logger

logger = setup_logger(__name__)

TAMANHO_MINIMO_ANOTACAO = 100
LIMITE_TEXTO_TELEGRAM = 4000
TIMEOUT_GERACAO = 180
FORMATOS_IMAGEM = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def _gerar_nome_anotacao(chat_id: int) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{chat_id}.md"


def _gerar_nome_imagem(chat_id: int, extensao: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{chat_id}{extensao}"


class TelegramBotService:
    def __init__(self, token: str, source_dir: Path = Path("source")):
        self.token = token
        self.source_dir = source_dir
        self.imagens_dir = source_dir / "imagens"
        self.application: Application | None = None
        self._running = False

    def _garantir_diretorios(self) -> None:
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.imagens_dir.mkdir(parents=True, exist_ok=True)

    def _build_application(self) -> Application:
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self._cmd_start))
        application.add_handler(CommandHandler("ajuda", self._cmd_ajuda))
        application.add_handler(CommandHandler("gerar", self._cmd_gerar))
        application.add_handler(CommandHandler("publicar", self._cmd_publicar))
        application.add_handler(CommandHandler("listar", self._cmd_listar))
        application.add_handler(CommandHandler("status", self._cmd_status))
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self._handle_text,
            )
        )
        application.add_handler(
            MessageHandler(
                filters.PHOTO | filters.Document.IMAGE,
                self._handle_image,
            )
        )
        application.add_handler(
            MessageHandler(
                ~filters.TEXT & ~filters.PHOTO & ~filters.Document.IMAGE,
                self._handle_unsupported,
            )
        )

        return application

    async def _cmd_start(self, update: Update, _context) -> None:
        await update.message.reply_text(
            "🤖 Olá! Eu sou o bot de automação de artigos.\n\n"
            "📝 Envie textos e anotações que eu salvo como "
            "arquivos .md\n"
            "🖼️ Envie imagens para compor seus artigos\n"
            "⚙️ Use /ajuda para ver todos os comandos"
        )

    async def _cmd_ajuda(self, update: Update, _context) -> None:
        await update.message.reply_text(
            "📋 Comandos disponíveis:\n\n"
            "/start — Boas-vindas\n"
            "/ajuda — Esta mensagem\n"
            "/gerar — Gera artigo com as anotações\n"
            "/listar — Lista anotações salvas\n"
            "/status — Status do conteúdo\n"
            "/publicar <nome> — Publica no Dev.to\n"
            "/publicar <nome> --published — Publicar (visível)\n\n"
            "💬 Envie qualquer texto para salvar como anotação\n"
            "🖼️ Envie imagens para salvar em /source/imagens"
        )

    async def _cmd_gerar(self, update: Update, _context) -> None:
        anotacoes = list(self.source_dir.glob("*.md"))
        if not anotacoes:
            await update.message.reply_text(
                "❌ Nenhuma anotação encontrada em /source.\n"
                "Envie textos para criar anotações primeiro."
            )
            return

        msg = await update.message.reply_text("⏳ Gerando artigo...")

        try:
            process = await asyncio.create_subprocess_exec(
                "uv",
                "run",
                "artigo",
                "generate",
                "--source",
                str(self.source_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=TIMEOUT_GERACAO
            )
        except asyncio.TimeoutError:
            process.kill()
            await msg.edit_text("❌ Geração excedeu o tempo limite (3 min).")
            return
        except FileNotFoundError:
            await msg.edit_text(
                "❌ Comando `artigo` não encontrado. "
                "Execute `uv sync` para instalar as dependências."
            )
            return

        if process.returncode != 0:
            erro = (stderr.decode() or stdout.decode())[:500]
            await msg.edit_text(f"❌ Erro ao gerar artigo:\n`{erro}`")
            return

        output_dir = Path("artigos")
        artigos = sorted(
            output_dir.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not artigos:
            await msg.edit_text(
                "❌ Artigo foi gerado mas não encontrado em /artigos/"
            )
            return

        artigo_path = artigos[0]
        conteudo = artigo_path.read_text(encoding="utf-8")

        if len(conteudo) <= LIMITE_TEXTO_TELEGRAM:
            await msg.edit_text(conteudo)
        else:
            await msg.delete()
            await update.message.reply_document(
                document=artigo_path.open("rb"),
                filename=artigo_path.name,
                caption="📄 Artigo gerado",
            )

    async def _cmd_publicar(  # noqa: PLR0911
        self, update: Update, context
    ) -> None:
        args = context.args
        publicado = False

        if not args:
            output_dir = Path("artigos")
            if not output_dir.exists():
                await update.message.reply_text(
                    "❌ Diretório /artigos não encontrado."
                )
                return
            artigos = sorted(output_dir.glob("*.md"))
            if not artigos:
                await update.message.reply_text(
                    "📂 Nenhum artigo em /artigos/. Use /gerar para criar um."
                )
                return
            linhas = [
                "📂 **Artigos disponíveis:**\n",
                *(f"• `{a.stem}`" for a in artigos),
                "",
                "💡 Uso: `/publicar <nome> [--published]`",
            ]
            await update.message.reply_text("\n".join(linhas))
            return

        args_list = list(args)
        if "--published" in args_list:
            publicado = True
            args_list.remove("--published")

        nome_artigo = args_list[0] if args_list else None
        if not nome_artigo:
            await update.message.reply_text(
                "❌ Informe o nome do artigo.\n"
                "Uso: `/publicar <nome> [--published]`"
            )
            return

        msg = await update.message.reply_text(
            f"⏳ Publicando `{nome_artigo}` no Dev.to..."
        )

        cmd = [
            "uv",
            "run",
            "artigo",
            "publish",
            nome_artigo,
        ]
        if publicado:
            cmd.append("--published")

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=30.0
            )
        except asyncio.TimeoutError:
            process.kill()
            await msg.edit_text("❌ Publicação excedeu o tempo limite (30s).")
            return
        except FileNotFoundError:
            await msg.edit_text("❌ Comando `artigo` não encontrado.")
            return

        if process.returncode != 0:
            erro = (stderr.decode() or stdout.decode())[:500]
            await msg.edit_text(f"❌ Erro ao publicar:\n`{erro}`")
            return

        saida = stdout.decode().strip()
        await msg.edit_text(
            f"✅ Artigo **{nome_artigo}** publicado!\n\n`{saida}`"
        )

    async def _cmd_listar(self, update: Update, _context) -> None:
        anotacoes = sorted(self.source_dir.glob("*.md"))
        if not anotacoes:
            await update.message.reply_text("📂 Nenhuma anotação em /source.")
            return

        linhas = ["📂 **Anotações em /source:**\n"]
        for arq in anotacoes:
            tamanho = len(arq.read_text(encoding="utf-8"))
            linhas.append(f"• `{arq.name}` — {tamanho} chars")

        await update.message.reply_text("\n".join(linhas))

    async def _cmd_status(self, update: Update, _context) -> None:
        qtd_anotacoes = len(list(self.source_dir.glob("*.md")))

        if self.imagens_dir.exists():
            qtd_imagens = len(list(self.imagens_dir.iterdir()))
        else:
            qtd_imagens = 0

        await update.message.reply_text(
            f"📊 **Status do conteúdo**\n\n"
            f"📝 Anotações: {qtd_anotacoes}\n"
            f"🖼️ Imagens: {qtd_imagens}\n"
            f"📂 Diretório: `{self.source_dir}`"
        )

    async def _handle_text(self, update: Update, _context) -> None:
        texto = update.message.text.strip()

        if len(texto) < TAMANHO_MINIMO_ANOTACAO:
            await update.message.reply_text(
                f"❌ Conteúdo muito curto ({len(texto)} caracteres). "
                f"Mínimo: {TAMANHO_MINIMO_ANOTACAO} caracteres."
            )
            logger.info(
                "Texto rejeitado (curto): %d chars de %s",
                len(texto),
                update.effective_user.id,
            )
            return

        nome_arquivo = _gerar_nome_anotacao(update.effective_chat.id)
        caminho = self.source_dir / nome_arquivo

        try:
            caminho.write_text(texto, encoding="utf-8")
            logger.info("Anotação salva: %s (%d chars)", caminho, len(texto))
            await update.message.reply_text(
                f"✅ Anotação salva em `{nome_arquivo}`\n"
                f"📝 {len(texto)} caracteres",
            )
        except OSError as e:
            logger.exception("Erro ao salvar anotação: %s", caminho)
            await update.message.reply_text(f"❌ Erro ao salvar anotação: {e}")

    async def _handle_image(self, update: Update, _context) -> None:
        chat_id = update.effective_chat.id

        if update.message.photo:
            photo = update.message.photo[-1]
            extensao = ".jpg"
            file = await photo.get_file()
        elif update.message.document:
            doc = update.message.document
            extensao = Path(doc.file_name or "").suffix.lower()
            if extensao not in FORMATOS_IMAGEM:
                await update.message.reply_text(
                    f"❌ Formato não suportado: `{extensao}`. "
                    f"Aceitos: jpg, png, gif, webp."
                )
                logger.info(
                    "Imagem rejeitada (formato): %s de %s",
                    extensao,
                    update.effective_user.id,
                )
                return
            file = await doc.get_file()
        else:
            await update.message.reply_text(
                "❌ Tipo de imagem não reconhecido."
            )
            return

        nome_arquivo = _gerar_nome_imagem(chat_id, extensao)
        caminho = self.imagens_dir / nome_arquivo

        try:
            await file.download_to_drive(caminho)
            logger.info("Imagem salva: %s", caminho)
            await update.message.reply_text(
                f"✅ Imagem salva em `{nome_arquivo}`"
            )
        except Exception as e:
            logger.exception("Erro ao salvar imagem: %s", caminho)
            await update.message.reply_text(f"❌ Erro ao salvar imagem: {e}")

    async def _handle_unsupported(self, update: Update, _context) -> None:
        await update.message.reply_text(
            "❌ Apenas textos e imagens são aceitos."
        )

    def start(self) -> None:
        if self._running:
            logger.warning("Bot já está em execução")
            return

        self._garantir_diretorios()
        self.application = self._build_application()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            logger.info(
                "Iniciando bot com token: %s...",
                self.token[:8] + "...",
            )
            self._running = True
            self.application.run_polling()
            self._running = False
            logger.info("Bot parou.")
        except Exception:
            logger.exception("Erro ao iniciar bot")
            self._running = False
        finally:
            loop.close()

    def stop(self) -> None:
        if self.application and self._running:
            logger.info("Parando bot...")
            self.application.stop()
            self._running = False
