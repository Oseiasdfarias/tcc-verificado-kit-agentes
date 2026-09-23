# Benchmark — fluxo do tcc-kit aplicado a um artigo de periódico (IEEE LATAM)

**Data:** 2026-09-17
**Versão do kit:** 1.9.2 (agentes e skills lidos direto deste repositório, sem instalar o plugin)
**Caso:** artigo derivado de um TCC de Engenharia Elétrica (aeropêndulo com ESP32, identificação ARX,
controle PID, visualização 3D), alvo *IEEE Latin America Transactions*
**Projeto avaliado:** `Projeto_Tcc_Oseias_Oficial/` (pastas `artigo_ieee_latam/` e `artigo_ieee_latam_en/`)

---

## 1. Resumo

O kit foi usado fora do caso para o qual foi desenhado (TCC com 5 capítulos, ABNT, português) para
auditar e depois reescrever um artigo IEEE de 6–9 páginas. Com adaptações feitas na hora, o fluxo
funcionou e mudou o resultado de forma concreta:

| Indicador | Rodada 1 (rascunho original) | Rodada 2 (versão reescrita) |
|---|---|---|
| Divergências texto × dados (`guardiao-dados`) | 30, todas bloqueantes | 0 |
| Referências com problema (`revisor-citacoes`) | 2 suspeitas (1 com autoria errada), 3 com tipo BibTeX errado, 0 com DOI | 0; 25 verificadas, todas com DOI ou ISBN |
| Apontamentos de método (`guardiao-metodo`) | 15 | 6 novos (1 grave: vazamento de validação, introduzido na reescrita) |
| Apontamentos de argumento (`orientador-rigoroso`) | 21 | 5 novos, menores |
| Risco de rejeição sem revisão (`banca-critica`, simulado) | alto | médio |
| Achados de consistência (`guardiao-consistencia`) | 22 (incluindo PT × EN) | 7, todos tratados |
| Itens obrigatórios do periódico ausentes | 7 | 5, todos dependentes do autor (fotos, vídeo, revisores etc.) |
| Páginas / avisos de compilação | 7 / 3 caixas estouradas | 8 / nenhum |

Custo total dos subagentes: **≈1,30 milhão de tokens** em **13 despachos** (300 chamadas de
ferramenta). A maior parte do valor, porém, não veio só dos agentes: os achados mais importantes
para o conteúdo científico vieram de **executar os scripts do projeto e ler o firmware** para montar
o `resumo-real.md`, uma etapa que o kit hoje não tem (seção 5.3).

---

## 2. Caso de teste

**Estado inicial do artigo.** Rascunho completo em português, 5 seções, 7 páginas, compilando.
Escrito com apoio de IA a partir da monografia. Não havia `tcc/dados/resumo-real.md` nem
`tcc-kit/`.

**Fontes de verdade disponíveis no projeto:**

- 9 CSVs de ensaio (1 de identificação e 2 de malha fechada usados no artigo);
- dois scripts de métricas escritos depois da defesa (`metricas_validacao.py`,
  `metricas_malha_fechada.py`);
- o firmware do ESP32 (C++) e o histórico git;
- resumos da monografia em `docs_tcc/`.

**Periódico.** IEEE LATAM: 6–9 páginas, template IEEEtran, corpo em PT/ES/EN, mas título, resumo e
index terms obrigatoriamente em inglês. Exige DOI em toda referência, fotos e biografias, graphical
abstract, video abstract e carta ao editor com 3 revisores sugeridos, CRediT e divulgação de
trabalhos prévios (o TCC).

---

## 3. Como o fluxo foi executado

### 3.1 Mapeamento skill → uso no artigo

| Skill do kit | Uso neste benchmark | Adaptação necessária |
|---|---|---|
| `configurar-projeto` | `tcc-kit/config.md` preenchido a partir do contexto | Campos de periódico, idioma e template não existem no esqueleto |
| `validar-metodologia` | `tcc-kit/metodologia.md` escrito a partir do que foi **de fato executado** | Paradigma "experimental de bancada única" não tem roteiro próprio |
| — (não existe) | `tcc-kit/dados/resumo-real.md` montado rodando os scripts, lendo o firmware e o git | **Etapa nova, manual e decisiva** |
| `revisar-capitulo` | Os 6 agentes, cada um sobre o artigo inteiro (não por seção) | 5 slugs fixos → 5 (depois 7) seções; ABNT → IEEE |
| `auditoria-tcc-completo` | `guardiao-consistencia` + checklist institucional | Checklist institucional → requisitos do periódico, pesquisados na web por um agente extra |
| `revisao-bibliografica` | Verificação de 25 candidatas e geração do `.bib` | DOI obrigatório e tipo de entrada BibTeX |
| `escrever-capitulo` (modo rápido) | Reescrita em inglês das 7 seções, com grounding no `resumo-real.md` | Idioma, estilo IEEE e seções livres |
| `revisar-capitulo` (2ª vez) | Rodada 2 com tabela RESOLVIDO / PARCIAL / PENDENTE | Modo "rodada N" não existe no kit |
| `preparar-defesa` | Substituída por rascunho da carta ao editor | Pacote de submissão não existe no kit |

