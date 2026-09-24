---
name: revisar-capitulo
description: Use quando o aluno quiser uma auditoria completa de um capítulo do TCC antes de considerar ele pronto -- roda, em paralelo, verificação de dados, verificação de citações, verificação de metodologia, e as 3 personas de revisão (orientador, banca, forma/português), e produz um relatório único, com comparação item a item quando o capítulo já foi revisado antes.
---

# Revisar Capítulo — auditoria completa do TCC Verificado

Esta skill roda os 6 agentes especialistas do kit contra um capítulo do TCC, ao mesmo tempo, e
consolida tudo em um relatório único, com prioridade para dado e citação.

## Quando usar

O aluno pede algo como "audita esse capítulo antes de eu considerar pronto" ou "roda a revisão
completa". Peça o caminho do capítulo se não foi informado, o caminho do resumo de dados real
(normalmente `tcc/dados/resumo-real.md`) se o capítulo fizer qualquer afirmação sobre
dados/resultados, e o caminho de `tcc-kit/metodologia.md` se existir (usado pelo `guardiao-metodo`).

## Identificar o slug do capítulo

Mapeie o capítulo pedido pro slug correspondente:

| Aluno diz (exemplos) | Slug |
|---|---|
| introdução | `introducao` |
| referencial teórico, fundamentação teórica, revisão de literatura | `referencial-teorico` |
| metodologia, método | `metodologia` |
| resultados | `resultados` |
| discussão, considerações finais, conclusão | `discussao-consideracoes-finais` |

Se o aluno pedir um capítulo fora desses 5 (ex: um TCC com estrutura diferente), slugifique livre
(minúsculo, hífen, sem acento) — não force um dos 5 slugs fixos onde não se aplica.

## Prioridade — importa, mas só na consolidação

Revisar argumento e forma de um capítulo que ainda tem dado inventado ou citação falsa é desperdício
de tempo do aluno. Por isso, no relatório final, dado e citação vêm sempre primeiro (são checagem
factual, bloqueante), e método, argumento, banca e forma depois (são julgamento interpretativo).

Essa prioridade vale **para a leitura do relatório, não para o despacho**: os 6 agentes não leem o
relatório uns dos outros, então rodam todos ao mesmo tempo.

## Passo 1 — Preparar pastas e rodada anterior

- Pasta desta rodada: `tcc-kit/relatorios/_brutos/<slug>-<data de hoje, AAAA-MM-DD>/`. Se já existir
  (segunda revisão no mesmo dia), ela é reaproveitada e os arquivos são sobrescritos.
- Rodada anterior: procure (Glob) a pasta `tcc-kit/relatorios/_brutos/<slug>-*` mais recente com data
  **anterior** à de hoje. Se existir, cada agente vai receber o caminho do próprio relatório dela
  (`<pasta anterior>/<agente>.md`, quando o arquivo existir). Se só houver relatório consolidado antigo
  (`tcc-kit/relatorios/<slug>-*.md`, de antes da versão 1.11, sem pasta `_brutos`), não há delta:
  registre isso no relatório final.
- Número da rodada: quantidade de relatórios consolidados `tcc-kit/relatorios/<slug>-*.md` com data
  anterior à de hoje, mais 1.

## Passo 2 — Foto do projeto (trava)

Os agentes podem gravar arquivos, mas só o próprio relatório. Pra conferir isso, antes do despacho rode:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" foto --saida tcc-kit/relatorios/_brutos/<slug>-<data>/.foto.json tcc tcc-kit
```

O caminho do plugin segue a mesma regra de `revisao-bibliografica`: procure `scripts/estado_projeto.py`
relativo à raiz deste plugin, e não invente um caminho. Se o comando falhar, siga sem a trava e registre
no relatório final que a conferência de integridade não rodou.

## Passo 3 — Despachar os 6 agentes em paralelo

Use a ferramenta Task **uma vez por agente, todas na mesma mensagem**, pra que rodem ao mesmo tempo:
`guardiao-dados`, `revisor-citacoes`, `guardiao-metodo`, `orientador-rigoroso`, `banca-critica`,
`revisor-forma`. Cada instrução leva:

- o caminho do capítulo;
- pro `guardiao-dados`, o caminho do resumo de dados real; pro `guardiao-metodo`, o caminho de
  `tcc-kit/metodologia.md` quando existir (e o resumo de dados, se houver);
- o **caminho do relatório**: `tcc-kit/relatorios/_brutos/<slug>-<data>/<nome do agente>.md`, dizendo
  que ele deve gravar ali e devolver só as 3 linhas;
- quando houver rodada anterior, o **caminho do relatório anterior** daquele agente, pedindo a seção
  `## Delta`.

