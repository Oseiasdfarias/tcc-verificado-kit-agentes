---
name: estado-tcc
description: Use quando o aluno pedir um panorama ou relatório do andamento do TCC -- "como está meu TCC?", "me dá um resumo do estado do projeto", "gera um relatório do andamento pro meu orientador", "o que eu já fiz até agora?". Monta o panorama completo (capítulos, revisões, pontos bloqueantes, o que ficou desatualizado depois de uma edição) a partir dos registros do kit, sem reler o texto dos capítulos, e salva em arquivo. Não é para "por onde eu continuo?" ou "o que falta no meu TCC?": isso é a skill iniciar-tcc, que sugere um próximo passo.
---

# Estado do TCC — panorama a partir dos registros do kit

Esta skill descreve o projeto, não decide nada. Ela monta um panorama a partir dos arquivos que as
outras skills do kit já mantêm (checklist, histórico, relatórios e o registro de versões) e **nunca
abre o texto dos capítulos**. É isso que mantém a consulta barata, mesmo num TCC completo.

O único arquivo que ela escreve é o próprio relatório. Não edita `tcc-kit/checklist.md`,
`tcc-kit/historico.md` nem `tcc-kit/.estado.json`, não registra nada no histórico e não despacha
agentes.

## Passo 1 — Verificar versões

