# Feature Specification: Artigo Blog Generator

**Feature Branch**: `001-artigo-blog-generator`

**Created**: 2026-04-29

**Status**: Draft

**Input**: Criação de um aplicativo Python para gerar artigos estilo Medium a partir de anotações markdown

## User Scenarios & Testing

### User Story 1 - Geração de Artigo (Priority: P1)

Como escritor/produtor de conteúdo, quero fornecer anotações em markdown na pasta `/source` e receber um artigo formatado no estilo Medium na pasta `/artigos`, para que eu possa rapidamente transformar notas brutas em artigos profissionais.

**Why this priority**: Funcionalidade central do sistema - todo o valor do projeto depende disso

**Independent Test**: Pode ser testado fornecendo arquivos markdown e verificando a geração do artigo

**Acceptance Scenarios**:

1. **Given** a pasta `/source` contém arquivos `.md` com anotações, **When** o usuário executa o comando de geração, **Then** um artigo formatado em estilo Medium é criado na pasta `/artigos`

2. **Given** a pasta `/source` contém subpastas organizando anotações por tema, **When** o usuário executa o comando de geração, **Then** o sistema processa todos os arquivos e gera artigo integrado

3. **Given** a pasta `/source` está vazia, **When** o usuário executa o comando de geração, **Then** o sistema informa que não há conteúdo para processar

4. **Given** o arquivo de anotações tem metadados (título, tags, data), **When** o artigo é gerado, **Then** essas informações são incorporadas no artigo final

---

### User Story 2 - Interface de Linha de Comando (Priority: P2)

Como usuário, quero executar a geração de artigos via CLI, para que eu possa integrar o processo em meus fluxos de trabalho existentes.

**Why this priority**: Essencial para usabilidade e automação

**Independent Test**: Pode ser testado executando comandos CLI e verificando saídas

**Acceptance Scenarios**:

1. **Given** o aplicativo está instalado, **When** o usuário executa `python -m main --help`, **Then** a ajuda com comandos disponíveis é exibida

2. **Given** o usuário executa o comando de geração, **When** o processo inicia, **Then** feedback de progresso é exibido no terminal

3. **Given** o usuário executa o comando sem argumentos, **When** o processo inicia, **Then** o sistema usa caminhos padrão (`/source` e `/artigos`)

---

### User Story 3 - Configuração de Estilo Medium (Priority: P3)

Como usuário, quero que o artigo gerado siga o estilo visual do Medium, para que o resultado final seja profissional e legível.

**Why this priority**: Diferenciador de valor - garante qualidade visual do output

**Independent Test**: Pode ser testado gerando artigo e verificando estrutura/formatação

**Acceptance Scenarios**:

1. **Given** anotações com formatação básica (listas, títulos, negrito), **When** o artigo é gerado, **Then** a formatação é preservada seguindo estilo Medium

2. **Given** anotações contêm código ou blocos de citação, **When** o artigo é gerado, **Then** esses elementos são formatados corretamente para o estilo Medium

---

### Edge Cases

- Pasta `/source` não existe: criar automaticamente ou informar erro?
- Pasta `/artigos` não existe: criar automaticamente ou informar erro?
- Arquivo markdown vazio: ignorar ou reportar?
- Anotações muito curtas (menos de 100 caracteres): gerar artigo mínimo ou informar?
- Arquivos não-markdown na pasta `/source`: ignorar silenciosamente ou reportar warning?
- Nome do arquivo de output: usar título do artigo ou timestamp?
- Sobrescrever artigo existente ou criar nova versão?

## Requirements

### Functional Requirements

- **FR-001**: Sistema deve processar todos os arquivos `.md` da pasta `/source`
- **FR-002**: Sistema deve gerar artigo final em formato markdown na pasta `/artigos`
- **FR-003**: Sistema deve usar Agno para transformar anotações em artigo estilo Medium
- **FR-004**: Sistema deve manter estrutura e formatação original das anotações quando relevante
- **FR-005**: Sistema deve fornecer CLI com comando principal para geração
- **FR-006**: Sistema deve exibir mensagens de progresso durante geração
- **FR-007**: Sistema deve criar diretórios `/source` e `/artigos` se não existirem
- **FR-008**: Sistema deve ler metadados frontmatter dos arquivos markdown se presentes

### Key Entities

- **Anotacao**: Arquivo markdown de entrada com conteúdo do usuário
- **Artigo**: Arquivo markdown de saída formatado em estilo Medium
- **Configuracao**: Parâmetros de geração (pastas, estilo, etc.)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Usuário consegue transformar anotações em artigo em menos de 2 minutos
- **SC-002**: Artigo gerado mantém formatação markdown legível
- **SC-003**: Sistema processa múltiplos arquivos de anotações em uma única execução
- **SC-004**: CLI responde ao comando `--help` em menos de 1 segundo

## Assumptions

- Usuário tem Python 3.11+ instalado
- API key para o modelo de IA está configurada via variável de ambiente
- Pasta `/source` contém anotações autocontidas (sem dependências externas)
- Artigo final será lido por humanos, não processado automaticamente