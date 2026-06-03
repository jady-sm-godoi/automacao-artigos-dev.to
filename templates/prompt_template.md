# Template de Artigo Medium

## Instruções
Escreva como se estivesse conversando com um amigo. Compartilhe suas experiências e insights com clareza.
Elimine qualquer padrão típico de IA: estruturas previsíveis, conectores repetitivos, travessões inseridos no meio de frases, listas padronizadas, frases genéricas, conclusões escolares, excesso de clareza artificial e finalizações universalizantes.
Evite também o estilo ‘IA poética’: frases harmoniosas demais, lirismo automático ou construções inspiracionais artificiais.
Se precisar criar pausas, NÃO use travessão. Exemplo: em vez de "algo — explicação", prefira "algo: explicação" ou "algo. Explicação".
Use vírgulas ou reestruture a frase para criar pausas de forma natural.
Entregue um texto natural, realista, orgânico e direto, sem polimento literário artificial.
Preserve o conteúdo, mas escreva como um autor humano experiente, com fluidez natural e leve imperfeição.

- "O artigo deve ter entre 1500 e 3000 palavras"
- "Aproveite todo o conteúdo das anotações: não faça um resumo, expanda cada ideia com exemplos, contexto e reflexão"
- "Cada tópico das anotações deve virar pelo menos um parágrafo próprio, com desenvolvimento completo"

Transforme as anotações abaixo em um artigo envolvente que reflita sua paixão pelo tópico.

## Estrutura do Artigo

1. **Título Chamativo**: crie um título que faça os leitores quererem
   saber mais. NÃO use `#` (H1) no corpo. O frontmatter já define o
   H1 da página. Use `##` (H2) para seções e `###` (H3) para
   subseções.
2. **Lead / Introdução**: comece introduzindo o tema geral de forma amigável e descontraída, mas sem fazer perguntas nessa seção.
3. **Corpo**: utilize subtítulos H2 e H3. Varie o comprimento das
   frases e evite jargão; use exemplos e citações para enriquecer a
   narrativa. Utilize os exemplos indicados nas anotações para ilustrar os conceitos e idéias.
4. **Conclusão**: recapitule as ideias principais e convide os
   leitores a refletir ou compartilhar suas próprias histórias.
   Desafie-os a agir ou pensar sobre o tema.

## Estilo Medium

- Tom: Acessível e amigável, como uma conversa entre amigos.
- Parágrafos: Frases curtas e diretas funcionam bem; evite jargão
  desnecessário.
- Utilize listas e negrito para clareza.
- **Imagens reais**: analise as imagens listadas na seção "Imagens
  Disponíveis" e insira cada uma no contexto mais relevante do
  artigo. Use caminho relativo:
  `![descrição da imagem](imagens/nome-do-arquivo.png)`.
  Máximo **5 imagens**. Formatos: PNG, JPG, JPEG, GIF, WebP.
- **Imagens geradas por IA**: se o tema abordar um conceito,
  metáfora ou explicação que se beneficiaria de uma ilustração
  visual (diagrama, esquema, comparação visual), sugira um prompt
  para geração de imagem por IA no local mais adequado do texto.
  Formato obrigatório:
  ```markdown
  > 🎨 **Imagem gerada por IA**
  > Prompt: `descrição detalhada em inglês para geradores como nonobanana, DALL-E, Midjourney`
  ```
  Máximo **3 sugestões** por artigo. Se já houver imagens reais
  disponíveis, prefira usá-las antes de sugerir imagens geradas.

## Formato de Saída

IMPORTANTE: O arquivo DEVE começar com frontmatter YAML CRU (sem
nenhum bloco de código ao redor). NÃO use ```yaml nem ``` para
envolver o frontmatter.

### Exemplo Correto (frontmatter CRU, sem code block):

---
title: "Título do Artigo"
description: "Resumo curto para exibição na listagem do Dev.to"
tags: tag1, tag2, tag3
---

- **title**: mesmo título do H1
- **description**: 1-2 frases resumindo o artigo
- **tags**: máx 4 tags, separadas por vírgula, extraídas das
  anotações ou do contexto

## Título

{{titulo}}

## Tags

{{tags}}

## Imagens Disponíveis

{{imagens}}

## Conteúdo para Transformar

{{conteudo}}
