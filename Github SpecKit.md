---
title: "Github speckit"
tags: ["SDD", "desenvolvimento", "AI"]
---

## Instalação

Para instala rodamos o seguinte:

```sh
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Vamos até a pasta do projeto que queremos o `SpecKit` e rodamos

```sh
specify init . --integration opencode
```

Ele vai criar uma pasta `.specify` e uma pasta `.opencode` na raiz do projeto.  Podemos colocar a pasta `.opencode` no `.gitignore`, mas a pasta `.specify` precisa subir para o github. 

---
## Passo 1: `/speckit.constitution` 

Padrão de código...  Digite no prompt do `opencode`, algo do tipo:

```sh
/speckit.constitution Este projeto segue [suas regras aqui, ex: "princípios SOLID", "testes obrigatórios", "clean architecture"]
```

---
## Passo 2: `/speckit.specify 

É usado para **descrever o que você quer construir** (features novas), e não para analisar código existente.  Para documentar o que seu projeto já faz, você precisa **descrever manualmente** no comando:

```sh
/speckit.specify Meu projeto já existente faz X, Y, Z. Ele tem as seguintes funcionalidades: [liste aqui o que o sistema atual faz]. Quero documentar isso como especificação.
```

---
## Passo 3: `/speckit.clarify 

O comando `/speckit.clarify` é típico do fluxo do **SpecKit** (usado dentro do **OpenCode** ou ferramentas similares de engenharia com IA).

### 💡 O que ele faz

Ele serve para **refinar um pedido (prompt)** antes da execução.

Na prática, quando você usa:

```sh
/speckit.clarify
```

o sistema:

- Analisa o que você já escreveu
- Identifica ambiguidades ou lacunas
- Faz perguntas de esclarecimento (ou sugere melhorias)
- Ajuda a transformar seu pedido em algo mais específico e bem definido
## ⚠️ Importante: O Spec Kit foi feito para greenfield

O GitHub Spec Kit foi projetado primordialmente para **greenfield development** (projetos novos do zero). Ele não tem um comando nativo que analisa código existente e gera specs automaticamente.

Existe uma issue aberta no repositório oficial (#438) pedindo justamente essa funcionalidade de "reverse engineering" para projetos legados[](https://github.com/github/spec-kit/issues/438). Até lá, você tem duas opções:

| Opção                                 | Como fazer                                                                                                                                                                                                                                     |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manual** (recomendado por enquanto) | Você mesmo descreve as funcionalidades existentes no `/speckit.specify`                                                                                                                                                                        |
| **Usar alternativas**                 | Ferramentas como `owflow` (com `/flow-init`) ou `opencode-enhancer-plugin` que oferecem análise automática do código base[](https://www.npmjs.com/package/opencode-enhancer-plugin?activeTab=versions)[](https://codeberg.org/palucdev/owflow) |

---
## Passo 4: `/speckit.plan 

O comando **`/speckit.plan`** faz parte do fluxo do SpecKit (usado no OpenCode) e serve basicamente para **transformar uma ideia ou especificação em um plano estruturado de implementação**.

Em outras palavras: ele pega o que você quer fazer e organiza em passos claros antes de sair codando.

### 🧠 O que o `/speckit.plan` faz

Quando você roda:

```
/speckit.plan
```

Ele normalmente:

- 📌 Analisa o contexto atual (prompt + arquivos, se houver)
- 🧩 Quebra o problema em partes menores
- 🛠️ Define etapas de implementação
- 📁 Pode sugerir estrutura de arquivos
- 🔄 Organiza dependências entre tarefas

### ⚠️ Quando usar (e quando não usar)

Use `/speckit.plan` quando:

- A tarefa é **complexa**
- Você quer **organização antes de codar**
- Está começando uma feature nova

Evite quando:

- É algo simples (tipo “criar uma função pequena”)
- Você já sabe exatamente o que vai fazer

---
## Passo 5: `/speckit.tasks 

O comando **`/speckit.tasks`** faz parte do fluxo do **Speckit**, que organiza desenvolvimento em etapas mais estruturadas (tipo: ideia → clarificação → implementação).

### 🧠 O que ele faz

O **`/speckit.tasks`** pega uma especificação (gerada normalmente pelo `/speckit.clarify`) e transforma isso em uma **lista de tarefas executáveis**.

Ou seja:

> Ele quebra o problema em passos práticos que você pode codar.

---
## Passo 6: `/speckit.implement 

O comando `/speckit.implement` faz parte do fluxo do **SpecKit** (usado no OpenCode) e é basicamente a etapa onde **o plano vira código**.

Vamos direto ao ponto:

---

## 🧠 O que ele faz

O `/speckit.implement` pega tudo que foi definido antes (principalmente no `/speckit.spec` e possivelmente refinado no `/speckit.clarify`) e:

- Gera **código real**
- Cria/edita arquivos do projeto
- Implementa funções, classes, endpoints, etc.
- Segue o plano estruturado que foi definido

Ou seja, é a fase de **execução automática da especificação**.

## 🧩 Como ele se encaixa no fluxo

O fluxo típico do SpecKit é:

1. **`/speckit.spec`**  
    → você descreve o que quer (ex: “criar API de usuários com Django”)
2. **`/speckit.clarify`** _(opcional)_  
    → o agente faz perguntas pra refinar requisitos
3. **`/speckit.plan`** _(às vezes implícito)_  
    → estrutura como será feito (arquivos, arquitetura, etapas)
4. **`/speckit.implement`**  
    → **gera o código de verdade baseado no plano**

---

## ⚙️ O que ele realmente produz

Dependendo do contexto do seu projeto, ele pode:

- Criar arquivos (`models.py`, `views.py`, etc.)
- Alterar código existente
- Adicionar testes
- Gerar migrations (em projetos Django, por exemplo)
- Integrar com libs que você já usa

---

## ⚠️ Importante (pegadinha comum)

Ele **não “pensa do zero”** — ele depende muito do que veio antes.

Se o `/speckit.spec` estiver vago, o resultado do `/speckit.implement` também vai ser.

👉 Exemplo ruim:

> “Criar sistema de usuários”

👉 Exemplo bom:

> “Criar API REST de usuários com Django Ninja, com autenticação JWT, endpoints de CRUD e validação de email”

---

## 🧠 Dica prática (bem útil)

Se você quiser mais controle, pode usar ele de forma incremental:

- Rodar `/speckit.spec` só pra uma parte pequena
- Refinar com `/speckit.clarify`
- E só então rodar `/speckit.implement`

Isso evita que ele saia criando um monte de coisa fora do que você queria.

---

## 🧪 Sobre sua outra dúvida (ligando com essa)

> “tem como rodar o speckit.implement só na primeira fase?”

Depende da ferramenta, mas normalmente:

- Não existe “fase 1” dentro do `implement`
- Ele sempre tenta implementar **tudo que está no plano atual**

👉 Workaround:  
Você controla isso **limitando o escopo no spec**, tipo:

> “implementar apenas os models e serializers, sem views ainda”

