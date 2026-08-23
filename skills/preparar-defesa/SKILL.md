---
name: preparar-defesa
description: Use quando o TCC já estiver completo e o aluno quiser preparar a defesa -- "transforma meu TCC numa apresentação", "me ajuda a preparar a defesa", "gera os slides pra minha banca". Gera uma apresentação Beamer a partir dos capítulos já aprovados e um material de prep de perguntas prováveis da banca.
---

# Preparar Defesa — apresentação Beamer + prep de perguntas

Esta skill transforma o TCC já escrito numa apresentação de defesa, e prepara o aluno pras perguntas
mais prováveis da banca — a versão automatizada da Aula 3.3 do curso.

## Passo 1 — Conferir auditoria prévia

Confira se existe algum arquivo `tcc-kit/relatorios/auditoria-completa-*.md`. Se não existir nenhum,
avise o aluno e pergunte se ele quer rodar `auditoria-tcc-completo` antes de gerar a apresentação — mas
siga direto pra geração se ele preferir. Isso é sugestão, não bloqueio, mesmo princípio de sempre.

## Passo 2 — Gerar a apresentação

**COMPORTAMENTO CRÍTICO — SE DESCOBRIR CAPÍTULOS FALTANDO, GERE A APRESENTAÇÃO DIRETO COM SEÇÕES PENDENTES MARCADAS. NÃO PERGUNTE AO ALUNO SE QUER PROSSEGUIR OU PREENCHER CAPÍTULOS PRIMEIRO. A ÚNICA PERGUNTA PERMITIDA NESTE FLUXO É A DO PASSO 1 (AUDITORIA). PROSSIGA DIRETO PARA GERAÇÃO SEM NENHUMA PERGUNTA ADICIONAL — EXCETO SE NENHUM CAPÍTULO TIVER CONTEÚDO REAL. NESSE CASO (ZERO CAPÍTULOS), NÃO GERE NADA: SIGA A REGRA DE "TRATAMENTO DE ERRO" ABAIXO E RECUSE, SUGERINDO `escrever-capitulo`. ESTA EXCEÇÃO SÓ VALE PRA ZERO CAPÍTULOS — COM PELO MENOS UM CAPÍTULO COM CONTEÚDO REAL, A REGRA DE PROSSEGUIR DIRETO SEM PERGUNTAR CONTINUA VALENDO INTEGRALMENTE.**

Leia os capítulos com conteúdo real disponíveis em `tcc/capitulos/`. Gere `tcc/apresentacao-defesa.tex`
em Beamer, com esta estrutura:

1. **Capa/título** — título do TCC (de `tcc-kit/tema.md`, campo **Tema**), nome do aluno, instituição,
   orientador (de `tcc-kit/config.md`, se existir).
2. **Introdução** — problema e objetivos, resumidos do capítulo `introducao`.
3. **Referencial teórico** — só os 2-3 conceitos mais centrais pro argumento, resumidos do capítulo
   `referencial-teorico` — não é um resumo de tudo, é o mínimo que sustenta o que vem depois.
4. **Metodologia** — resumo do capítulo `metodologia` (ou de `tcc-kit/metodologia.md`, se existir, pro
   paradigma/método).
5. **Resultados** — os achados principais do capítulo `resultados`. Se `tcc/capitulos/resultados.tex`
   tiver algum gráfico TikZ (Aula 2.8), reaproveite o código do gráfico no slide correspondente, em vez
   de recriar do zero. `tcc/apresentacao-defesa.tex` é um arquivo novo e separado, com preâmbulo
   próprio — ele precisa compilar sozinho, sem depender do preâmbulo do template principal do TCC. Se o
   código TikZ reaproveitado precisar de pacotes (`tikz`, `pgfplots`, etc.) ou de uma declaração
   `\pgfplotsset{compat=...}`, inclua tudo isso no preâmbulo da apresentação também.
