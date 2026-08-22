---
name: escrever-capitulo
description: Use quando o aluno quiser escrever de verdade um capítulo do TCC a partir de um plano já aprovado -- "escreve minha introdução", "escreve o capítulo de metodologia", "vamos escrever o referencial teórico". Rascunha a prosa em dois modos escolhíveis pelo aluno (co-piloto ou rápido), sempre com dado real e citação verificada.
---

# Escrever Capítulo — transforma o plano aprovado em prosa

Esta skill não decide o argumento do capítulo — isso já foi decidido e aprovado em
`tcc-kit/capitulos/<slug>/plano.md` (skill `planejar-capitulo`). O trabalho aqui é transformar aquele
plano em prosa real, sempre com dado e citação verificados — nunca inventa nenhum dos dois, em nenhum
dos dois modos abaixo.

## Passo 1 — Determinar o modo

Leia o campo `Modo de escrita` de `tcc-kit/config.md`.

- **Se `tcc-kit/config.md` não existir, ou existir sem esse campo** (config de uma versão anterior a
  este subprojeto): pergunte ao aluno qual modo ele quer:
  - **`co-piloto`**: eu faço algumas perguntas antes de escrever cada seção, pra usar seu raciocínio de
    verdade.
  - **`rápido`**: eu escrevo direto a partir do plano, com o mínimo de perguntas.

  Se `tcc-kit/config.md` existir, pergunte também se ele quer salvar essa escolha como padrão pras
  próximas vezes. Se confirmar, adicione (ou atualize) o campo `Modo de escrita` no arquivo,
  preservando todos os outros campos como estão:
  ```markdown
  **Modo de escrita:** co-piloto
  ```
  (ou `rápido`, conforme a escolha). Se `tcc-kit/config.md` não existir, não há onde salvar — use a
  escolha só nesta execução e informe ao aluno que rodar `configurar-projeto` primeiro permite fixar um
  padrão da próxima vez.

- **Se o campo já existir**: use o modo salvo por padrão, mas aceite um pedido pontual de troca em
  linguagem natural (ex: "escreve rápido dessa vez", "hoje eu quero com perguntas") sem alterar o valor
  salvo em `config.md`.

## Passo 2 — Carregar o plano

Mapeie o capítulo pedido pro slug correspondente (mesma tabela de `planejar-capitulo`: introdução →
`introducao`, referencial teórico/fundamentação/revisão de literatura → `referencial-teorico`,
metodologia/método → `metodologia`, resultados → `resultados`, discussão/considerações
finais/conclusão → `discussao-consideracoes-finais`).

Leia `tcc-kit/capitulos/<slug>/plano.md`.

- **Se não existir**: avise o aluno que não há um plano aprovado pra esse capítulo ainda, sugira rodar
  `planejar-capitulo` primeiro — mas não bloqueie. Se o aluno quiser seguir sem plano formal (comum no
  modo rápido), pergunte diretamente quais seções ele quer no capítulo e qual o argumento de cada uma,
  de forma resumida, antes de prosseguir pro Passo 3.

## Passo 3a — Modo co-piloto: entrevista por seção

Pra cada seção do plano, faça 1-2 perguntas socráticas específicas do tipo de capítulo antes de
rascunhar aquela seção — nunca despeje todas as perguntas de uma vez, uma seção de cada vez. Use estas
perguntas como base (adapte a redação ao contexto real da seção, mas mantenha o espírito de elicitar o
raciocínio do aluno, não confirmar o óbvio):

- **introducao**: "qual problema real motivou esse tema pra você?" / "o que você quer que o leitor
  entenda logo na primeira página?"
- **referencial-teorico**: "dessas referências que você já validou, qual conceito é o mais central pro
  seu argumento?" / "existe algum contraponto entre os autores que vale destacar?"
- **metodologia**: "por que essa abordagem, e não outra que também resolveria o problema?" / "teve
  alguma limitação prática que influenciou como você conduziu isso?"
- **resultados**: "qual desses números foi o que mais chamou sua atenção, e por quê?" / "algum
  resultado saiu diferente do que você esperava antes de rodar a análise?"
- **discussao-consideracoes-finais**: "que resultado te surpreendeu, ou contradisse o que você
  esperava?" / "qual a principal contribuição prática do que você encontrou?"

Se o capítulo não bater em nenhum dos 5 slugs fixos (capítulo fora da convenção padrão), adapte o
espírito das perguntas — sempre buscando o "porquê" e o "o que te chamou atenção", nunca só pedindo
confirmação do que já está no plano.

Se o aluno responder de forma vaga ou genérica, você pode pedir mais detalhe **uma vez** — não insista
indefinidamente, siga com o que tiver depois da segunda resposta. Rascunhe a seção usando as respostas
reais do aluno como matéria-prima central — nunca escreva o raciocínio no lugar dele, mesmo que a
resposta seja curta.

Depois de rascunhar cada seção, siga pro Passo 4 daquela seção antes de passar pra próxima.

## Passo 3b — Modo rápido: direto do plano

Rascunhe cada seção direto do `Argumento` e das `Referências` já registrados no `plano.md`, sem
perguntas extras. Só pergunte ao aluno se uma seção específica não tiver argumento nenhum registrado no
plano (não dá pra rascunhar do vazio).

## Passo 4 — Grounding anti-alucinação (idêntico nos dois modos)

Antes de finalizar qualquer seção, confira:

- **Toda afirmação numérica ou sobre dado/resultado** precisa vir de `tcc/dados/resumo-real.md`.
  Nunca escreva um número, percentual, ou afirmação de resultado que "parece razoável" — se o dado que
  a seção precisaria não está em `resumo-real.md`, avise o aluno explicitamente e pare naquele ponto em
  vez de inventar ou aproximar.
- **Toda citação** usa só `chave`s presentes em `tcc-kit/referencias/index.yaml` com
  `status: verificado`. Nunca cite uma `chave` com outro status (`pendente-manual`,
  `pendente-conversao`) como se já estivesse pronta, e nunca invente uma citação que não está no
  índice. Se o plano indicava uma referência que não está mais no índice (ex: foi removida depois), avise
  o aluno e pergunte como prosseguir — sem essa citação, ou substituindo por outra da base.

## Passo 5 — Salvar (incremental, por seção)

Assim que uma seção for finalizada (nos dois modos), grave ela imediatamente em
`tcc/capitulos/<slug>.tex` — não acumule o capítulo inteiro em memória até o fim. Isso preserva o
progresso se o aluno interromper no meio de uma entrevista longa (modo co-piloto).

Antes de começar a escrever a primeira seção, confira se `tcc/capitulos/<slug>.tex` já tem conteúdo
real (não só o placeholder que o template deixou — leia o arquivo e julgue pelo conteúdo, não por um
número de caracteres). Se tiver, pergunte ao aluno: sobrescrever tudo, mesclar com o que já existe, ou
só completar as seções que ainda faltam.

## Passo 6 — Resumo final

Informe ao aluno quantas seções foram escritas, e se alguma ficou pendente por falta de dado ou
referência (Passo 4). **Sempre** sugira rodar a skill `revisar-capitulo` antes de considerar o capítulo
pronto — em nenhum dos dois modos esta skill se apresenta como aprovação final, só como rascunho.
