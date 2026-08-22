---
name: validar-metodologia
description: Use quando o aluno quiser definir ou validar a abordagem metodológica do TCC antes de rodar uma análise ou escrever sobre o método -- "que teste eu uso pra isso?", "minha metodologia faz sentido?", "analisa meus dados e me diz que abordagem usar", "não sei como analisar essas entrevistas". Cobre qualquer paradigma de pesquisa (quantitativo, qualitativo, bibliográfico/teórico, misto), não só TCC com dataset.
---

# Validar Metodologia — escolhe e valida a abordagem certa pra pergunta de pesquisa

Esta skill ajuda o aluno a decidir — ou confirma se o que ele já pretende fazer é metodologicamente
adequado — antes de rodar qualquer análise ou escrever o capítulo de Metodologia. Nunca decide sozinha:
explica, recomenda, o aluno confirma. Serve qualquer tipo de TCC, não só o exemplo quantitativo com
dataset que o curso demonstra — quantitativo, qualitativo, bibliográfico/teórico e misto recebem o
mesmo nível de detalhe.

## Passo 1 — Carregar contexto

Confira se `tcc-kit/tema.md` existe. Se existir, extraia os campos **Tema** e **Justificativa** — não
pergunte de novo o que já está registrado ali.

Confira se `tcc-kit/metodologia.md` já existe. Se existir, mostre o conteúdo atual (paradigma, método,
status) e pergunte se o aluno quer revisar/atualizar ou manter como está. Se ele optar por manter, pare
aqui e informe que nada foi alterado.

## Passo 2 — Escolher o modo

Pergunte diretamente: "Você já sabe que método/abordagem quer usar, ou quer que eu analise uma base
real que você já tem (dataset, entrevistas, documentos) e proponha?"

- Se o aluno já sabe → Passo 3a.
- Se quer que a IA analise e proponha → Passo 3b.

## Passo 3a — Aluno decide o paradigma

Pergunte qual dessas descreve melhor a pesquisa do aluno:

1. **Quantitativo** (dataset, pesquisa de campo com números)
2. **Qualitativo** (entrevistas, observação, documentos, sem número como foco central)
3. **Bibliográfico/teórico** (revisão de literatura é o método central, sem coleta de dado primário)
4. **Misto** (combina quantitativo e qualitativo)

### Se quantitativo

Pergunte que tipo de relação/pergunta o aluno quer responder, e recomenda:

- **Associação entre duas variáveis categóricas?** → teste qui-quadrado. Pressuposto: frequência
  esperada de pelo menos 5 em pelo menos 80% das células da tabela (regra de Cochran) — se não
  atendido, sugira o teste exato de Fisher no lugar.
- **Diferença de média/medida numérica entre 2 grupos?** → teste t de Student. Pressuposto:
  distribuição aproximadamente normal em cada grupo — se a amostra for pequena e a normalidade
  duvidosa, sugira o teste não-paramétrico Mann-Whitney U.
- **Diferença entre 3 ou mais grupos?** → ANOVA de um fator. Pressupostos: normalidade em cada grupo e
  homogeneidade de variância (teste de Levene) — se algum pressuposto falhar, sugira Kruskal-Wallis.
- **Relação entre duas variáveis numéricas contínuas?** → correlação de Pearson (pressuposto: relação
  linear e normalidade bivariada) ou, se a relação não for claramente linear ou os dados forem
  ordinais, correlação de Spearman.

Em qualquer teste escolhido, sempre lembre:
- Significância (p-valor) não é o mesmo que relevância prática — peça que o aluno também calcule e
  reporte um tamanho de efeito (V de Cramér pro qui-quadrado, d de Cohen pro teste t, η² pra ANOVA, r
  pra correlação).
- Se mais de um teste for rodado sobre a mesma base (múltiplas comparações), o risco de falso positivo
  aumenta — avise sobre correção (ex: Bonferroni) ou, no mínimo, sobre reportar isso com transparência
  no capítulo de Metodologia.

### Se qualitativo

Pergunte a fonte de dado (entrevista semiestruturada, documento, observação de campo, rede social) e o
que o aluno pretende fazer com ela:

- **Identificar padrões/temas recorrentes no material?** → análise temática (Braun & Clarke). Fases:
  familiarização com os dados, geração de códigos iniciais, busca por temas, revisão dos temas,
  definição e nomeação, produção do relatório. Avise que pular fases (ir direto pra "temas" sem
  codificação sistemática) é a falha mais comum apontada em banca.
- **Categorizar sistematicamente a frequência/presença de elementos específicos?** → análise de
  conteúdo. Precisa de um esquema de categorização definido a priori ou emergente, idealmente com
  verificação de consistência (mais de um codificador, ou o próprio aluno recodificando uma amostra
  depois de um tempo).
- **Analisar como a linguagem constrói significado/poder/ideologia no texto?** → análise de discurso.
  Exige um referencial teórico explícito (ex: Análise de Discurso Crítica de Fairclough, ou a linha
  discursiva francesa) — sem essa base teórica declarada, não é análise de discurso, é impressão de
  leitura.
- **Estudo aprofundado de um caso específico (uma empresa, uma turma, uma comunidade)?** → estudo de
  caso. Exige delimitação clara do que conta como "o caso" e triangulação de mais de uma fonte de dado
  (ex: entrevista + documento + observação) pra sustentar as conclusões.

Lembre sempre dos critérios de rigor equivalentes ao "p<0,05" do quantitativo (Lincoln & Guba):
- **Credibilidade** — os achados representam de verdade a realidade estudada (ex: via triangulação ou
  checagem com os participantes).
- **Confirmabilidade** — outro pesquisador, olhando os mesmos dados, chegaria numa interpretação
  similar (ex: mantendo um diário de decisões analíticas).
- **Transferabilidade** — descrição densa o suficiente do contexto pra outro leitor avaliar se os
  achados se aplicam a outro contexto.
- **Saturação** — nas entrevistas, o ponto em que novas entrevistas param de trazer informação nova,
  dando sustentação ao tamanho da amostra.

### Se bibliográfico/teórico

Pergunte que tipo de revisão o aluno pretende fazer:

- **Narrativa** — mais livre, sem protocolo formal de busca. Apropriada quando o objetivo é
  contextualizar/discutir um tema amplo, não mapear exaustivamente a produção sobre ele.
- **Sistemática** — exige protocolo explícito e replicável: pergunta de pesquisa estruturada, bases de
  dados consultadas, termos de busca, critérios de inclusão/exclusão, e idealmente um fluxo de seleção
  documentado (quantos registros encontrados, quantos excluídos e por quê, quantos incluídos — modelo
  PRISMA é a referência mais usada).
- **Integrativa** — combina literatura teórica e empírica pra construir um panorama mais amplo, com
  critério de qualidade menos rígido que a sistemática, mas ainda documentado.

Valide coerência: se o aluno disser que fará uma revisão "sistemática" mas não conseguir descrever
nenhum critério de inclusão/exclusão nem bases de dados consultadas, avise que isso descreve uma
revisão narrativa, não sistemática — pergunte se quer ajustar a classificação ou estruturar de fato um
protocolo.

### Se misto

Aplique os dois sub-fluxos relevantes (quantitativo e qualitativo, ou quantitativo e bibliográfico,
conforme o caso) separadamente, e pergunte adicionalmente como os dois componentes se integram (ex: os
dados qualitativos explicam um achado quantitativo inesperado; ou os dados quantitativos testam um
padrão sugerido pelas entrevistas). Um TCC misto sem essa integração explícita é, na prática, dois
estudos soltos, não um estudo misto — avise se notar isso.

## Passo 3b — IA analisa e propõe

Pergunte se o aluno tem um arquivo de dado (caminho de um CSV) ou uma pasta de texto
(transcrições/documentos) pra apontar.

- **Se apontar um arquivo tabular (CSV)**: leia a estrutura (nomes de coluna, tipos, algumas linhas de
  amostra — use Bash com pandas, mesma ferramenta que a Aula 2.2/2.3 do curso já ensina o aluno a pedir
  manualmente). Classifique cada coluna relevante como categórica ou numérica, proponha o teste
  apropriado seguindo exatamente os mesmos critérios do Passo 3a (quantitativo) com base no que
  encontrar, e explique o porquê antes de perguntar se o aluno confirma.
