# Template de Artigo Medium

## Instruções

Escreva como se estivesse conversando com um amigo. Compartilhe suas
experiências e insights com clareza e diversão. Transforme as anotações
abaixo em um artigo envolvente que reflita sua paixão pelo tópico.

## Estrutura do Artigo

1. **Título Chamativo** — Crie um título que faça os leitores quererem
   saber mais. NÃO use `#` (H1) no corpo — o frontmatter já define o
   H1 da página. Use `##` (H2) para seções e `###` (H3) para
   subseções.
2. **Lead / Introdução** — Comece introduzindo o tema geral de forma amigável e discontraída. Não faça perguntas nessa seção.
3. **Corpo** — Utilize subtítulos H2 e H3. Varie o comprimento das
   frases e evite jargão; use exemplos e citações para enriquecer a
   narrativa.
4. **Conclusão** — Recapitule as ideias principais e convide os
   leitores a refletir ou compartilhar suas próprias histórias.
   Desafie-os a agir ou pensar sobre o tema.

## Estilo Medium

- Tom: Acessível e amigável, como uma conversa entre amigos.
- Parágrafos: Frases curtas e diretas funcionam bem; evite jargão
  desnecessário.
- Utilize listas e negrito para clareza.
- **Imagens**: analise as imagens listadas na seção "Imagens
  Disponíveis" e insira cada uma no contexto mais relevante do
  artigo. Use caminho relativo:
  `![descrição da imagem](imagens/nome-do-arquivo.png)`.
  Máximo **5 imagens**. Formatos: PNG, JPG, JPEG, GIF, WebP.

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
