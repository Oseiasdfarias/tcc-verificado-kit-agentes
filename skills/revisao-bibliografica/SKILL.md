---
name: revisao-bibliografica
description: Use quando o aluno pedir pra buscar/levantar referências sobre um tema ("busca referências sobre X", "levanta bibliografia sobre Y"), ou quando outra parte do kit (ex: revisor-citacoes) sugerir e o aluno confirmar que quer buscar uma referência nova pra preencher uma lacuna específica.
---

# Revisão Bibliográfica — busca, valida, baixa e indexa referências reais

Esta skill busca artigos acadêmicos reais sobre um tema, deixa o aluno confirmar quais entram, baixa
o PDF quando possível, converte pra Markdown, e mantém `tcc/referencias/index.yaml` atualizado —
a base que a escrita do TCC consulta pra nunca inventar referência.

**Princípio inegociável**: você nunca adiciona uma referência à base sem o aluno confirmar aquele
artigo especificamente. Automatize busca, download e conversão — nunca a decisão de que referência
entra no trabalho do aluno.

## Quando usar

- Aluno pede diretamente: "busca referências sobre churn de clientes", "levanta bibliografia sobre
  adesão a tratamento crônico".
- Outra parte do kit (o agente `revisor-citacoes`) detecta uma afirmação sem sustentação ou uma citação
  sem correspondência na base local, sugere rodar esta skill pra aquela lacuna específica, e o aluno
  confirma que quer buscar.

Se o aluno não confirmou explicitamente que quer buscar, não rode esta skill — só sugira.

## Passo 1 — Busca