6. **Discussão/Considerações finais** — síntese do capítulo `discussao-consideracoes-finais`.

**Extensão da apresentação**: mire em algo em torno de 12-18 slides de conteúdo no total — uma faixa
razoável pra uma defesa de 15-20 minutos, duração comum desse tipo de banca. Introdução e Resultados
tendem a merecer relativamente mais slides que Referencial teórico ou Metodologia, que devem ficar
enxutos (mesmo espírito da instrução acima de "só os 2-3 conceitos mais centrais"). Isso é orientação
de proporção, não uma regra fixa pra contar e forçar mecanicamente.

**Grounding (igual ao `escrever-capitulo`)**: toda afirmação de qualquer slide precisa rastrear pra algo
já escrito em algum capítulo aprovado — nunca invente dado, número, ou conclusão nova só pro slide. Se
um capítulo necessário pra alguma seção não existir com conteúdo real, gere a apresentação normalmente
mas marque aquela seção explicitamente como pendente (ex: um slide com "Seção pendente — capítulo de
Resultados ainda não escrito"), em vez de inventar conteúdo de preenchimento.

## Passo 3 — Prep de perguntas

Use a ferramenta Task pra despachar o agente `banca-critica` (já existente, sem nenhuma mudança
necessária — ele já aceita "um resumo do TCC completo" como entrada), passando o conteúdo de todos os
capítulos disponíveis lidos no Passo 2. Peça explicitamente um número maior de perguntas — o dobro do
padrão que ele normalmente geraria pra um capítulo — já que aqui ele está analisando o TCC inteiro, não
um capítulo isolado.

## Passo 4 — Salvar e resumir

Salve o relatório do `banca-critica` em `tcc-kit/relatorios/prep-perguntas-defesa-<data>.md` (data no
formato AAAA-MM-DD), sem reformatação adicional.

Informe ao aluno os dois arquivos gerados: `tcc/apresentacao-defesa.tex` e o prep de perguntas. Feche
lembrando — mesmo espírito da Aula 3.2 que o próprio `banca-critica` já usa no fechamento do relatório
dele — que apresentar é diferente de ler slide: recomende que o aluno treine explicar cada ponto com as
próprias palavras antes da defesa de verdade.

## Tratamento de erro

- **Nenhum capítulo com conteúdo real ainda**: avise que não há nada pra apresentar ainda, sugira
  `escrever-capitulo` primeiro — não gere uma apresentação vazia.
- **Alguns capítulos faltando**: gere a apresentação com as seções correspondentes marcadas como
  pendentes (Passo 2) — nunca invente conteúdo de preenchimento.
- **Sem auditoria prévia**: avisa e pergunta (Passo 1), segue se o aluno confirmar.

## Passo 5 — Atualizar checklist e histórico

**Se o Passo 2 recusou gerar a apresentação** (caso de zero capítulos com conteúdo real, ver
"Tratamento de erro"), não atualize nem o checklist nem o histórico — nada foi produzido.

**Se `tcc/apresentacao-defesa.tex` foi gerado** (Passo 2 e Passo 4 concluídos), confira se
`tcc-kit/checklist.md` existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a seção "Apresentação de defesa" já
  marcada (as demais seções ficam no estado inicial, como no esqueleto):

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
- [x] Gerada em <data de hoje, AAAA-MM-DD>

---
Atualizado em: <data de hoje, AAAA-MM-DD>, por: preparar-defesa
```

- **Se já existir**, edite só a seção "Apresentação de defesa" pra `- [x] Gerada em <data de hoje,
  AAAA-MM-DD>` (preservando as demais seções como estão), e atualize a linha final pra `Atualizado em:
  <data de hoje, AAAA-MM-DD>, por: preparar-defesa`.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — preparar-defesa
Apresentação de defesa gerada (tcc/apresentacao-defesa.tex) e prep de perguntas salvo
(tcc-kit/relatorios/prep-perguntas-defesa-<data>.md).
```