Não passe log de compilação, PDF ou saída de script como evidência, a não ser que você mesmo tenha
acabado de gerar na conversa atual (e diga isso ao agente).

## Passo 4 — Conferir a trava e as entregas

1. Rode:

   ```bash
   uv run "<caminho do plugin>/scripts/estado_projeto.py" comparar tcc-kit/relatorios/_brutos/<slug>-<data>/.foto.json tcc tcc-kit
   ```

   Se a saída listar qualquer arquivo (`alterado`, `novo` ou `removido`), **avise o aluno antes de
   qualquer outra coisa**, com a lista, dizendo que um agente mexeu em arquivo do projeto quando só
   podia gravar o próprio relatório, e sugira conferir e restaurar esses arquivos. Siga com a
   consolidação, com o mesmo aviso no topo do relatório final. `sem alterações` é o esperado.
2. Confira (Glob) se os 6 brutos existem. Se algum agente devolveu o relatório inteiro na resposta em
   vez de gravar, grave você mesmo esse texto no caminho do bruto. Se algum não entregou nada, despache
   de novo só aquele agente, uma vez; se falhar de novo, registre no relatório final que aquele agente
   não entregou.

## Passo 5 — Consolidar a partir das linhas de achado

**Não abra os brutos inteiros.** Os agentes escrevem cada achado numa linha que começa com
`- **<PREFIXO>-<NN>**`. Pegue só essas linhas com Grep na pasta desta rodada, com o padrão
`^- \*\*[A-Z]+-[0-9]+\*\*` (isso inclui as linhas de `## Delta`, que usam o mesmo começo; distinga pelo
nível: RESOLVIDO, PARCIAL ou PENDENTE). Pegue também, com Grep, a linha seguinte de cada `BANCA`
(o caminho de resposta). Só abra um trecho de um bruto quando precisar desempatar se dois achados são o
mesmo problema. Se um bruto tem conteúdo mas nenhuma linha de achado (agente fora do formato), aí sim
leia esse bruto inteiro e extraia os achados, e registre isso no relatório final.

**Deduplicação:** achados de agentes diferentes com o mesmo trecho e o mesmo problema viram uma linha
só, com todos os IDs (ex: `MET-02 = ORI-05`). Na dúvida, mantenha separados.

Salve em `tcc-kit/relatorios/<slug>-<data>.md`, nesta estrutura:

```markdown
# Auditoria — [nome do capítulo] — [data] (rodada N)

[Se a trava encontrou alteração: aviso aqui, com a lista de arquivos.]

## Achados bloqueantes
[As linhas DADOS (BLOQUEANTE), depois as linhas CIT com nível SUSPEITA e NÃO ENCONTRADA — marque cada
NÃO ENCONTRADA como *conferir manualmente*, não como citação falsa (NÃO ENCONTRADA não é sinônimo de
errada: pode ser uma referência real que a busca não alcançou). Achado bloqueante que o Delta marcou
como PENDENTE ou PARCIAL também entra aqui, com o ID antigo. Se não houver nenhum, escreva
"nenhum achado bloqueante".]

## Delta com a rodada anterior
[Só se houve rodada anterior com brutos. Tabela | ID | Situação | Evidência |, agrupada por situação:
PENDENTE, PARCIAL, RESOLVIDO. Sem rodada anterior com brutos, omita a seção; se houve relatório antigo
sem brutos, escreva só "Rodada anterior sem relatórios por agente (versão antiga do kit): sem
comparação item a item."]

## Apontamentos
### Metodologia
### Argumento (orientador)
### Citações e referências
[CIT com nível APONTAMENTO: DOI disponível, tipo da entrada, sustentação.]
### Lacunas de referência
[Linhas LAC, com o termo de busca sugerido pra `revisao-bibliografica`.]
### Forma e escrita
[Uma linha por achado, já deduplicada. Omita subseção vazia.]

## Perguntas prováveis da banca
[Linhas BANCA com o caminho de resposta.]

## Relatórios completos
[Um link por agente: `_brutos/<slug>-<data>/<agente>.md`. Registre aqui qualquer agente que não
entregou ou saiu do formato.]

---
Revisado por IA — a decisão final sobre cada capítulo é sua (TCC Verificado, Aula 3.2).
```

