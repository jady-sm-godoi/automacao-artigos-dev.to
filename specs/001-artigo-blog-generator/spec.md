# Feature Specification: Artigo Blog Generator

**Feature Branch**: `001-artigo-blog-generator`

**Created**: 2026-04-29

**Last Updated**: 2026-05-20

**Status**: Implemented

**Input**: Criação de um aplicativo Python para gerar artigos estilo Medium a
partir de anotações markdown e publicar no Dev.to

## Clarifications

### Session 2026-04-29

- Q: Nome do arquivo de artigo → A: Usar título do artigo gerado
  (ex: titulo-do-artigo.md)
- Q: Modelo de LLM → A: GPT-4o (OpenAI) - versátil, boa qualidade
- Q: Estrutura de saída do artigo → A: Markdown formatado (portável,
  conversível para HTML depois)
- Q: Prompt do Agente → A: Prompt configurável via arquivo de template
- Q: Interface CLI → A: `artigo generate` (subcomando explícito)

### Session 2026-05-20

- Q: Método de autenticação Dev.to → A: API key via header `api-key`
- Q: Publicação padrão → A: Rascunho (draft), opção `--published` para
  publicado
- Q: Formato do artigo → A: Markdown com frontmatter YAML (title,
  description, tags)

## User Scenarios & Testing

### User Story 1 - Geração de Artigo (Priority: P1)

Como escritor/produtor de conteúdo, quero fornecer anotações em markdown na
pasta `/source` e receber um artigo formatado no estilo Medium na pasta
`/artigos`, para que eu possa rapidamente transformar notas brutas em
artigos profissionais.

**Independent Test**: Pode ser testado fornecendo arquivos markdown e
verificando a geração do artigo

**Acceptance Scenarios**:

1. **Given** a pasta `/source` contém arquivos `.md` com anotações,
   **When** o usuário executa o comando de geração, **Then** um artigo
   formatado em estilo Medium é criado na pasta `/artigos`

2. **Given** a pasta `/source` contém subpastas organizando anotações por
   tema, **When** o usuário executa o comando de geração, **Then** o sistema
   processa todos os arquivos e gera artigo integrado

3. **Given** a pasta `/source` está vazia, **When** o usuário executa o
   comando de geração, **Then** o sistema informa que não há conteúdo para
   processar

4. **Given** o arquivo de anotações tem metadados (título, tags, data),
   **When** o artigo é gerado, **Then** essas informações são incorporadas
   no artigo final

---

### User Story 2 - Interface de Linha de Comando (Priority: P2)

Como usuário, quero executar a geração de artigos via CLI, para que eu
possa integrar o processo em meus fluxos de trabalho existentes.

**Independent Test**: Pode ser testado executando comandos CLI e verificando
saídas

**Acceptance Scenarios**:

1. **Given** o aplicativo está instalado, **When** o usuário executa
   `artigo generate --help`, **Then** a ajuda com comandos disponíveis é
   exibida

2. **Given** o usuário executa o comando de geração, **When** o processo
   inicia, **Then** feedback de progresso é exibido no terminal

3. **Given** o usuário executa o comando sem argumentos, **When** o
   processo inicia, **Then** o sistema usa caminhos padrão (`/source` e
   `/artigos`)

---

### User Story 3 - Configuração de Estilo Medium (Priority: P3)

Como usuário, quero que o artigo gerado siga o estilo visual do Medium,
para que o resultado final seja profissional e legível.

**Independent Test**: Pode ser testado gerando artigo e verificando
estrutura/formatação

**Acceptance Scenarios**:

1. **Given** anotações com formatação básica (listas, títulos, negrito),
   **When** o artigo é gerado, **Then** a formatação é preservada seguindo
   estilo Medium

2. **Given** anotações contêm código ou blocos de citação, **When** o
   artigo é gerado, **Then** esses elementos são formatados corretamente
   para o estilo Medium

---

### User Story 4 - Publicação no Dev.to (Priority: P2)

Como produtor de conteúdo, quero publicar artigos da pasta `/artigos` no
Dev.to via CLI, para que eu possa compartilhar meus artigos com a
comunidade sem sair do terminal.

**Independent Test**: Pode ser testado com chave de API Dev.to e
verificando o artigo publicado no dashboard

**Acceptance Scenarios**:

1. **Given** um artigo existe em `/artigos`, **When** o usuário executa
   `artigo publish <nome>`, **Then** o artigo é enviado ao Dev.to como
   rascunho

