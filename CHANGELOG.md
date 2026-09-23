# Changelog

Toda versão nova aqui corresponde a uma bump em `.claude-plugin/plugin.json` e
`.claude-plugin/marketplace.json`. Alunos que já instalaram recebem a atualização com:

```
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```

## 1.11.0 — 2026-09-23

Revisão mais rigorosa e mais barata, a partir do benchmark com um artigo IEEE
(`docs/benchmarks/2026-09-17-artigo-ieee-latam.md`).

- **Agentes gravam o próprio relatório.** Os 7 agentes ganham a ferramenta Write, só pra gravar o
  relatório no caminho que a skill passou, e devolvem 3 linhas. A skill monta o consolidado com Grep
  nas linhas de achado, sem carregar nem reescrever os relatórios inteiros. Chamados direto pelo aluno
  (sem caminho), continuam respondendo com o relatório completo e sem gravar nada.
- **Trava por hash**: `revisar-capitulo`, `auditoria-tcc-completo` e `preparar-defesa` tiram uma foto
  do projeto antes do despacho e conferem depois (`estado_projeto.py foto`/`comparar`). Se um agente
  mexer em qualquer arquivo além do relatório, o aluno é avisado com a lista.
- **Linha de achado com ID estável** (`DADOS`, `CIT`, `LAC`, `MET`, `ORI`, `BANCA`, `FORMA`, `CONS`).
- **`revisar-capitulo`**: os 6 agentes rodam em paralelo (a prioridade dado → citação → resto vale só
  na consolidação); rodada N com seção Delta (RESOLVIDO / PARCIAL / PENDENTE por ID); achados repetidos
  entre agentes viram uma linha só; relatórios completos em `tcc-kit/relatorios/_brutos/<slug>-<data>/`.
- **`revisor-citacoes`**: confere primeiro o Markdown local de `revisao-bibliografica`, depois o DOI na
  Crossref (com `doi.org` pra Zenodo/DataCite), e só então busca na web; aponta DOI disponível, tipo de
  entrada BibTeX errado e fonte que não sustenta a frase (só quando leu o texto da fonte).
- **`guardiao-metodo`**: checklist para estudos com modelagem (vazamento, escolha no conjunto de
  avaliação, comparação justa, testes múltiplos, diagnósticos, reprodutibilidade) e leitura do script
  que gerou um número quando ele estiver indicado.
- **`guardiao-dados`**: seção Cobertura com o que foi conferido e bateu.
- **Todos os agentes**: log, PDF ou saída de script só contam como evidência se forem da execução atual.
- **Backup** (`estado_projeto.py backup`) em `tcc-kit/versoes/<momento>/` antes de sobrescrever arquivo
  do aluno em `escrever-capitulo`, `escolher-template`, `gerar-diagrama` e `preparar-defesa`. Git, só
  leitura e nunca encadeado.
- `auditoria-tcc-completo` e `preparar-defesa` passam caminhos dos capítulos ao agente em vez de colar o
  conteúdo na instrução.

## 1.10.0 — 2026-09-23

Registro de versões por hash e skill nova `estado-tcc`: o kit passa a saber quando um artefato ficou
desatualizado depois de uma edição, sem reler o texto pra descobrir.

- Script novo: `scripts/estado_projeto.py` (só biblioteca padrão, roda com `uv run`). `registrar` grava
  o sha256 dos arquivos que uma etapa usou em `tcc-kit/.estado.json`; `verificar` compara com os
  arquivos atuais e imprime uma tabela curta (`atual` / `desatualizada` / `entrada-removida`). O hash é
  calculado fora do modelo: nenhuma skill ou agente carrega o arquivo de estado no contexto.
- `escrever-capitulo`, `revisar-capitulo`, `auditoria-tcc-completo` e `preparar-defesa` ganham um passo
  que registra a versão das entradas antes de atualizar checklist e histórico. Se o `uv` não estiver
  disponível, avisam em uma linha e seguem.
- Skill nova: `estado-tcc` — panorama completo do projeto (etapas, capítulos, pontos bloqueantes,
  atividade recente, pendências) montado só a partir de checklist, fim do histórico, seção de achados
  bloqueantes dos relatórios e saída de `verificar`, sem abrir os capítulos. Salva em
  `tcc-kit/estado/estado-<data>.md`, em linguagem legível pelo orientador. Aponta capítulo alterado
  depois da revisão, capítulo escrito com dados que mudaram depois, e auditoria/slides desatualizados.
  Só lê: não edita checklist, histórico nem o registro, e nunca grava hash retroativo.
- Projetos anteriores continuam funcionando: sem `tcc-kit/.estado.json`, `verificar` responde
  `sem registros` e a `estado-tcc` mostra as datas das revisões sem afirmar se estão atuais.

## 1.9.2 — 2026-09-16

