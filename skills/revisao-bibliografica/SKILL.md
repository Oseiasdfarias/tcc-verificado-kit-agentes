---
name: revisao-bibliografica
description: Use quando o aluno pedir pra buscar/levantar referências sobre um tema ("busca referências sobre X", "levanta bibliografia sobre Y"), ou quando outra parte do kit (ex: revisor-citacoes) sugerir e o aluno confirmar que quer buscar uma referência nova pra preencher uma lacuna específica.
---

# Revisão Bibliográfica — busca, valida, baixa e indexa referências reais

Esta skill busca artigos acadêmicos reais sobre um tema, deixa o aluno confirmar quais entram, baixa
o PDF quando possível, converte pra Markdown, e mantém `tcc-kit/referencias/index.yaml` atualizado —
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

Se o aluno não especificou nenhum termo (ex: pediu só "busca referências sobre meu tema" direto, sem
passar por `iniciar-tcc` ou `escolher-tema` na conversa) e `tcc-kit/tema.md` existir, leia esse arquivo
e use os "Termos de busca sugeridos" de lá como ponto de partida — o mesmo termo que `iniciar-tcc` já
passaria adiante, disponível também quando esta skill é invocada direto. Deixe claro ao aluno quais
termos você está usando e que ele pode pedir outros.

Busque primeiro na Semantic Scholar API via WebFetch:

```
https://api.semanticscholar.org/graph/v1/paper/search?query=<termo codificado em URL>&fields=title,authors,year,venue,externalIds,abstract,openAccessPdf&limit=10
```

A resposta é JSON com uma lista `data`, cada item com `title`, `authors` (lista de `{name}`), `year`,
`venue`, `externalIds` (contém `DOI` quando existe), `abstract`, e `openAccessPdf` (contém `url` quando
existe PDF de acesso aberto — pode ser `null`).

Se a chamada em si falhar (erro de rede, HTTP 429/5xx, timeout, ou qualquer resposta que não seja o JSON
esperado), tente de novo no máximo 2 vezes, com um intervalo curto entre tentativas. Se ainda falhar
depois disso, não insista mais — caia direto pro fallback de WebSearch abaixo, do mesmo jeito que se a
API tivesse respondido vazia. A Semantic Scholar sem chave de API tem rate limit agressivo e pode ficar
indisponível por vários minutos; insistir além dessas tentativas custa tempo do aluno sem necessidade.

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

Antes de processar cada artigo confirmado, leia `tcc-kit/referencias/index.yaml` (se existir) e confira se
já existe uma entrada com o mesmo DOI (ou, se DOI ausente em algum dos dois lados, mesmo título
normalizado — minúsculo, sem pontuação). Se já existir, pule esse artigo e avise o aluno que ele já
está na base — isso vale também pra uma entrada com status `pendente-manual`: ela já está no índice
desde o Passo 4 (mesmo sem PDF ainda), então uma busca repetida não deve tratá-la como candidato novo.

## Passo 4 — Download

Antes de baixar qualquer coisa, garanta que `tcc-kit/referencias/pdfs/` e `tcc-kit/referencias/md/` existem —
rode `mkdir -p tcc-kit/referencias/pdfs tcc-kit/referencias/md` uma vez no início deste passo. Sem isso, o
`curl` e a conversão do Passo 5 falham num projeto novo, e essa falha é fácil de confundir com "o site
bloqueou o download" quando a causa real é só a pasta não existir.

Pra cada artigo confirmado e não-duplicado: gere uma `chave` no padrão `sobrenomeAno` (mesmo padrão da
Aula 2.11 do curso pro `.bib` — ex: `silva2021`; se colidir com uma chave já existente no índice —
`verificado`, `pendente-conversao` ou `pendente-manual` — **ou com uma chave que você já atribuiu a
outro artigo nesta mesma execução** (mantenha uma lista das chaves já usadas nesta rodada: downloads
bem-sucedidos só são gravados em `index.yaml` no Passo 6, no final do lote, então dois artigos
confirmados no mesmo lote — ex: dois autores "Silva, 2021" diferentes — podem colidir sem que o índice
ainda saiba disso) — acrescente `b`, `c`, etc: `silva2021b`).

