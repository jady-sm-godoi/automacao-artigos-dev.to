# Data Model: Telegram Bot Integration

## Entities

### TelegramMessage

| Field | Type | Description |
|-------|------|-------------|
| message_id | int | ID da mensagem no Telegram |
| chat_id | int | ID do chat/usuário |
| user_id | int | ID do remetente |
| text | str \| None | Texto da mensagem (se for texto) |
| content_type | enum | text, image, command |
| command | str \| None | Nome do comando (se /command) |
| file_id | str \| None | Telegram file_id (se imagem) |
| caption | str \| None | Legenda da imagem |
| timestamp | datetime | Momento do recebimento |

### AnotacaoTelegram

| Field | Type | Description |
|-------|------|-------------|
| filename | str | Nome do arquivo .md gerado |
| content | str | Conteúdo da mensagem |
| source_message_id | int | message_id de origem |
| chat_id | int | Chat de origem |
| created_at | datetime | Timestamp de criação |
| filepath | str | Caminho completo em /source |

### ImagemTelegram

| Field | Type | Description |
|-------|------|-------------|
| filename | str | Nome do arquivo de imagem |
| extension | str | Extensão (jpg, png, gif, webp) |
| source_message_id | int | message_id de origem |
| chat_id | int | Chat de origem |
| filepath | str | Caminho completo em /source/imagens/ |
| size_bytes | int | Tamanho do arquivo |

## Validation Rules

| Rule | Description | FR Ref |
|------|-------------|--------|
| Min text length | Texto < 100 chars é rejeitado | FR-007 |
| Image format | Apenas jpg, png, gif, webp | FR-008 |
| Filename unique | Timestamp-based para evitar colisão | FR-017 |
| Content source | /source e /source/imagens criados se ausentes | FR-003 |

## State Transitions

Mensagem recebida → [valida tipo] → texto: salva .md em /source
                               → imagem: salva em /source/imagens/
                               → comando: executa handler
                               → inválido: responde com erro
