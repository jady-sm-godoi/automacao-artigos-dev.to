# Quickstart: Telegram Bot

## 1. Criar o Bot no Telegram

1. Abra o Telegram e procure por [@BotFather](https://t.me/BotFather)
2. Envie `/newbot` e siga as instruções
3. Escolha um nome (ex: "Meu Artigo Bot") e um username (ex: `meu_artigo_bot`)
4. O BotFather fornecerá um **token**. Guarde-o.

## 2. Configurar Token

Adicione ao `.env` na raiz do projeto:

```bash
TELEGRAM_BOT_TOKEN="seu-token-aqui"
```

## 3. Iniciar o Bot

```bash
artigo bot
```

O bot iniciará em modo polling. Você verá:
```
Bot iniciado! 🤖
```

## 4. Usar no Telegram

Abra o chat com seu bot e experimente:

```
/start          → Boas-vindas
/ajuda          → Lista de comandos
Enviar texto    → Salva como anotação .md
Enviar imagem   → Salva em /source/imagens/
/gerar          → Gera artigo e envia de volta
/listar         → Lista anotações
/publicar nome  → Publica no Dev.to (rascunho)
/status         → Status do conteúdo em /source
```

## 5. Testes

```bash
# Unitários
uv run pytest tests/unit/test_telegram_bot.py -v

# Integração
uv run pytest tests/integration/test_cli.py -v
```