Se o artigo tem `openAccessPdf.url`: tente baixar com
`curl -sL -o "tcc-kit/referencias/pdfs/<chave>.pdf" "<url>"`. Confirme que o arquivo baixado é um PDF válido —
não basta checar tamanho: um HTML de página de erro ou de desafio anti-bot (Cloudflare e afins) salvo
com extensão `.pdf` é um sinal de falha disfarçada de sucesso, e uma página de desafio maior que "alguns
KB" passaria despercebida por uma checagem só de tamanho. Confirme o conteúdo de verdade — rode
`file "tcc-kit/referencias/pdfs/<chave>.pdf"` e confira que o retorno começa com "PDF document" (ou leia os
primeiros bytes do arquivo e confira que começam com `%PDF-`) — além de existir e ter tamanho razoável
(acima de alguns KB).

Se o download deu certo e o PDF é válido, siga direto pro Passo 5 — não crie entrada em
`baixar-manualmente.md` nem em `index.yaml` com `pendente-manual` pra esse artigo.

Se não tem `openAccessPdf.url`, ou o download falhar por qualquer motivo (incluindo o caso de o arquivo
baixado não passar na checagem de PDF válido acima): não trate como erro fatal.

Se o motivo específico foi o arquivo baixado não passar na checagem de PDF válido, **apague-o primeiro**
(`rm "tcc-kit/referencias/pdfs/<chave>.pdf"`) antes de seguir: deixá-lo na pasta faz o Passo 5 tentar
convertê-lo na próxima varredura e sobrescrever o status `pendente-manual` (criado logo abaixo) com
`pendente-conversao`, quebrando o fluxo de download manual — o aluno baixaria o PDF de verdade depois e
ele seria ignorado pra sempre, porque `pendente-conversao` fica fora do critério de varredura do Passo 5.

Faça as duas coisas abaixo pra esse artigo:

1. Acrescente uma entrada em `tcc-kit/referencias/baixar-manualmente.md` nesse formato:

```markdown
## <chave>

**Título:** <título>
**Autores:** <autores>
**Ano:** <ano>
**Link:** <o melhor link que você tem — página do artigo, DOI, ou o que encontrou na busca>

Baixe o PDF manualmente e salve como `tcc-kit/referencias/pdfs/<chave>.pdf`.
```

2. Adicione (ou crie, se `tcc-kit/referencias/index.yaml` ainda não existir) uma entrada nesse arquivo pra
   esse artigo, imediatamente, com `status: pendente-manual` — não espere o aluno baixar o PDF pra
   indexar (formato completo no Passo 6). Omita (ou deixe `null`) `arquivo_pdf` e `arquivo_md`; pra
   `resumo`, use o `abstract` da busca como resumo provisório se tiver disponível, deixando claro que
   ainda não é baseado no texto completo — se não tiver abstract, omita `resumo` por enquanto. Isso é o
   que permite o Passo 3 reconhecer esse artigo como já-tratado numa busca futura, mesmo antes do PDF
   chegar.

## Passo 5 — Conversão

Pra cada PDF presente em `tcc-kit/referencias/pdfs/` cuja `chave` correspondente ainda não tem status
`verificado` nem `pendente-conversao` no índice — isso cobre os baixados automaticamente no Passo 4, os
que o aluno colocou manualmente depois de uma rodada anterior (nesse caso a entrada já existe no índice
com status `pendente-manual`, criada no Passo 4), **e também um PDF que esteja na pasta sem nenhuma
entrada correspondente no índice** (órfão — ex: sobra de uma execução interrompida, ou um arquivo que o
aluno colocou lá por conta própria sem passar pelo Passo 1/2 desta skill; trate-o como o caso de
inserção manual descrito no Passo 6) — rode:

