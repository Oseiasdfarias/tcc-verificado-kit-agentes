# Changelog

Toda versão nova aqui corresponde a uma bump em `.claude-plugin/plugin.json` e
`.claude-plugin/marketplace.json`. Alunos que já instalaram recebem a atualização com:

```
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```

## 1.5.0 — 2026-08-22

Validação metodológica: fecha o gap identificado na análise completa de estrutura de agentes — a Aula
2.3 ensinava só uma regra de bolso pra interpretar teste estatístico, sem nenhuma validação de rigor.

- Skill nova: `validar-metodologia` — dois modos (`aluno decide` ou `IA analisa e propõe`), cobrindo
  quatro paradigmas de pesquisa como cidadãos de primeira classe: quantitativo, qualitativo,
  bibliográfico/teórico, misto. Não fica preso ao exemplo de dataset do curso. Salva
  `tcc-kit/metodologia.md`.
- Agente novo: `guardiao-metodo` (6º da linhagem de revisão) — confere coerência entre o método
  descrito no capítulo e o que foi validado, e aponta conclusão que extrapola o que o método permite
  (ex: tratar correlação como causalidade). Integrado ao `revisar-capitulo`.
- `iniciar-tcc` agora detecta um 9º estágio: tema e referências definidos, mas metodologia ainda não
  validada.

## 1.4.2 — 2026-08-22

Correção: no tema escuro do GitHub, o Mermaid do README (`## Como funciona`) aplicava sua cor de texto
padrão do dark theme (clara) por cima do preenchimento claro dos blocos coloridos — texto quase
ilegível. Cada `classDef` agora fixa `color:#1e1e1e`, garantindo contraste em claro e escuro.

## 1.4.1 — 2026-08-22

Correção: o diagrama Mermaid simplificado no README (`## Como funciona`) tinha ficado de fora do merge
da PR #6 — o merge capturou a branch antes do commit de simplificação chegar ao remoto, então
`develop` ainda mostrava a versão detalhada antiga. Sem mudança de comportamento do kit.

## 1.4.0 — 2026-08-22

Escrita assistida de capítulo: transforma o plano aprovado em prosa real, em dois modos escolhíveis
pelo aluno.

- Skill nova: `escrever-capitulo` — modo `co-piloto` (entrevista socrática por seção, rascunha com as
  respostas reais do aluno) ou `rápido` (rascunha direto do plano, sem perguntas extras). Grounding
  anti-alucinação idêntico nos dois modos: todo dado vem de `tcc/dados/resumo-real.md`, toda citação
  usa só referência com `status: verificado`. Sempre sugere `revisar-capitulo` antes de considerar o
  capítulo pronto.
- `tcc-kit/config.md` ganha o campo `Modo de escrita` (extensão retrocompatível — configs antigos
  continuam funcionando, a skill pergunta e oferece salvar quando o campo não existe)
- `iniciar-tcc` agora detecta um 7º estágio: plano aprovado mas capítulo ainda sem conteúdo real
  escrito

## 1.3.0 — 2026-08-22

Template LaTeX por universidade: coleta os dados institucionais do projeto e ajuda a encontrar/adaptar
um template LaTeX da sua universidade (quando existir no Overleaf).

- Skill nova: `configurar-projeto` (coleta universidade, curso, orientador, banca, dados do aluno —
  salva `tcc-kit/config.md`)
- Skill nova: `escolher-template` (busca no Overleaf via WebSearch, apresenta candidatos + link da
  galeria geral, orienta o download manual — Overleaf não oferece download automático —, reorganiza
  arquivo de template quando a estrutura vier diferente da convenção do kit, adapta capa/folha de
  rosto com os dados do onboarding)
- `iniciar-tcc` agora detecta configuração e template como os 2 primeiros estágios da cadeia, antes de
  tema

## 1.2.1 — 2026-08-22

Correção: `revisao-bibliografica` não travava mais a conversão inteira sem o binário `llama-server`
(dependência do `marker` pra reconhecimento de fórmula em CPU), mas ainda perdia o PDF inteiro quando
ele faltava — mesmo pra artigos sem nenhuma fórmula.

- `scripts/pdf_to_md.py` agora tenta a conversão completa primeiro; se falhar especificamente por
  `llama-server` ausente, tenta de novo com extração pura de texto (sem fórmula/OCR) em vez de falhar
  tudo. Novo código de saída `3` sinaliza esse caso.
- `revisao-bibliografica` reconhece o código `3`: referência ainda entra como `verificado` (o texto é
  real), mas o aluno é avisado que fórmulas daquele artigo podem precisar de conferência manual.

## 1.2.0 — 2026-08-22

Orquestração em estágios adaptativos: detecta em que ponto do TCC você está e sugere o próximo passo,
sem forçar um roteiro fixo.

- Skill nova: `iniciar-tcc` (detecta tema/referências existentes, sugere o próximo passo, sempre com
  confirmação do aluno)
- Skill nova: `escolher-tema` (conduz o brainstorm de tema até confirmação, salva `tcc-kit/tema.md`)
- Skill nova: `planejar-capitulo` (gera e itera o plano de um capítulo, salva
  `tcc-kit/capitulos/<capítulo>/plano.md`)
- `tcc/referencias/` e `tcc/relatorios/` migraram pra `tcc-kit/referencias/` e `tcc-kit/relatorios/` —
  namespace novo dedicado a tudo que o kit gera, separado do conteúdo real do TCC (`tcc/`)
- **Se você já tinha `tcc/referencias/` ou `tcc/relatorios/` de uma instalação 1.1.0 anterior**, a
  atualização não move nada automaticamente: renomeie essas pastas manualmente pra
  `tcc-kit/referencias/` e `tcc-kit/relatorios/` antes de continuar usando o kit. Sem esse passo, as
  skills não vão mais achar sua base de referências existente, e o checador de duplicata da
  `revisao-bibliografica` não vai reconhecer o que já foi baixado antes.

## 1.1.0 — 2026-08-22

Motor de revisão bibliográfica: busca, confirmação, download e indexação de referências reais antes
da escrita, com base "viva" que se atualiza durante o processo.

- Skill nova: `revisao-bibliografica` (busca via Semantic Scholar API + fallback WebSearch, download
  com fallback manual em `baixar-manualmente.md`, conversão PDF→MD via `marker`, índice em
  `tcc/referencias/index.yaml`)
- Script novo: `scripts/pdf_to_md.py`
- `revisor-citacoes` agora detecta lacuna (afirmação sem citação, ou citação NÃO ENCONTRADA) e sugere
  rodar `revisao-bibliografica` — sempre com confirmação do aluno antes de buscar

## 1.0.0 — 2026-08-21

Primeira versão publicada como plugin do Claude Code. Conteúdo idêntico ao kit que já era distribuído
como pasta pra copiar — só a forma de instalação mudou.

- 5 agentes: `guardiao-dados`, `revisor-citacoes`, `orientador-rigoroso`, `banca-critica`,
  `revisor-forma`
- 1 skill: `revisar-capitulo` (orquestra os 5 em sequência, consolida relatório único)
