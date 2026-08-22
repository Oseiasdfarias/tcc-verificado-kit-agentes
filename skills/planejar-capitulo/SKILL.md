---
name: planejar-capitulo
description: Use quando o aluno quiser planejar a estrutura de um capítulo do TCC antes de escrever de verdade -- "planeja o capítulo de metodologia", "me ajuda a estruturar o referencial teórico", "quero um plano antes de escrever a introdução".
---

# Planejar Capítulo — estrutura, argumento e referências, antes de escrever

Esta skill gera uma proposta de plano pro capítulo, itera com o aluno até aprovação, e só então salva
o plano final. O plano é sempre uma proposta até o aluno aprovar — nunca vira arquivo definitivo sem
essa aprovação explícita.

## Passo 1 — Identificar o capítulo

Mapeie o que o aluno disse pro slug correspondente:

| Aluno diz (exemplos) | Slug |
|---|---|
| introdução | `introducao` |
| referencial teórico, fundamentação teórica, revisão de literatura | `referencial-teorico` |
| metodologia, método | `metodologia` |
| resultados | `resultados` |
| discussão, considerações finais, conclusão | `discussao-consideracoes-finais` |

Se o aluno pedir um capítulo fora desses 5 (ex: um TCC com estrutura diferente), slugifique livre
(minúsculo, hífen, sem acento) — não force um dos 5 slugs fixos onde não se aplica.

## Passo 2 — Checar plano existente

Confira se `tcc-kit/capitulos/<slug>/plano.md` já existe.

**Se já existir:** mostre o plano atual e pergunte se o aluno quer ajustar esse plano ou recriar do
zero. Não prossiga sem essa resposta.

## Passo 3 — Checar base de referências

Confira se `tcc-kit/referencias/index.yaml` existe e tem pelo menos 1 entrada com `status: verificado`.

**Se não tiver:** avise o aluno explicitamente que ainda não há referência verificada na base, e
pergunte se ele quer que você rode `revisao-bibliografica` antes de planejar, ou se prefere seguir sem
sugestão de referência por enquanto (o plano ainda pode ser útil só pra estrutura). Respeite a escolha
do aluno — não bloqueie.

## Passo 4 — Gerar proposta de estrutura

Proponha uma estrutura de seções. Como ponto de partida (o aluno pode pedir qualquer outra
organização), esses são os padrões mais comuns por tipo de capítulo:

- **introducao**: contexto do problema → problema de pesquisa → objetivos (geral e específicos) →
  justificativa.
- **referencial-teorico**: conceito central → estado da arte (o que a literatura já mostrou) → lacuna
  que o trabalho do aluno endereça.
- **metodologia**: abordagem/tipo de pesquisa → dados/instrumentos usados → procedimento de análise.
- **resultados**: uma seção por pergunta de pesquisa ou hipótese, cada uma apresentando o achado
  correspondente.
- **discussao-consideracoes-finais**: interpretação dos resultados à luz da teoria → limitações do
  estudo → contribuições → considerações finais.

Pra cada seção proposta, escreva 1-3 frases do argumento principal dela, e — se houver
`tcc-kit/referencias/index.yaml` com entradas — sugira quais `chave`s parecem relevantes pra aquela
seção (cruzando o assunto da seção com o `resumo` e `tema_relacionado` de cada referência). Se nenhuma
referência da base parecer relevante pra uma seção específica, deixe essa seção sem referência sugerida
— não force uma correspondência forçada só pra preencher o campo.

## Passo 5 — Iterar

Mostre a proposta completa ao aluno. Aceite pedidos de ajuste (reordenar, remover, adicionar seção,
trocar referência sugerida) e gere uma nova versão até o aluno aprovar explicitamente.

## Passo 6 — Salvar

Só depois da aprovação explícita, crie (ou sobrescreva, já que o aluno concordou no Passo 2 ou está
criando pela primeira vez) `tcc-kit/capitulos/<slug>/plano.md`:

```markdown
# Plano: <Nome do Capítulo>

## Seção 1: <nome da seção>
**Argumento:** <1-3 frases>
**Referências:** <chave1, chave2 — ou "nenhuma" se não se aplica>

## Seção 2: <nome da seção>
**Argumento:** <1-3 frases>
**Referências:** <chave1, chave2 — ou "nenhuma">

---
Aprovado em: <data de hoje, AAAA-MM-DD>
```

A linha `Aprovado em` só entra no arquivo depois da aprovação do Passo 5 — nunca salve um plano sem
essa linha (isso marcaria incorretamente um rascunho como aprovado).

## Passo 7 — Resumo final

Informe o aluno que o plano foi salvo, o caminho do arquivo, e que ele já pode começar a escrever esse
capítulo seguindo o plano — a escrita em si não é conduzida por esta skill.