```bash
uv run --with marker-pdf "<caminho do plugin>/scripts/pdf_to_md.py" "tcc-kit/referencias/pdfs/<chave>.pdf" "tcc-kit/referencias/md/<chave>.md"
```

(O caminho exato do plugin instalado pode variar — procure o arquivo `scripts/pdf_to_md.py` relativo à
raiz deste plugin. Se não conseguir localizar automaticamente, informe o aluno e pare, não invente um
caminho.)

Leia o código de saída do comando:
- **0**: conversão ok (com reconhecimento de fórmula/OCR, quando o PDF precisou) — status vira
  `verificado`.
- **3**: conversão ok, mas sem reconhecimento de fórmula/OCR — o binário `llama-server` (usado pelo
  `marker` pra isso) não está instalado nesta máquina. Status ainda vira `verificado` (o texto restante
  do artigo saiu normal, é real e usável), mas registre no `resumo` que fórmulas/equações desse artigo
  podem não ter sido capturadas corretamente, e avise o aluno no resumo final do Passo 7 — sobretudo se
  o tema tiver cara de precisar de fórmula (áreas exatas/engenharia). Não é preciso pedir pro aluno
  instalar nada a menos que ele pergunte ou o tema realmente dependa de fórmula.
- **2**: saída curta/vazia demais — status vira `pendente-conversao`, avise o aluno explicitamente
  (provável PDF escaneado sem texto, ou arquivo corrompido) em vez de adicionar como se estivesse
  pronto.
- **1**: arquivo de entrada não encontrado, ou argumentos malformados — não presuma que é impossível
  (por exemplo, um caminho com espaço não citado corretamente quebraria os argumentos): reporte ao
  aluno o comando exato que você rodou, pra facilitar o diagnóstico.
