# Feature Specification: Telegram Bot Integration

**Feature Branch**: `003-telegram-bot-integration`

**Created**: 2026-05-22

**Status**: Draft

**Input**: Integração com Telegram para enviar textos, anotações e imagens ao bot,
que salvam em /source e /source/imagens, com comando para gerar artigo e
receber o resultado no chat

## User Scenarios & Testing

### User Story 1 - Envio de Texto e Anotações (Priority: P1)

Como usuário, quero enviar textos e anotações para o bot do Telegram, para que
sejam salvos automaticamente como arquivos .md na pasta /source, servindo de
insumo para geração de artigos.

**Why this priority**: É a base da integração — sem conteúdo enviado, não há
artigo a gerar. Habilita o fluxo completo de "escrever no Telegram → salvar
como anotação".

**Independent Test**: Pode ser testado enviando mensagens de texto ao bot e
verificando se os arquivos .md correspondentes aparecem em /source.

**Acceptance Scenarios**:

1. **Given** o bot está ativo, **When** o usuário envia uma mensagem de texto,
   **Then** o bot salva o conteúdo em um arquivo .md em /source e confirma
   o salvamento

2. **Given** o usuário envia múltiplas mensagens de texto, **When** cada
   mensagem é processada, **Then** cada mensagem gera um arquivo .md
   independente com timestamp no nome

3. **Given** o usuário envia uma mensagem com menos de 100 caracteres,
   **When** o bot processa, **Then** o bot informa que o conteúdo é muito
   curto e não salva

4. **Given** o usuário envia uma mensagem de texto com formatação (markdown),
   **When** o bot processa, **Then** a formatação é preservada no arquivo .md

---

### User Story 2 - Envio de Imagens (Priority: P1)

Como usuário, quero enviar imagens para o bot do Telegram, para que sejam
salvas na pasta /source/imagens e possam ser referenciadas nos artigos
gerados.

**Why this priority**: Imagens são parte essencial de artricos visuais no
estilo Medium. Permite enriquecer o artigo com figuras, diagramas e
capturas de tela.

**Independent Test**: Pode ser testado enviando imagens ao bot e verificando
se os arquivos aparecem em /source/imagens.

**Acceptance Scenarios**:

1. **Given** o bot está ativo, **When** o usuário envia uma imagem,
   **Then** o bot salva a imagem em /source/imagens/ com nome baseado
   em timestamp e confirma o salvamento

2. **Given** o usuário envia um arquivo que não é imagem, **When** o bot
   processa, **Then** o bot informa que apenas imagens são aceitas e não
   salva o arquivo

3. **Given** a pasta /source/imagens não existe, **When** o bot recebe uma
   imagem, **Then** a pasta é criada automaticamente antes de salvar

4. **Given** o usuário envia múltiplas imagens, **When** cada imagem é
   processada, **Then** cada imagem é salva com nome único

---

### User Story 3 - Geração de Artigo via Bot (Priority: P1)

Como usuário, quero enviar o comando /gerar para o bot do Telegram, para que
o sistema execute "artigo generate" e me retorne o artigo gerado diretamente
no chat para avaliação.

**Why this priority**: É o fluxo principal de valor — o usuário envia conteúdo
e recebe o artigo sem sair do Telegram.

**Independent Test**: Pode ser testado enviando /gerar após enviar anotações
e verificando se o artigo gerado é retornado no chat.

**Acceptance Scenarios**:

1. **Given** existem anotações em /source, **When** o usuário envia /gerar,
   **Then** o bot executa "artigo generate" e envia o artigo gerado como
   mensagem de texto no chat

2. **Given** não existem anotações em /source, **When** o usuário envia
   /gerar, **Then** o bot informa que não há conteúdo para gerar artigo

3. **Given** o artigo gerado excede o limite de caracteres do Telegram,
   **When** o bot tenta enviar, **Then** o bot envia o artigo como arquivo
   .md anexado

4. **Given** a geração falha (ex: API key ausente), **When** o bot processa,
   **Then** o bot informa o erro ao usuário

---

### User Story 4 - Gerenciamento de Conteúdo (Priority: P2)

Como usuário, quero consultar e gerenciar o conteúdo enviado via bot, para
que eu possa saber o que já foi salvo e organizar meu fluxo de trabalho.

**Why this priority**: Aumenta a usabilidade sem ser crítico para o fluxo
principal de envio e geração.

**Independent Test**: Pode ser testado enviando comandos de gerenciamento
e verificando as respostas do bot.

**Acceptance Scenarios**:

1. **Given** o bot está ativo, **When** o usuário envia /listar, **Then**
   o bot lista os arquivos .md disponíveis em /source

2. **Given** o bot está ativo, **When** o usuário envia /status, **Then**
   o bot informa quantas anotações e imagens existem em /source

3. **Given** o bot está ativo, **When** o usuário envia /ajuda, **Then**
   o bot exibe uma mensagem com todos os comandos disponíveis

---

### User Story 5 - Publicação via Bot (Priority: P3)

Como usuário, quero publicar artigos no Dev.to diretamente pelo bot do
Telegram, para que eu complete o fluxo sem sair do mensageiro.

**Why this priority**: Complementa a geração mas depende do artigo já ter
sido gerado e da chave Dev.to estar configurada.