Rode:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" verificar
```

O caminho do plugin segue a mesma regra de `revisao-bibliografica`: procure
`scripts/estado_projeto.py` relativo à raiz deste plugin, e não invente um caminho. Nunca leia
`tcc-kit/.estado.json` diretamente: use só a saída do comando.

A saída é uma tabela com `etapa`, `data`, `estado` e `alterados`. As etapas são:

| Etapa | Significa |
|---|---|
| `escrita:<slug>` | Capítulo escrito por `escrever-capitulo`; entradas: plano e resumo de dados real |
| `revisao:<slug>` | Capítulo auditado por `revisar-capitulo`; entradas: capítulo, dados, metodologia |
| `auditoria-completa` | Auditoria do TCC inteiro; entradas: os 5 capítulos |
| `defesa` | Apresentação de defesa gerada; entradas: os 5 capítulos |
| `reproducao` | Resumo de dados montado por `reproduzir-dados`; entradas: dados e scripts confirmados |

Estados: `atual`, `desatualizada` (algum arquivo em `alterados` mudou, ou passou a existir depois do
registro) e `entrada-removida` (algum arquivo em `alterados` sumiu).

- **`sem registros`**: normal em projeto criado antes desta versão do kit. Siga sem afirmar nada sobre
  desatualização.
- **Código 2** (`tcc-kit/.estado.json` ilegível): siga sem a verificação e diga no relatório que o
  arquivo de registro de versões está ilegível. Não apague nem corrija o arquivo.
- **Comando falhou por outro motivo** (`uv` ausente, script não encontrado): siga sem a verificação e
  diga no relatório que a verificação de versões não rodou.

## Passo 2 — Ler o checklist

Leia `tcc-kit/checklist.md`. Ele dá o estado de cada etapa do ciclo (configuração, template, tema,
referências, metodologia, os 5 capítulos, auditoria completa, apresentação de defesa).

**Se não existir, ou não bater com o formato esperado:** não crie nem corrija o arquivo (esta skill
não é dona dele). Faça uma detecção mínima **só por existência**, com Glob, sem abrir o conteúdo dos
capítulos: `tcc-kit/config.md`, `tcc-kit/template.md`, `tcc-kit/tema.md`, `tcc-kit/metodologia.md`,
`tcc-kit/capitulos/*/plano.md`, `tcc/capitulos/*.tex`, `tcc-kit/relatorios/*.md` e
`tcc/apresentacao-defesa.tex`. Nesse modo, um `.tex` que existe aparece como "arquivo existe", sem
afirmar se tem conteúdo real. Diga no relatório que o checklist não existe (ou está fora do formato) e
que a situação foi inferida só pelos arquivos presentes.

## Passo 3 — Ler só o fim do histórico

Se `tcc-kit/historico.md` existir, localize os cabeçalhos das entradas (linhas que começam com `## `)
com Grep e leia **só as 5 entradas mais recentes** (Read com offset a partir do 5º cabeçalho contado do
fim). Nunca leia o arquivo inteiro.

## Passo 4 — Pontos bloqueantes, só a seção que importa

Para cada capítulo com pelo menos um `tcc-kit/relatorios/<slug>-*.md`, pegue o mais recente (maior data
no nome do arquivo). Nele, localize com Grep a linha `## Achados bloqueantes` e o próximo cabeçalho
`## `, e leia **só esse trecho**. Registre a data do relatório (do nome do arquivo) e os itens
bloqueantes, um por linha, resumidos em poucas palavras.

Para a auditoria completa, não leia o relatório: use a data do arquivo
`tcc-kit/relatorios/auditoria-completa-*.md` mais recente e, se a entrada dela estiver entre as lidas no
Passo 3, o número de achados que ela registra.

## Passo 5 — Identificação e contagens

- `tcc-kit/config.md`: campos **Aluno**, **Orientador(a)**, **Curso/Programa**, **Universidade**,
  **Ano previsto de conclusão** (arquivo pequeno, pode ler inteiro).
- `tcc-kit/tema.md`: campo **Tema**.
- Referências verificadas: conte com Grep as linhas `status: verificado` em
  `tcc-kit/referencias/index.yaml`.
- Metodologia: leia com Grep só a linha do campo `Status` de `tcc-kit/metodologia.md`.
- Resumo de dados: se existe etapa `reproducao` no Passo 1, "reproduzido em <data>"; senão, se
  `tcc/dados/resumo-real.md` existe (Glob), "montado à mão"; senão, "não existe".

Campo ou arquivo ausente vira "não informado" no relatório. Não invente nenhum desses valores.

## Passo 6 — Cruzar e escrever o relatório

**Nunca abra `tcc/capitulos/*.tex`.** Tudo no relatório vem dos Passos 1 a 5.

Cruze o checklist com a saída do Passo 1:

- `revisao:<slug>` **desatualizada** com o capítulo em `alterados`: a situação do capítulo ganha
  "**alterado depois da revisão**". Se o que mudou foi o resumo de dados ou a metodologia, escreva
  "**dados (ou metodologia) alterados depois da revisão**".
- `escrita:<slug>` **desatualizada** com o resumo de dados em `alterados`: entra em "Atenção" como
  "o capítulo <nome> foi escrito com dados que mudaram depois: confira se os números ainda batem". Se
  foi o plano que mudou: "o plano do capítulo <nome> mudou depois da escrita".
- `auditoria-completa` ou `defesa` **desatualizada**: marque "desatualizada" na linha correspondente da
  visão geral e liste em "Atenção" quais capítulos mudaram (ou passaram a existir) depois.
- `reproducao` **desatualizada**: entra em "Atenção" como "os dados ou scripts mudaram depois do
  resumo de dados (<arquivos>): refaça a reprodução antes de confiar nos números". Na visão geral, a
  linha "Resumo de dados" mostra a data da reprodução e "desatualizado".
- `entrada-removida`: entra em "Atenção" dizendo qual arquivo sumiu desde o registro.
- Capítulo com relatório de revisão, mas sem etapa `revisao:<slug>` na saída do Passo 1 (revisão
  anterior a esta versão do kit): mostre a data do relatório, sem afirmar se está atual ou não.

Salve em `tcc-kit/estado/estado-<data de hoje, AAAA-MM-DD>.md` (sobrescreva se já existir um do mesmo
dia), neste formato:

```markdown
# Estado do TCC — <data>

**Tema:** <tema>
**Aluno:** <nome> · **Orientador(a):** <nome> · **Curso:** <curso> · **Universidade:** <universidade> · **Conclusão prevista:** <ano>

## Visão geral
| Etapa | Situação |
|---|---|
| Configuração institucional | <feita / pendente> |
| Template | <escolhido / pendente> |
| Tema | <definido / pendente> |
| Referências verificadas | <N> |
| Metodologia | <estado> |
| Resumo de dados | <reproduzido em <data>[, desatualizado] / montado à mão / não existe> |
| Auditoria do TCC completo | <nunca rodada / rodada em <data>[, desatualizada]> |
| Apresentação de defesa | <nunca gerada / gerada em <data>[, desatualizada]> |

## Capítulos
| Capítulo | Situação | Última revisão | Pontos bloqueantes em aberto |
|---|---|---|---|
| Introdução | <situação> | <data ou —> | <N ou —> |
| Referencial teórico | … | … | … |
| Metodologia | … | … | … |
| Resultados | … | … | … |
| Discussão/Considerações finais | … | … | … |

<Para cada capítulo com ponto bloqueante: um subtítulo "### <capítulo>" com os itens, um por linha.>

## Atenção
<Só inclua esta seção se houver algum caso do cruzamento acima. Um item por linha.>

## Atividade recente
<as até 5 entradas mais recentes do histórico, uma linha cada: data, o que foi feito>

## Pendências, na ordem do ciclo
<Etapas não concluídas ou desatualizadas, na ordem: configuração, template, tema, referências,
metodologia, capítulos (na ordem da tabela), auditoria completa, apresentação. Sem recomendar qual
fazer primeiro.>

---
Gerado a partir dos registros do kit, sem reler o texto dos capítulos.
<Se o Passo 1 respondeu "sem registros", ou se algum capítulo tem revisão sem registro de versão,
acrescente: "Revisões feitas antes da versão 1.10 do kit não têm registro de versão, então não dá pra
saber se o capítulo mudou depois delas. Para passar a acompanhar um capítulo, rode a revisão dele de
novo.">
<Se o checklist não existia, ou a verificação de versões não rodou, diga aqui.>
```

**Escreva para o aluno e para o orientador ao mesmo tempo.** O orientador não conhece o kit. Não use
no relatório os termos "hash", "etapa", "slug", "registro de versão" (exceto no rodapé), nem nomes de
skill ou de agente. Nome de capítulo sempre por extenso.

## Passo 7 — Resumo na conversa

Mostre ao aluno o caminho do relatório e 3 a 5 linhas: quantos capítulos em cada situação, quantos
pontos bloqueantes em aberto e, se houver, os itens de "Atenção". Termine dizendo que, para decidir o
próximo passo, ele pode perguntar "por onde eu continuo?".

## Regras

- **Nunca registre versão.** Esta skill não roda `registrar` em hipótese nenhuma, nem para "começar a
  acompanhar" um capítulo antigo. Registrar a versão atual de um capítulo que não foi revisado de novo
  declararia uma revisão que não aconteceu.
- **Não invente situação.** Se um dado não está nos registros, o relatório diz que não está.
- **Não recomende.** Pendências são listadas na ordem do ciclo; a escolha do que fazer é do aluno.