2. **Given** o usuário passa a flag `--published`, **When** o artigo é
   publicado, **Then** o artigo fica visível publicamente no Dev.to

3. **Given** o nome do artigo não existe, **When** o usuário tenta
   publicar, **Then** o sistema lista os artigos disponíveis

4. **Given** a chave de API não está configurada, **When** o usuário
   tenta publicar, **Then** o sistema informa o erro

---

### User Story 5 - Frontmatter no Artigo Gerado (Priority: P3)

Como usuário do Dev.to, quero que os artigos gerados incluam frontmatter
YAML com metadados (title, description, tags), para que a plataforma
possa exibir corretamente o artigo.

**Independent Test**: Pode ser verificado no arquivo gerado e na resposta
da API do Dev.to

**Acceptance Scenarios**:

1. **Given** o template inclui instruções de frontmatter, **When** o
   artigo é gerado, **Then** o markdown começa com bloco
   `---\ntitle:\ndescription:\ntags:\n---`

2. **Given** o artigo tem frontmatter, **When** é publicado no Dev.to,
   **Then** os campos title, description e tags são extraídos e enviados
   explicitamente na requisição

---

### Edge Cases

- Pasta `/source` não existe: criar automaticamente e informar erro
- Pasta `/artigos` não existe: criar automaticamente
- Arquivo markdown vazio: ignorar silenciosamente
- Anotações muito curtas (menos de 100 caracteres): gerar artigo mínimo
  ou informar
- Arquivos não-markdown na pasta `/source`: ignorar silenciosamente
  (warning em log)
- **Nome do arquivo de output**: usar título do artigo gerado
  (ex: `titulo-do-artigo.md`)
- **Sobrescrever**: criar nova versão incrementando counter se existir
- **Dev.to sem chave**: erro claro pedindo configuração
- **Dev.to 401**: chave inválida
- **Dev.to 422**: erro de validação (mostrar msg da API)
- **Dev.to 429**: rate limit excedido

## Requirements

### Functional Requirements

- **FR-001**: Sistema deve processar todos os arquivos `.md` da pasta
  `/source`
- **FR-002**: Sistema deve gerar artigo final em formato markdown na pasta
  `/artigos`
- **FR-003**: Sistema deve usar Agno para transformar anotações em artigo
  estilo Medium
- **FR-004**: Sistema deve manter estrutura e formatação original das
  anotações quando relevante
- **FR-005**: Sistema deve fornecer CLI com comando principal para geração
- **FR-006**: Sistema deve exibir mensagens de progresso durante geração
- **FR-007**: Sistema deve criar diretórios `/source` e `/artigos` se não
  existirem
- **FR-008**: Sistema deve ler metadados frontmatter dos arquivos markdown
  se presentes
- **FR-009**: Sistema deve publicar artigos no Dev.to via API
- **FR-010**: Sistema deve extrair frontmatter (title, description, tags)
  do artigo e enviar como campos explícitos na API
- **FR-011**: Sistema deve suportar publicação como rascunho ou publicado

### Key Entities

- **Anotacao**: Arquivo markdown de entrada com conteúdo do usuário
  (pasta `/source`)
- **Artigo**: Arquivo markdown de saída formatado em estilo Medium
  (pasta `/artigos`)
- **Template**: Arquivo de prompt configurável para o agente Agno
- **Configuracao**: Parâmetros de geração (pastas, modelo, etc.)
- **Publicador**: Serviço que gerencia comunicação com API do Dev.to

## Success Criteria

### Measurable Outcomes

- **SC-001**: Usuário consegue transformar anotações em artigo em menos de
  2 minutos
- **SC-002**: Artigo gerado mantém formatação markdown legível
- **SC-003**: Sistema processa múltiplos arquivos de anotações em uma
  única execução
- **SC-004**: CLI responde ao comando `--help` em menos de 1 segundo
- **SC-005**: Artigo é publicado no Dev.to em menos de 5 segundos

## Assumptions

- Usuário tem Python 3.11+ instalado
- API key da OpenAI (GPT-4o) está configurada via variável de ambiente
- API key do Dev.to está configurada via variável de ambiente
  (`DEVTO_API_KEY`)
- Pasta `/source` contém anotações autocontidas (sem dependências
  externas)
- Artigo final será lido por humanos, não processado automaticamente