**Independent Test**: Pode ser testado com artigo existente em /artigos
e chave Dev.to configurada, verificando a resposta da API.

**Acceptance Scenarios**:

1. **Given** um artigo existe em /artigos, **When** o usuário envia
   /publicar nome-do-artigo, **Then** o artigo é enviado ao Dev.to como
   rascunho e o bot retorna a URL

2. **Given** o artigo não existe, **When** o usuário envia /publicar,
   **Then** o bot lista os artigos disponíveis

3. **Given** o usuário envia /publicar nome-do-artigo --published,
   **When** o comando é processado, **Then** o artigo é publicado
   visivelmente no Dev.to

---

### Edge Cases

- **Mensagem muito curta (< 100 caracteres)**: bot informa e não salva
- **Arquivo não suportado**: bot rejeita e informa tipos aceitos (texto,
  imagem)
- **Imagem em formato não suportado**: bot informa formatos aceitos
  (jpg, png, gif, webp)
- **Múltiplas mensagens em sequência**: cada uma vira um arquivo .md
  independente
- **Comando /gerar sem conteúdo**: bot informa que /source está vazio
- **Geração falha**: bot captura exceção e exibe erro amigável
- **Telegram API offline**: bot tenta reconectar em caso de falha de
  conexão
- **Token não configurado**: bot informa erro ao iniciar se TELEGRAM_BOT_TOKEN
  não estiver definido
- **Timeout de geração (> 2 min)**: bot informa que a geração levou mais
  tempo que o esperado e sugere tentar novamente
- **Limite de taxa do Telegram**: bot respeita limites de rate limiting
  da API do Telegram

## Requirements

### Functional Requirements

- **FR-001**: Bot DEVE salvar mensagens de texto como arquivos .md em /source
- **FR-002**: Bot DEVE salvar imagens enviadas em /source/imagens
- **FR-003**: Bot DEVE criar pastas /source e /source/imagens se não existirem
- **FR-004**: Bot DEVE responder ao comando /gerar executando "artigo generate"
- **FR-005**: Bot DEVE retornar o artigo gerado como mensagem no chat
- **FR-006**: Bot DEVE lidar com artigos longos enviando como arquivo .md
  anexado
- **FR-007**: Bot DEVE validar tamanho mínimo de 100 caracteres para anotações
- **FR-008**: Bot DEVE validar formato de imagem (jpg, png, gif, webp)
- **FR-009**: Bot DEVE responder ao comando /start com mensagem de boas-vindas
  e instruções
- **FR-010**: Bot DEVE responder ao comando /ajuda com lista de comandos
- **FR-011**: Bot DEVE responder ao comando /listar com arquivos em /source
- **FR-012**: Bot DEVE responder ao comando /status com contagem de itens
- **FR-013**: Bot DEVE responder ao comando /publicar publicando no Dev.to
- **FR-014**: Bot DEVE ser iniciado via CLI com comando dedicado
- **FR-015**: Bot DEVE usar token via variável de ambiente TELEGRAM_BOT_TOKEN
- **FR-016**: Bot DEVE tratar erros gracefulmente com mensagens amigáveis
- **FR-017**: Cada mensagem de texto DEVE gerar arquivo .md com nome único
  (timestamp)

### Key Entities

- **Mensagem Telegram**: Texto, imagem ou comando enviado pelo usuário via
  Telegram. Contém remetente, timestamp, tipo de conteúdo e dados.
- **Sessao Usuario**: Contexto de conversa do usuário no Telegram.
  Identificada pelo chat_id do Telegram.
- **Anotacao Telegram**: Arquivo .md gerado a partir de uma mensagem de texto.
  Salvo em /source com nome baseado em timestamp.
- **Imagem Telegram**: Arquivo de imagem baixado do Telegram. Salvo em
  /source/imagens com nome baseado em timestamp.
- **Comando Telegram**: Mensagem iniciada com / que dispara uma ação no bot
  (gerar, publicar, listar, status, ajuda).

## Success Criteria

### Measurable Outcomes

- **SC-001**: Mensagem de texto enviada ao bot é salva como .md em /source
  em menos de 5 segundos
- **SC-002**: Imagem enviada ao bot é salva em /source/imagens em menos de
  10 segundos (dependendo do tamanho)
- **SC-003**: Comando /gerar retorna o artigo gerado em menos de 3 minutos
- **SC-004**: Bot responde a comandos de texto (/start, /ajuda, /listar) em
  menos de 3 segundos
- **SC-005**: Usuário consegue completar o fluxo completo (enviar anotações
  → gerar artigo → receber resultado) sem sair do Telegram
- **SC-006**: 100% dos erros (token ausente, API falha, conteúdo vazio) são
  reportados ao usuário com mensagem compreensível

## Assumptions

- Usuário tem Telegram instalado e conta ativa
- Bot será implementado usando a API Bot do Telegram via polling (long
  polling)
- Token do bot configurado via variável de ambiente TELEGRAM_BOT_TOKEN
- Cada mensagem de texto vira um arquivo .md independente (não acumula)
- Bot é público (qualquer usuário do Telegram pode interagir)
- Sistema "artigo generate" já está funcional (dependência deste projeto)
- Imagens são salvas com nomes únicos baseados em timestamp para evitar
  colisões
- O artigo gerado será enviado como texto se tiver até 4000 caracteres, ou
  como arquivo .md se for maior