- **Se apontar uma pasta de texto**: leia uma amostra representativa (os 2-3 primeiros arquivos
  inteiros, e uma contagem de arquivos/linhas pra caracterizar o volume total, em vez de ler tudo de
  uma vez e arriscar estourar o contexto). Caracterize o tipo de material (entrevista transcrita,
  documento institucional, post de rede social) e proponha a técnica de análise qualitativa mais
  coerente, seguindo os mesmos critérios do Passo 3a (qualitativo).
- **Se não apontar nada**: confira `tcc-kit/tema.md` e `tcc-kit/referencias/index.yaml`. Se
  `referencias/index.yaml` existir, conte as entradas com `status: verificado` e observe os campos
  `tema_relacionado` e `resumo` pra entender que linha teórica já foi levantada. Proponha paradigma
  bibliográfico/teórico e o tipo de revisão mais coerente com a quantidade e natureza do que já foi
  levantado (ex: poucas referências e ainda exploratórias → sugira narrativa; recorte temático já claro
  e volume razoável → pode sugerir integrativa).
- **Se nada disso existir** (nem arquivo apontado, nem `tema.md`, nem `referencias/index.yaml` com
  entradas): avise explicitamente que não há informação suficiente pra propor nada, e sugira usar o
  Passo 3a (aluno decide) em vez disso. Nunca invente uma base de dado ou corpus que não existe.

Em qualquer um dos três primeiros casos, explique a proposta (paradigma + método + por quê) e os
pressupostos/critérios de rigor associados (os mesmos do Passo 3a) antes de seguir — o aluno confirma
ou pede ajuste. Só depois de confirmado, vá pro Passo 4.

## Passo 4 — Consolidar pressupostos

Junte, num checklist, os pressupostos/critérios de rigor específicos do método que ficou definido
(Passo 3a ou 3b) — os mesmos itens detalhados nas seções acima pro método escolhido.

## Passo 5 — Salvar

Salve (ou atualize) `tcc-kit/metodologia.md`:

```markdown
# Metodologia — <paradigma>

**Paradigma:** <Quantitativo | Qualitativo | Bibliográfico/teórico | Misto>
**Método escolhido:** <ex: teste qui-quadrado / análise temática / revisão sistemática>
**Como foi definido:** <Aluno decidiu diretamente | IA analisou <fonte> e propôs, aluno confirmou>

## Justificativa
<por que esse método serve a essa pergunta de pesquisa / a esse dado>

## Pressupostos e critérios de rigor a verificar
- [ ] <item específico do método escolhido>
- [ ] <item específico do método escolhido>

## Status
<Pendente de execução | Executado (ver tcc/dados/resumo-real.md) | Não se aplica (bibliográfico/teórico)>

Definido em: <data de hoje, AAAA-MM-DD>
```

Status inicial: "Pendente de execução" pra quantitativo (ou componente quantitativo de um misto) ainda
não rodado; "Não se aplica" pra bibliográfico/teórico puro; pra qualitativo, "Pendente de execução" se
a coleta/codificação ainda não aconteceu, ou "Executado" se o aluno já tiver feito e estiver só
validando retroativamente.

## Passo 6 — Resumo final

Informe o que foi salvo (paradigma + método). Se o método ainda não foi executado, lembre que, depois
de rodar a análise (ou fazer a coleta/codificação), `tcc/dados/resumo-real.md` deve registrar o
resultado real, pra `escrever-capitulo` e `guardiao-dados` poderem usar como fonte de verdade. Se já
existia `plano.md` ou capítulo de Metodologia/Resultados escrito antes desta skill rodar, sugira rodar
`revisar-capitulo` — o `guardiao-metodo` vai conferir coerência com o que acabou de ser definido aqui.

## Tratamento de erro

- **Modo "IA analisa" sem nenhuma base disponível**: avisa explicitamente, sugere o modo "aluno decide"
  em vez disso — nunca inventa uma base.
- **Arquivo/pasta apontado pelo aluno não existe ou não pode ser lido**: avisa, não tenta adivinhar o
  conteúdo.
- **`tcc-kit/metodologia.md` já existe**: mostra o conteúdo atual, pergunta se quer revisar ou manter
  (Passo 1).
- **Paradigma misto com só um componente detalhado**: pergunta explicitamente se falta detalhar o
  outro.