### 3.2 Despacho dos agentes

- **Como foram despachados.** Os agentes do plugin não estavam instalados, então cada um rodou como
  subagente genérico (modelo `sonnet`, igual ao frontmatter). A primeira instrução de cada despacho
  era ler o próprio arquivo `agents/<nome>.md` e seguir a persona, com um parágrafo de adaptação para
  artigo.
- **Ordem na rodada 1.** Segui a regra do `revisar-capitulo`: `guardiao-dados` e `revisor-citacoes`
  primeiro, em paralelo. Os outros quatro, mais `guardiao-consistencia` e o agente de requisitos do
  periódico, foram despachados em paralelo depois.
- **Ordem na rodada 2.** Todos em paralelo; em dois despachos juntei duas personas cada
  (`guardiao-metodo` + `orientador-rigoroso` e `revisor-forma` + `guardiao-consistencia`).
- **Consolidação.** Os relatórios brutos foram salvos em `relatorios/_brutos/` e
  `relatorios/_brutos_r2/` e concatenados no formato do `revisar-capitulo`, com os achados
  bloqueantes no topo.

### 3.3 Decisões que só o autor podia tomar

Antes da reescrita, quatro perguntas foram feitas ao autor:

1. idioma de submissão (resposta: inglês completo);
2. o que fazer com o termo "gêmeo digital" (resposta: sombra digital);
3. se podia rodar análises novas com os dados existentes (resposta: sim, as quatro propostas);
4. se havia acesso ao protótipo (resposta: não; declarar a versão do firmware usada em 2023).

O kit não tem um momento previsto para essas decisões entre a auditoria e a reescrita.

---

## 4. Métricas por agente

### 4.1 Custo

| Rodada | Agente | Tokens | Ferramentas | Tempo (s) |
|---|---|---:|---:|---:|
| 1 | guardiao-dados | 92.691 | 13 | 256 |
| 1 | revisor-citacoes | 140.452 | 60 | 474 |
| 1 | guardiao-metodo | 81.216 | 13 | 182 |
| 1 | orientador-rigoroso (inclui reenvio) | 89.429 | 12 | 282 |
| 1 | banca-critica | 77.340 | 10 | 175 |
| 1 | revisor-forma | 101.873 | 24 | 308 |
| 1 | guardiao-consistencia (+ PT × EN) | 96.800 | 18 | 200 |
| 1 | requisitos do periódico (agente extra) | 64.613 | 15 | 156 |
| — | verificação de referências / BibTeX | 89.452 | 47 | 309 |
| 2 | guardiao-dados | 97.894 | 15 | 292 |
| 2 | guardiao-metodo + orientador-rigoroso | 127.388 | 23 | 380 |
| 2 | banca-critica (revisores IEEE) | 110.689 | 18 | 236 |
| 2 | revisor-forma + guardiao-consistencia | 133.290 | 32 | 481 |
| | **Total** | **1.303.127** | **300** | **3.731** |

- **Rodada 1:** 744 mil tokens; cerca de 8 min de relógio para os despachos em paralelo, mais a espera
  pelos dois primeiros.
- **Rodada 2:** 469 mil tokens; cerca de 8 min de relógio.
- Os tokens do coordenador (a sessão principal, que montou o resumo real, rodou as análises e
  reescreveu o texto) **não estão incluídos**.

### 4.2 Achados e qualidade

A "precisão" abaixo é o julgamento do coordenador depois de conferir cada item contra o código e os
dados. Não houve avaliação cega por humano.