- **127** (ou mensagem de "comando não encontrado"): o próprio `uv` não está instalado — isso é
  diferente dos códigos acima, que vêm do script rodando. Avise o aluno claramente que precisa instalar
  o `uv` (aponte para https://docs.astral.sh/uv/getting-started/installation/) e pare — não tente outro
  método de conversão.

## Passo 6 — Indexar

Pra cada artigo processado no Passo 5 (status `verificado` ou `pendente-conversao`): se já existe uma
entrada em `tcc-kit/referencias/index.yaml` com essa `chave` — caso normal, criada no Passo 4 com status
`pendente-manual` quando o download automático falhou — **atualize essa entrada no lugar** (troque o
`status`, preencha `arquivo_pdf`/`arquivo_md`, e reescreva `resumo` a partir do conteúdo real de
`md/<chave>.md` agora que ele existe). Só crie uma entrada nova se essa `chave` ainda não existir no
índice — dois casos possíveis:
- caso raro: o download automático do Passo 4 deu certo de primeira, sem nunca passar por
  `pendente-manual`;
- PDF órfão detectado pelo Passo 5 (sem nenhuma entrada prévia no índice, colocado na pasta fora do
  fluxo desta skill): trate como uma inserção manual comum — gere uma `chave` a partir do nome do
  arquivo (use o padrão `sobrenomeAno` se der pra inferir do conteúdo convertido, senão use o nome do
  arquivo sem a extensão) e preencha os demais campos (`titulo`, `autores`, `ano`, `veiculo`) a partir
  do que der pra inferir do texto em `md/<chave>.md`. Como esses metadados não vieram de uma busca que
  o aluno confirmou no Passo 2, deixe isso explícito no `resumo` (algo como "metadados inferidos
  automaticamente a partir do PDF — confira antes de usar") e avise o aluno no resumo final do Passo 7
  pra ele conferir essa entrada.

```yaml
referencias:
  - chave: <chave>
    titulo: "<título completo>"
    autores: ["<Sobrenome, N.>", "..."]
    ano: <ano>
    veiculo: "<periódico/veículo>"
    doi: "<DOI ou omitir se não existir>"
    status: verificado  # ou pendente-conversao, ou pendente-manual (ver Passo 4)
    arquivo_pdf: pdfs/<chave>.pdf  # omitir/null enquanto status for pendente-manual
    arquivo_md: md/<chave>.md  # omitir/null se status for pendente-conversao ou pendente-manual e nao houver arquivo usavel
    resumo: "<2-4 linhas resumindo o achado/argumento principal, escritas por você a partir do conteúdo de md/<chave>.md — enquanto status for pendente-manual, pode ser um resumo provisório a partir do abstract da busca>"
    tema_relacionado: "<o termo de busca ou a lacuna que originou essa busca>"
    adicionado_em: "<data de hoje, AAAA-MM-DD>"
```

Artigos que foram pro `baixar-manualmente.md` (Passo 4) **já entram no índice imediatamente**, com
status `pendente-manual` — é isso que permite o Passo 3 reconhecer, numa busca futura, que aquele
artigo já está pendente e não deve virar candidato "novo" de novo. Quando o aluno baixa o PDF
manualmente e essa skill roda de novo, o Passo 5 detecta o PDF novo na pasta, converte, e o Passo 6
**atualiza essa mesma entrada** (mesma `chave`) pra `verificado` ou `pendente-conversao` — nunca cria
uma segunda entrada pro mesmo artigo. Nesse momento, remova também a seção correspondente daquele
artigo em `tcc-kit/referencias/baixar-manualmente.md` — ela existe só pra rastrear o que ainda está
aguardando download manual, e esse artigo não está mais nessa situação.

## Passo 7 — Resumo final

Informe ao aluno, em 2-3 frases: quantas referências foram adicionadas com sucesso (`verificado`),
quantas ficaram pendentes de conversão, e quantas foram pra `baixar-manualmente.md` aguardando download
manual. Se algum PDF órfão foi indexado nesta rodada (Passo 6), avise também e peça pro aluno conferir
os metadados inferidos daquela entrada. Se alguma conversão saiu no código 3 (Passo 5) — sem
reconhecimento de fórmula por falta do `llama-server` —, avise quais referências caíram nesse caso e
que fórmulas/equações delas podem precisar de conferência manual.

## Passo 8 — Atualizar checklist e histórico

Conte quantas entradas em `tcc-kit/referencias/index.yaml` têm `status: verificado` (a contagem total
no índice, não só as adicionadas nesta execução).

Confira se `tcc-kit/checklist.md` existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a seção "Referências" já marcada
  (`[x]` se a contagem for 1 ou mais, `[ ]` se for zero; as demais seções ficam no estado inicial, como
  no esqueleto):

```markdown
# Checklist de progresso — TCC

## Configuração institucional
- [ ] Configurado (tcc-kit/config.md)

## Template
- [ ] Escolhido/adaptado (tcc-kit/template.md)

## Tema
- [ ] Definido (tcc-kit/tema.md)

## Referências
- [x] Pelo menos 1 referência verificada (N verificada(s))

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
Atualizado em: <data de hoje, AAAA-MM-DD>, por: revisao-bibliografica
```

(substitua `N` pela contagem real; se a contagem for zero, use `- [ ] Pelo menos 1 referência
verificada` sem o número, igual ao esqueleto original).

- **Se já existir**, edite só a seção "Referências" pra `- [x] Pelo menos 1 referência verificada (N
  verificada(s))` (ou `- [ ] Pelo menos 1 referência verificada` se a contagem for zero), preservando as
  demais seções como estão, e atualize a linha final pra `Atualizado em: <data de hoje, AAAA-MM-DD>,
  por: revisao-bibliografica`.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — revisao-bibliografica
Busca rodada pro termo "<termo usado>". N referência(s) nova(s) verificada(s), M pendente(s) de
conversão ou download manual.
```

Preencha `N` e `M` com os números reais desta execução (não a contagem total do índice, que já foi
usada acima pro checklist) — se nenhuma referência nova foi confirmada pelo aluno, ainda assim
acrescente a entrada, registrando que a busca aconteceu sem resultado confirmado.