Depois de salvar, informe ao aluno o caminho do relatório e um resumo de 2-3 frases: quantos achados
bloqueantes, quantos itens da rodada anterior foram resolvidos (se houve), se o revisor-citacoes
encontrou alguma lacuna, e o tom geral dos outros 4 agentes (sólido / precisa de ajuste / muitos
apontamentos) — o tom vem das 3 linhas que cada agente devolveu.

## Registrar a versão das entradas

Depois de salvar o relatório, rode:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" registrar --etapa revisao:<slug> --saida tcc-kit/relatorios/<slug>-<data>.md --entradas <caminho do capítulo> [<caminho do resumo de dados real>] [tcc-kit/metodologia.md]
```

Inclua o resumo de dados real só se ele foi passado ao `guardiao-dados`, e `tcc-kit/metodologia.md`
só se ele foi passado ao `guardiao-metodo`. O caminho do plugin segue a mesma regra de
`revisao-bibliografica`: procure `scripts/estado_projeto.py` relativo à raiz deste plugin, e não
invente um caminho.

Isso grava em `tcc-kit/.estado.json` a versão exata do capítulo (e dos dados e da metodologia) que foi
revisada. Com isso, a skill `estado-tcc` consegue avisar depois que o capítulo mudou e a revisão não
vale mais para a versão atual. Não leia `tcc-kit/.estado.json` nem mostre a saída do comando ao aluno.

- **Comando falhou** (`uv` ausente, script não encontrado, código diferente de 0 e de 2): avise em uma
  linha que o registro de versão não foi gravado e siga para a próxima seção. O relatório já está salvo.
- **Código 2** (`tcc-kit/.estado.json` ilegível): avise o aluno e pergunte se quer apagar o arquivo
  (perdendo os registros de versão) ou corrigir à mão. Não apague sem confirmação. Siga para a próxima
  seção em qualquer caso.

## Atualizar checklist e histórico

Depois de salvar o relatório consolidado (seção anterior), recalcule o estado do capítulo `<slug>` do
zero — não presuma qual era o estado anterior no checklist — nesta ordem:

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

## Dados
**Tipo:** não definido
- [ ] Preparados (tcc-kit/dados/limpeza.md)
- [ ] Resumo real (tcc/dados/resumo-real.md)

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

## Formatação ABNT
- [ ] Nunca rodada

## Auditoria completa do TCC
- [ ] Nunca rodada

## Apresentação de defesa
- [ ] Nunca gerada

---
Atualizado em: <data de hoje, AAAA-MM-DD>, por: revisar-capitulo
```

(edite a linha do capítulo correspondente na tabela antes de salvar, com o estado recalculado).

- **Se já existir**, edite só a linha do capítulo `<slug>` na tabela "Capítulos" pro estado recalculado
  acima (preservando as demais linhas e seções como estão), e atualize a linha final pra `Atualizado
  em: <data de hoje, AAAA-MM-DD>, por: revisar-capitulo`.
- **Se o checklist existente não tiver as seções `## Dados` ou `## Formatação ABNT`** (versão anterior
  do kit), insira-as no lugar do esqueleto acima, no estado inicial, sem mexer nas outras seções.
- **Se o arquivo existir mas não bater com o formato esperado** (seção removida, cabeçalho alterado, não
  reconhecível): não sobrescreva sem avisar. Avise o aluno explicitamente que `tcc-kit/checklist.md`
  existe mas não bate com o formato esperado, e pergunte se quer que a skill recrie o esqueleto (perdendo
  o que foi editado manualmente) ou se prefere corrigir o arquivo manualmente antes de continuar — mesmo
  padrão que `iniciar-tcc` já usa pra `tcc-kit/tema.md` corrompido.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — revisar-capitulo (<nome do capítulo>)
Auditoria rodada pro capítulo <nome do capítulo>. N achados bloqueantes. Relatório:
tcc-kit/relatorios/<slug>-<data>.md.
```

Preencha `N` com a contagem real de itens na seção "Achados bloqueantes" do relatório que acabou de ser
salvo (0 se disser "nenhum achado bloqueante").