| Agente (R1) | Achados | Confirmados | Problemas observados |
|---|---:|---:|---|
| guardiao-dados | 30 | 30 | Nenhum. Encontrou tudo que a leitura manual do firmware tinha encontrado, inclusive nas figuras TikZ |
| revisor-citacoes | 10 refs + 12 candidatas + 8 lacunas | 10/10 classificações | O DOI sugerido para o AeroShield (Zenodo) estava errado; foi corrigido na verificação seguinte (`10.1016/j.ifacol.2023.10.264`) |
| guardiao-metodo | 15 | 15 | Sobreposição com orientador e banca (gêmeo digital, pedagogia, determinismo) |
| orientador-rigoroso | 21 | 20 | O primeiro retorno trouxe só um resumo executivo; foi preciso pedir o relatório completo |
| banca-critica | veredito + 12 perguntas + top 5 | útil | Citou precedentes (Quanser Aero) sem verificar; depois se confirmou que existem |
| revisor-forma | ~35 itens em 8 categorias | ~33 | 2 itens de gosto (larguras de figura, babel `brazil`) |
| guardiao-consistencia | 22 | 21 | Sobre o atraso "z⁻⁶ ou z⁻⁷", sugeriu que a fórmula (6) estava certa; o valor real é 7. Faltava ao agente o dado para saber disso |
| requisitos do periódico | 23 itens | 23 | Achou exigências que o plano do autor não tinha: video abstract, resumo em inglês, DOI, CRediT, revisores |

| Agente (R2) | Achados | Confirmados | Problemas observados |
|---|---:|---:|---|
| guardiao-dados | 0 divergências + 3 itens "fora do resumo" | 3/3 procedentes | Nenhum; a lista de cobertura ajudou a confiar no zero |
| guardiao-metodo + orientador | 14 itens da R1 conferidos + 11 novos | 11/11 | **Pegou o vazamento de validação** introduzido pelo coordenador na reescrita |
| banca-critica | veredito + 10 perguntas + top 5 | útil | Sugestões viáveis, separando o que dá para fazer com os dados atuais do que exige ensaio novo |
| forma + consistência | 11 | 8 | 3 falsos positivos: caixas estouradas lidas de um `build.log` antigo |

**Duplicação.** O mesmo problema ("gêmeo digital" para um fluxo unidirecional) apareceu em
5 relatórios da R1. A alegação pedagógica sem avaliação com alunos apareceu em 4. Sem deduplicação,
o relatório consolidado ficou com 368 linhas.

---

## 5. O que o benchmark mostrou

### 5.1 O que funcionou bem

1. **`guardiao-dados` contra um `resumo-real.md` bem feito é muito eficaz.** Ele encontrou 100% das
   divergências na R1 e zero falsos positivos na R2. A instrução de marcar como achado uma
   afirmação específica que o resumo diz "não registrado" (frequência de corte, jitter, custo)
   pegou os números inventados que não tinham contraponto numérico.
2. **A regra "agente só relata, não edita"** manteve as decisões com o coordenador e o autor, e
   deixou as rodadas auditáveis.
3. **A rodada 2 com tabela RESOLVIDO / PARCIAL / PENDENTE** foi o recurso de maior valor por token:
   confirmou as correções e pegou um problema novo, o vazamento de validação, que o próprio
   coordenador tinha criado.
4. **`revisor-citacoes` com busca na web** achou a referência com autoria errada, que nenhum outro
   passo pegaria.
5. **`banca-critica` como corpo editorial** (desk-review + 3 revisores + top 5) produziu um plano
   de ação priorizado e realista.

### 5.2 O que funcionou mal ou exigiu improviso

1. **Não existe etapa para construir o `resumo-real.md`.** O kit supõe que o aluno já tem esse
   arquivo, mas aqui ele teve de ser montado lendo 3 CSVs, 2 scripts, o firmware e um diff do git.
   Foi a etapa de maior impacto de todo o processo.
2. **Slugs fixos de capítulo.** O artigo tinha 5 seções e passou a ter 7, com nomes livres; as
   regras do checklist (estado por capítulo) não se aplicam como estão.
3. **O `revisor-forma` é ABNT e português.** Para inglês e IEEE, a persona precisou ser reescrita no
   prompt (tiques de IA em inglês, título das tabelas, `\mathrm` em subscritos, pontuação de
   equações).
4. **O checklist institucional é estático.** O equivalente para periódico precisa de pesquisa na
   web e fonte para cada item; foi preciso criar um agente extra.
5. **O `revisor-citacoes` não exige DOI nem confere o tipo BibTeX.** Entradas `@article` usadas para
   TCC e capítulo de livro fazem o veículo sumir no PDF do IEEEtran; isso só apareceu porque foi
   pedido explicitamente.
