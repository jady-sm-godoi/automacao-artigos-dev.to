from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.telegram_bot import (
    TAMANHO_MINIMO_ANOTACAO,
    TelegramBotService,
    _gerar_nome_anotacao,
    _gerar_nome_imagem,
)


@pytest.fixture
def bot(tmp_path):
    return TelegramBotService(token="fake-token", source_dir=tmp_path)


def test_gerar_nome_anotacao():
    nome = _gerar_nome_anotacao(12345)
    assert nome.endswith("-12345.md")
    assert len(nome) > 10


def test_gerar_nome_imagem():
    nome = _gerar_nome_imagem(12345, ".jpg")
    assert nome.endswith("-12345.jpg")
    assert len(nome) > 10


class TestHandleText:
    @pytest.mark.asyncio
    async def test_rejeita_texto_curto(self, bot):
        update = MagicMock()
        update.message.text = "curto"
        update.message.reply_text = AsyncMock()
        update.effective_user.id = 1
        update.effective_chat.id = 1

        await bot._handle_text(update, None)

        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "curto" in args
        assert "100" in args

    @pytest.mark.asyncio
    async def test_salva_texto_valido(self, bot, tmp_path):
        texto = "a" * TAMANHO_MINIMO_ANOTACAO
        update = MagicMock()
        update.message.text = texto
        update.message.reply_text = AsyncMock()
        update.effective_user.id = 1
        update.effective_chat.id = 1

        await bot._handle_text(update, None)

        arquivos = list(tmp_path.glob("*.md"))
        assert len(arquivos) == 1
        conteudo = arquivos[0].read_text(encoding="utf-8")
        assert conteudo == texto
        update.message.reply_text.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_trata_erro_ao_salvar(self, bot, tmp_path):
        texto = "a" * TAMANHO_MINIMO_ANOTACAO
        update = MagicMock()
        update.message.text = texto
        update.message.reply_text = AsyncMock()
        update.effective_user.id = 1
        update.effective_chat.id = 1

        with patch.object(
            Path, "write_text", side_effect=OSError("permissão negada")
        ):
            await bot._handle_text(update, None)

        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "Erro" in args


class TestHandleImage:
    @pytest.mark.asyncio
    async def test_salva_photo_como_jpg(self, bot, tmp_path):
        update = MagicMock()
        update.effective_chat.id = 1
        update.message.photo = [MagicMock()]
        update.message.document = None
        update.message.reply_text = AsyncMock()

        file_mock = AsyncMock()
        file_mock.download_to_drive = AsyncMock()
        update.message.photo[-1].get_file = AsyncMock(return_value=file_mock)

        await bot._handle_image(update, None)

        img_dir = tmp_path / "imagens"
        file_mock.download_to_drive.assert_awaited_once()
        args = file_mock.download_to_drive.call_args[0][0]
        assert str(args).startswith(str(img_dir))
        assert args.suffix == ".jpg"
        update.message.reply_text.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_rejeita_formato_invalido(self, bot):
        update = MagicMock()
        update.effective_chat.id = 1
        update.message.photo = None
        update.effective_user.id = 1

        doc = MagicMock()
        doc.file_name = "imagem.bmp"
        doc.get_file = AsyncMock()
        update.message.document = doc
        update.message.reply_text = AsyncMock()

        await bot._handle_image(update, None)

        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "não suportado" in args

    @pytest.mark.asyncio
    async def test_salva_document_imagem_valido(self, bot, tmp_path):
        update = MagicMock()
        update.effective_chat.id = 1
        update.message.photo = None
        update.message.document = MagicMock()
        update.message.document.file_name = "foto.png"
        update.message.reply_text = AsyncMock()

        file_mock = AsyncMock()
        file_mock.download_to_drive = AsyncMock()
        update.message.document.get_file = AsyncMock(return_value=file_mock)

        await bot._handle_image(update, None)

        img_dir = tmp_path / "imagens"
        file_mock.download_to_drive.assert_awaited_once()
        args = file_mock.download_to_drive.call_args[0][0]
        assert str(args).startswith(str(img_dir))
        assert args.suffix == ".png"


class TestCommands:
    @pytest.mark.asyncio
    async def test_cmd_start(self, bot):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._cmd_start(update, None)
        update.message.reply_text.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_cmd_ajuda(self, bot):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._cmd_ajuda(update, None)
        update.message.reply_text.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_cmd_listar_sem_anotacoes(self, bot):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._cmd_listar(update, None)
        update.message.reply_text.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_cmd_listar_com_anotacoes(self, bot, tmp_path):
        (tmp_path / "nota.md").write_text("conteudo")
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._cmd_listar(update, None)
        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "nota.md" in args

    @pytest.mark.asyncio
    async def test_cmd_status(self, bot, tmp_path):
        (tmp_path / "nota.md").write_text("conteudo")
        (tmp_path / "imagens").mkdir()
        (tmp_path / "imagens" / "foto.jpg").write_bytes(b"x")

        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._cmd_status(update, None)
        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "1" in args

    @pytest.mark.asyncio
    async def test_cmd_gerar_sem_anotacoes(self, bot):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._cmd_gerar(update, None)
        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "Nenhuma anotação" in args

    @pytest.mark.asyncio
    async def test_cmd_publicar_sem_args(self, bot, tmp_path):
        output = tmp_path / "artigos"
        output.mkdir()
        (output / "artigo.md").write_text("# Titulo")
        with patch(
            "src.services.telegram_bot.Path",
            return_value=output,
        ):
            update = MagicMock()
            update.message.reply_text = AsyncMock()
            context = MagicMock()
            context.args = []
            await bot._cmd_publicar(update, context)

        update.message.reply_text.assert_awaited_once()


class TestHandleUnsupported:
    @pytest.mark.asyncio
    async def test_rejeita_tipo_nao_suportado(self, bot):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        await bot._handle_unsupported(update, None)
        update.message.reply_text.assert_awaited_once()
        args = update.message.reply_text.call_args[0][0]
        assert "Apenas textos" in args


class TestServiceLifecycle:
    def test_garantir_diretorios_cria_pastas(self, bot, tmp_path):
        bot._garantir_diretorios()
        assert tmp_path.exists()
        assert (tmp_path / "imagens").exists()

    @patch("src.services.telegram_bot.Application")
    def test_build_application_registra_handlers(self, mock_app, bot):
        app_instance = MagicMock()
        mock_app.builder.return_value.token.return_value.build.return_value = (
            app_instance
        )

        result = bot._build_application()

        assert result == app_instance
        assert app_instance.add_handler.call_count == 9

    def test_stop_nao_falha_quando_parado(self, bot):
        bot.stop()
