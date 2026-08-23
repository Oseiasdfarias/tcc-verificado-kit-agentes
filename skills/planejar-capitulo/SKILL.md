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

Se o aluno escolheu no Passo 2 ajustar o plano existente (em vez de recriar do zero), use o conteúdo
atual de `tcc-kit/capitulos/<slug>/plano.md` como ponto de partida da proposta: mantenha as seções e
argumentos já aprovados, e aplique só os ajustes que o aluno pedir. Não gere uma estrutura nova do zero
nesse caso.

Se o aluno escolheu recriar do zero (ou não havia plano anterior), proponha uma estrutura de seções.
Como ponto de partida (o aluno pode pedir qualquer outra organização), esses são os padrões mais comuns
por tipo de capítulo:

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
`tcc-kit/referencias/index.yaml` com entradas de `status: verificado` — sugira quais `chave`s dessas
entradas parecem relevantes pra aquela seção (cruzando o assunto da seção com o `resumo` e
`tema_relacionado` de cada referência). Nunca sugira uma entrada com `status: pendente-manual` ou
`pendente-conversao` — ela ainda não foi confirmada como referência utilizável, e sugeri-la como se
fosse contradiria a promessa do kit de só entrar referência já validada. Se nenhuma referência
verificada parecer relevante pra uma seção específica, deixe essa seção sem referência sugerida — não
force uma correspondência forçada só pra preencher o campo.

Se o aluno já respondeu no Passo 3 que quer seguir sem sugestão de referência (por não haver nenhuma
verificada na base ainda), pule a sugestão de `chave`s nesta etapa — proponha só o argumento de cada
seção.

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

Informe o aluno que o plano foi salvo, o caminho do arquivo, e que ele já pode pedir pra escrever esse
capítulo — a skill `escrever-capitulo` transforma esse plano em prosa de verdade, em dois modos
(co-piloto ou rápido).

## Passo 8 — Atualizar checklist e histórico

Recalcule o estado do capítulo `<slug>` do zero — não presuma qual era o estado anterior no checklist —
nesta ordem:

1. `tcc-kit/capitulos/<slug>/plano.md` não existe → estado é "Não iniciado".
2. `plano.md` existe, mas `tcc/capitulos/<slug>.tex` não existe ou não tem conteúdo real (mesmo
   critério de julgamento de leitura que `revisor-forma`/`iniciar-tcc` já usam — não é limite fixo de
   caracteres, é conferir se há texto real, não só o placeholder do template) → estado é "Planejado".
3. `tcc/capitulos/<slug>.tex` tem conteúdo real, mas não existe nenhum arquivo
   `tcc-kit/relatorios/<slug>-*.md` → estado é "Escrito, ainda não revisado".
4. Existe pelo menos um `tcc-kit/relatorios/<slug>-*.md` → leia o mais recente (maior data no nome do
   arquivo) e confira a seção "Achados bloqueantes": se disser "nenhum achado bloqueante", estado é
   "Revisado, sem achados bloqueantes"; caso contrário (pelo menos um achado listado), estado é
   "Revisado, com achados bloqueantes pendentes".

Confira se `tcc-kit/checklist.md` existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a linha do capítulo `<slug>` já
  refletindo o estado recalculado acima (as demais linhas e seções ficam no estado inicial, como no
  esqueleto — use o nome do capítulo por extenso na tabela: Introdução, Referencial teórico,
  Metodologia, Resultados, ou Discussão/Considerações finais, conforme o slug):

```markdown
# Checklist de progresso — TCC

## Configuração institucional
- [ ] Configurado (tcc-kit/config.md)

## Template
- [ ] Escolhido/adaptado (tcc-kit/template.md)

## Tema
- [ ] Definido (tcc-kit/tema.md)

## Referências
- [ ] Pelo menos 1 referência verificada

## Metodologia
**Estado:** Não iniciado

## Capítulos
| Capítulo | Estado |
|---|---|
| Introdução | Não iniciado |
| Referencial teórico | Não iniciado |
| Metodologia | Não iniciado |
| Resultados | Não iniciado |
| Discussão/Considerações finais | Não iniciado |

## Auditoria completa do TCC
- [ ] Nunca rodada

## Apresentação de defesa
- [ ] Nunca gerada

---
Atualizado em: <data de hoje, AAAA-MM-DD>, por: planejar-capitulo
```

(edite a linha do capítulo correspondente na tabela antes de salvar, com o estado recalculado — o
esqueleto acima mostra o estado inicial de todas as linhas só como ponto de partida).

- **Se já existir**, edite só a linha do capítulo `<slug>` na tabela "Capítulos" pro estado recalculado
  acima (preservando as demais linhas e seções como estão), e atualize a linha final pra `Atualizado
  em: <data de hoje, AAAA-MM-DD>, por: planejar-capitulo`.
- **Se o arquivo existir mas não bater com o formato esperado** (seção removida, cabeçalho alterado, não
  reconhecível): não sobrescreva sem avisar. Avise o aluno explicitamente que `tcc-kit/checklist.md`
  existe mas não bate com o formato esperado, e pergunte se quer que a skill recrie o esqueleto (perdendo
  o que foi editado manualmente) ou se prefere corrigir o arquivo manualmente antes de continuar — mesmo
  padrão que `iniciar-tcc` já usa pra `tcc-kit/tema.md` corrompido.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — planejar-capitulo (<nome do capítulo>)
Plano do capítulo <nome do capítulo> aprovado. Arquivo: tcc-kit/capitulos/<slug>/plano.md.
```