6. **O `guardiao-metodo` não tem checklist para modelagem e aprendizado de máquina.** Vazamento de
   validação, seleção no conjunto de teste e comparações injustas só apareceram na R2, e porque o
   prompt de adaptação citou esses riscos.
7. **Ordem sequencial dos dois primeiros agentes.** Esperar `guardiao-dados` e `revisor-citacoes`
   antes dos outros não trouxe benefício: os agentes não leem o relatório uns dos outros. A ordem só
   importa na consolidação.
8. **Retorno incompleto.** O `orientador-rigoroso` devolveu só um resumo, e o relatório completo
   precisou ser pedido de novo. O kit depende de o agente devolver o texto integral.
9. **Consolidação manual.** Os relatórios chegaram como mensagem e tiveram de ser copiados para
   arquivos. Se cada agente gravasse o próprio relatório bruto, a consolidação seria mecânica.
10. **Nenhum agente olha o PDF compilado.** Rótulos sobrepostos em TikZ, equações estourando a
    coluna e DOIs que não aparecem nas referências (o `IEEEtran.bst` ignora o campo `doi`) foram
    achados pelo coordenador renderizando as páginas.
11. **Artefato velho.** O `revisor-forma` da R2 leu um `build.log` desatualizado e relatou 3 caixas
    estouradas que já não existiam.

### 5.3 O que só apareceu ao executar código

Nenhum agente do kit encontraria os itens abaixo, porque eles exigem rodar scripts ou ler código com
uma pergunta específica. Foram eles que mudaram a contribuição do artigo:

| Descoberta | Como foi feita | Efeito no artigo |
|---|---|---|
| O sinal chamado de "PRBS" é uma onda quadrada com período sorteado, e `random(5)` pode indexar fora de um vetor de 4 posições | Leitura de `referencia.cpp` | Descrição correta da excitação e nota de rodapé |
| Um atraso de entrada de 7–12 amostras explica a maior parte do erro do ARX de 2ª ordem (51,35% → 78,98%) | Varredura de (na, nb, nk) em script novo | **Virou o resultado central** |
| O atraso de 7 amostras da função de transferência publicada existe fisicamente; o erro foi estimar sem atraso e simular com ele | Reestimação com nk = 7 (86,49%) | Explicação do "bug" original |
| Os ensaios de 2023 rodaram com a lei D antiga (e·Δθ·Ts) | Reconstrução do termo integral a partir dos logs (resíduo 3×10⁻⁴ contra 2–3) | Declaração exata do controlador testado |
| O termo D antigo freia a subida e reforça a descida | Análise de sinal + pico de −0,035 V medido nos logs | Explicação alternativa da assimetria |
| O comando nunca saiu de 0–3,3 V, então o bug de saturação não afetou os dados | Mínimo e máximo do sinal logado | Um confundidor a menos |
| Os modelos de 2ª ordem não têm par de polos complexos | Polos convertidos para s | Ponte entre o modelo físico e os modelos identificados |

**Conclusão:** para trabalhos empíricos, a verificação por texto (agentes) precisa ser precedida de
uma **reprodução** (rodar os scripts, conferir versões do código, gerar o resumo com procedência).

### 5.4 Erros do coordenador

1. **Vazamento de validação.** A primeira versão da reescrita escolheu nk olhando o segmento de
   validação. A R2 pegou; a seleção foi refeita com uma janela separada e os números mudaram pouco
   (79,42% → 78,98%; 86,49% → 86,20%).
2. **Contagem errada.** O coordenador escreveu "4006 linhas" no resumo real (são 4007); o erro foi
   pego por uma asserção no próprio script.
3. **Comando git destrutivo por engano.** Um comando composto incluiu `git rm --cached -r .` na raiz
   do repositório. Os arquivos em disco não foram afetados e não houve commit; o índice foi
   restaurado com `git reset`. Isso motiva uma regra de segurança para skills que editam arquivos
   (proposta, seção 7).

---

## 6. Resultado no artigo

| Aspecto | Antes | Depois |
|---|---|---|
| Idioma | Português, com título e resumo em português (não conforme) | Inglês completo |
| Estrutura | 5 seções, sem trabalhos relacionados nem limitações | 7 seções + disponibilidade de dados + biografias |
| Referências | 10 (1 com autoria errada, nenhum DOI) | 23 citadas, todas verificadas, com DOI/ISBN impresso |
| Resultado central | "Ordem 10 é necessária para modos aerodinâmicos" (sem evidência) | "Um atraso de 7–12 amostras explica a maior parte do erro" (seleção sem vazamento) |
| Malha fechada | Tabela com valores inexistentes | Medianas e quartis por ensaio, lei do PID confirmada pelos logs |
| Visualização 3D | "Gêmeo digital" | "Sombra digital" (Kritzinger et al.) |
| Alegações sem medição | Determinismo, jitter, eficácia pedagógica, baixo custo | Removidas ou movidas para limitações |
| Figuras | 5 (2 PNG antigos de validação) | 8 (6 geradas por script versionado) |
| Reprodutibilidade | Nenhuma menção | Repositório, arquivos e script citados |