Determine o termo de busca: o tema que o aluno passou diretamente, ou a lacuna específica descrita por
quem te acionou (ex: "precisa de referência sobre custo de troca de operadora em contratos de
assinatura").

Busque primeiro na Semantic Scholar API via WebFetch:

```
https://api.semanticscholar.org/graph/v1/paper/search?query=<termo codificado em URL>&fields=title,authors,year,venue,externalIds,abstract,openAccessPdf&limit=10
```

A resposta é JSON com uma lista `data`, cada item com `title`, `authors` (lista de `{name}`), `year`,
`venue`, `externalIds` (contém `DOI` quando existe), `abstract`, e `openAccessPdf` (contém `url` quando
existe PDF de acesso aberto — pode ser `null`).

Se a resposta vier vazia, ou com menos de 3 resultados claramente relevantes ao termo buscado, faça uma
busca de fallback com WebSearch focada em fontes brasileiras, por exemplo:
`<termo> site:scielo.br` e `<termo> site:periodicos.capes.gov.br`. Extraia manualmente título, autores,
ano e link de cada resultado relevante encontrado assim.

Se, mesmo com o fallback, não encontrar nada relevante: informe o aluno claramente ("não encontrei
referência relevante pra esse termo") e sugira tentar palavras-chave diferentes. Não invente resultado,
não devolva silêncio.

## Passo 2 — Apresentar candidatos e confirmar

Apresente os candidatos encontrados (API + fallback, combinados) numa lista numerada, cada um com:
título, autores, ano, veículo, um resumo de 1-2 linhas a partir do `abstract`, e se tem PDF de acesso
aberto disponível (sim/não).

Pergunte ao aluno quais entram. Aceite respostas como "1, 3 e 5", "todos", "nenhum, busca de novo com
outro termo". Só os artigos confirmados seguem pro Passo 3 — os outros são descartados.

## Passo 3 — Checar duplicata

Antes de processar cada artigo confirmado, leia `tcc/referencias/index.yaml` (se existir) e confira se
já existe uma entrada com o mesmo DOI (ou, se DOI ausente em algum dos dois lados, mesmo título
normalizado — minúsculo, sem pontuação). Se já existir, pule esse artigo e avise o aluno que ele já
está na base.

## Passo 4 — Download

Pra cada artigo confirmado e não-duplicado: gere uma `chave` no padrão `sobrenomeAno` (mesmo padrão da
Aula 2.11 do curso pro `.bib` — ex: `silva2021`; se colidir com uma chave já existente, acrescente
`b`, `c`, etc: `silva2021b`).

Se o artigo tem `openAccessPdf.url`: tente baixar com
`curl -sL -o tcc/referencias/pdfs/<chave>.pdf "<url>"`. Confirme que o arquivo baixado é um PDF válido
(comece checando que o arquivo existe e tem tamanho razoável, acima de alguns KB — um HTML de página de
erro salvo com extensão `.pdf` é um sinal de falha disfarçada de sucesso).

Se não tem `openAccessPdf.url`, ou o download falhar por qualquer motivo: não trate como erro fatal —
acrescente uma entrada em `tcc/referencias/baixar-manualmente.md` nesse formato:

```markdown
## <chave>

**Título:** <título>
**Autores:** <autores>
**Ano:** <ano>
**Link:** <o melhor link que você tem — página do artigo, DOI, ou o que encontrou na busca>

Baixe o PDF manualmente e salve como `tcc/referencias/pdfs/<chave>.pdf`.
```

## Passo 5 — Conversão

Pra cada PDF presente em `tcc/referencias/pdfs/` que ainda não tem entrada `verificado` ou
`pendente-conversao` no índice (isso cobre tanto os baixados automaticamente no Passo 4 quanto os que o
aluno colocou manualmente depois de uma rodada anterior), rode:

```bash
uv run --with marker-pdf <caminho do plugin>/scripts/pdf_to_md.py tcc/referencias/pdfs/<chave>.pdf tcc/referencias/md/<chave>.md
```

(O caminho exato do plugin instalado pode variar — procure o arquivo `scripts/pdf_to_md.py` relativo à
raiz deste plugin. Se não conseguir localizar automaticamente, informe o aluno e pare, não invente um
caminho.)

Leia o código de saída do comando:
- **0**: conversão ok — status vira `verificado`.
- **2**: saída curta/vazia demais — status vira `pendente-conversao`, avise o aluno explicitamente
  (provável PDF escaneado sem texto, ou arquivo corrompido) em vez de adicionar como se estivesse
  pronto.
- **1**: arquivo de entrada não encontrado — não deveria acontecer aqui (acabamos de confirmar o
  arquivo no Passo 4), trate como bug e reporte ao aluno.

## Passo 6 — Indexar

Pra cada artigo processado (status `verificado` ou `pendente-conversao`), adicione (ou crie, se ainda
não existir) uma entrada em `tcc/referencias/index.yaml`:

```yaml
referencias:
  - chave: <chave>
    titulo: "<título completo>"
    autores: ["<Sobrenome, N.>", "..."]
    ano: <ano>
    veiculo: "<periódico/veículo>"
    doi: "<DOI ou omitir se não existir>"
    status: verificado  # ou pendente-conversao
    arquivo_pdf: pdfs/<chave>.pdf
    arquivo_md: md/<chave>.md  # omitir/null se status for pendente-conversao e a conversao nao gerou arquivo usavel
    resumo: "<2-4 linhas resumindo o achado/argumento principal, escritas por você a partir do conteúdo de md/<chave>.md>"
    tema_relacionado: "<o termo de busca ou a lacuna que originou essa busca>"
    adicionado_em: "<data de hoje, AAAA-MM-DD>"
```

Artigos que foram pro `baixar-manualmente.md` (Passo 4) **não** entram no índice ainda — só entram
depois que o aluno baixar o PDF manualmente e essa skill rodar de novo (o Passo 5 detecta o PDF novo na
pasta na próxima execução).

## Passo 7 — Resumo final

Informe ao aluno, em 2-3 frases: quantas referências foram adicionadas com sucesso (`verificado`),
quantas ficaram pendentes de conversão, e quantas foram pra `baixar-manualmente.md` aguardando download
manual.
