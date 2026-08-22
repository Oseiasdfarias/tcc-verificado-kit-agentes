# Changelog

Toda versão nova aqui corresponde a uma bump em `.claude-plugin/plugin.json` e
`.claude-plugin/marketplace.json`. Alunos que já instalaram recebem a atualização com:

```
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```

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