`escrever-capitulo` deixa mais visível que os modos `co-piloto`/`rápido` são duas escolhas igualmente
válidas, não uma "certa" e uma "atalho" — reconhecendo que parte dos alunos (e orientadores) trata o
TCC como um requisito a cumprir, não como um projeto de vida, e isso é legítimo. Documenta também o
ciclo de revisão pontual esperado nos dois modos: compilar o capítulo, ler o resultado no PDF, e colar
de volta na conversa qualquer parágrafo que precisar de ajuste, sem precisar editar o `.tex` a mão nem
rodar a skill de novo do zero. `README.md` atualizado com a mesma linguagem.

## 1.9.1 — 2026-09-06

`gerar-diagrama` não trava mais quando o aluno não tem LaTeX instalado localmente (fluxo comum pra
quem usa só Overleaf, já suportado pela skill `escolher-template`). Antes, o Passo 5 rodava
`latexmk -pdf` sem prever esse caso; agora, se o comando não existir no ambiente, a skill avisa que o
código do diagrama já foi salvo e orienta compilar no Overleaf, em vez de tratar como erro. Compilação
que roda mas falha de verdade (sintaxe TikZ errada) continua sendo tratada como sinal de problema real
no diagrama.

## 1.9.0 — 2026-09-06

`revisao-bibliografica` troca `marker` (biblioteca pesada, carrega modelos de ML e dependia de um
binário externo opcional, `llama-server` do `llama.cpp`, pra reconhecimento de fórmula/OCR) por
`pdfplumber` (extração de texto pura Python, sem binário nenhum, mesmo comportamento em qualquer
sistema operacional). Quando a extração automática sai curta/vazia demais (PDF escaneado, ou página com
fórmula/tabela complexa), a skill não pede mais pra instalar nada — o próprio agente lê o PDF original
diretamente (a mesma capacidade de visão que já processa qualquer PDF numa conversa) e escreve o
Markdown a mão. Reduz drasticamente o peso de dependências e elimina qualquer aviso técnico pro aluno
nesse fluxo, sem perder qualidade no caso difícil.

## 1.8.0 — 2026-09-04

Skill nova: `gerar-diagrama`, pra diagramas e ilustrações conceituais em TikZ (fluxograma de
metodologia, framework conceitual, mapa de relacionamento) — sem agente companheiro, sem cobrir gráfico
de dado real (fica pra uma frente futura, ainda sem dono). Diagrama salvo em `tcc/diagramas/<nome>.tex`,
incluído no capítulo via `\input`. Só registra em `tcc-kit/historico.md`; não edita
`tcc-kit/checklist.md` -- diagrama é ação opcional e repetível, diferente dos estágios de ocorrência
única que o checklist já modela.

## 1.7.0 — 2026-08-23

Checklist de progresso e histórico de rastreamento: dois artefatos novos que dão visibilidade contínua
sobre o que já foi feito no TCC, sem precisar reconstruir esse estado inferindo a partir de uma dúzia de
arquivos espalhados.

- Artefato novo: `tcc-kit/checklist.md` — estado atual de cada estágio do ciclo de vida (configuração,
  template, tema, referências, metodologia, um por um dos 5 capítulos, auditoria completa, apresentação
  de defesa). Capítulos e metodologia têm estados intermediários (ex: "Escrito, ainda não revisado",
  "Revisado, com achados bloqueantes pendentes") derivados dos próprios relatórios que as skills já
  produzem — sem lógica de detecção nova.
- Artefato novo: `tcc-kit/historico.md` — jornal de auditoria, uma entrada por skill concluída, em
  ordem cronológica, apontando pro relatório detalhado de cada execução quando existir.
- As 10 skills que produzem algo (todas exceto `iniciar-tcc`) ganham um passo final novo que mantém os
  dois arquivos atualizados. `iniciar-tcc` não muda — continua com sua própria detecção ao vivo,
  independente destes dois artefatos.

## 1.6.0 — 2026-08-22

Consolidação, auditoria cross-capítulo e preparação de defesa: fecha o ciclo de escrita com uma etapa
que lê o TCC inteiro, não capítulo a capítulo.

- Skill nova: `auditoria-tcc-completo` — lê todos os capítulos de uma vez, confere se objetivos da
  Introdução foram respondidos na Discussão, se números que o aluno relata batem entre capítulos, e se
  a terminologia se mantém estável. Inclui lembrete de checklist institucional (Aula 3.1).
- Agente novo: `guardiao-consistencia` (7º da linhagem de revisão) — só é despachado por
  `auditoria-tcc-completo`, nunca por `revisar-capitulo` (que continua com os mesmos 6 agentes de
  sempre, por capítulo).
- Skill nova: `preparar-defesa` — gera apresentação Beamer a partir dos capítulos aprovados (nunca
  inventa conteúdo novo pro slide) e reaproveita o `banca-critica` já existente sobre o TCC completo pra
  gerar prep de perguntas da banca.
- `iniciar-tcc` ganha 2 ramificações de sugestão novas (a 5ª extensão da skill): todos os capítulos
  escritos sem auditoria completa, e auditoria feita sem apresentação de defesa.

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
- `iniciar-tcc` ganha uma nova ramificação de sugestão (a 4ª extensão da skill): tema e referências
  definidos, mas metodologia ainda não validada.

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