Pendências do autor (marcadas em vermelho no PDF): financiamento, divulgação de uso de IA, a frase
de diferenciação nos trabalhos relacionados, dimensões e custo do protótipo, fotos e biografias,
revisores sugeridos, graphical abstract e video abstract.

---

## 7. Lições para o kit

As recomendações abaixo estão detalhadas em
[`docs/propostas/2026-09-17-fluxo-artigos.md`](../propostas/2026-09-17-fluxo-artigos.md).

1. **Criar uma etapa de reprodução de dados** que gere o `resumo-real.md` com a procedência de cada
   número (arquivo, script, commit) e rode os scripts do projeto.
2. **Aceitar seções de nome livre** e um estado por seção, não só os 5 capítulos fixos.
3. **Criar perfis de estilo para o `revisor-forma`** (ABNT-PT, IEEE-EN, APA-EN…) e uma lista de
   tiques de IA por idioma.
4. **Trocar o checklist institucional fixo** por uma skill de requisitos do veículo, com fonte (URL)
   por item.
5. **`revisor-citacoes`:** DOI obrigatório (conferido na Crossref), tipo de entrada BibTeX e se a
   fonte sustenta a frase citada.
6. **`guardiao-metodo`:** checklist de vazamento, seleção no conjunto de teste, comparação justa e
   múltiplas comparações.
7. **Criar um agente de diagramação** que compile, conte páginas, leia o log **da compilação atual**
   e renderize as páginas.
8. **Rodada N com delta:** cada rodada lê a anterior e marca RESOLVIDO / PARCIAL / PENDENTE.
9. **Despachar os agentes em paralelo** e aplicar a ordem (dados e citações primeiro) só na
   consolidação.
10. **Cada agente grava o próprio relatório bruto** em arquivo; a skill deduplica os achados
    repetidos entre agentes.
11. **Checkpoint de decisões do autor** entre a auditoria e a reescrita.
12. **Regras de segurança:** backup em `versoes/` antes de reescrever; nunca encadear comandos git
    nas skills; nenhum comando git além de leitura.
13. **Evals novos** a partir deste caso (tabela inventada, referência com autoria errada, vazamento,
    resumo fora do idioma exigido, log velho).

---

## 8. Limitações deste benchmark

- **Um único caso (n = 1)**, com um único coordenador (o modelo que também reescreveu o texto). Não
  houve comparação com revisão humana nem avaliação cega da qualidade dos achados.
- **Precisão avaliada pelo próprio coordenador**, contra o código e os dados. Itens de julgamento
  (argumento, forma) não têm gabarito.
- **O risco de rejeição é simulado.** Só a submissão real mede a aceitação.
- **Personas lidas por arquivo.** Os agentes não rodaram como agentes instalados do plugin; o
  comportamento pode diferir um pouco do plugin instalado (ferramentas, contexto).
- **Custos parciais.** Os números são os reportados pelas notificações dos subagentes; o consumo do
  coordenador não foi medido.

---

## 9. Artefatos

No projeto avaliado (`Projeto_Tcc_Oseias_Oficial/`):

- `artigo_ieee_latam/tcc-kit/`: `config.md`, `metodologia.md`, `dados/resumo-real.md`,
  `checklist.md`, `historico.md`;
- `artigo_ieee_latam/tcc-kit/relatorios/artigo-completo-2026-09-17.md` (rodada 1) e
  `artigo-en-rodada2-2026-09-17.md` (rodada 2), com os relatórios brutos em `_brutos/` e
  `_brutos_r2/`;
- `artigo_ieee_latam_en/`: artigo reescrito, `referencias.bib`, `figuras/*.pdf`,
  `submissao/letter_to_editor.tex` e a versão anterior em `versoes/v1-2026-09-15/`;
- `materiais_complementares/Identificacao_de_Sistemas/identificacao_aeropendulo/ident_up/analise_complementar.py`
  (353 linhas): análises novas e figuras.
