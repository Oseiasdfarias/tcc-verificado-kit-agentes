---
name: adicionar-referencias
description: Use quando o aluno já tiver referências próprias e quiser colocá-las no TCC -- "adiciona minhas referências", "já tenho os artigos", "importa meu .bib do Zotero", "coloquei os PDFs na pasta", "meu orientador me passou uns artigos". Lê a pasta tcc-kit/referencias/minhas/ (PDFs, .bib, lista de DOIs ou links), confere cada item numa base oficial, mostra o que foi confirmado, o que diverge e o que não foi encontrado, e só indexa o que o aluno aprovar, junto das referências buscadas pelo kit.
---

# Adicionar Referências — as suas, conferidas

O aluno pesquisa por conta própria, recebe artigos do orientador, usa Zotero ou Mendeley. Essas
referências entram no mesmo índice das que o kit busca, com a mesma exigência: existir de verdade e
estar com os dados certos. Esta skill confere, mostra o resultado e só indexa o que o aluno aprovar.

Regras:

- **Nunca apaga nem altera** nada em `tcc-kit/referencias/minhas/`: é a pasta do aluno.
- **Nada entra no índice sem aprovação** (Passo 4).
- Referência não confirmada não é "falsa": é "não encontrada". O aluno pode ter a fonte em mãos.
- Comandos que funcionem no PowerShell: para rede, use a ferramenta WebFetch; para arquivo, `uv run
  python`.

Os scripts do plugin (`pdf_to_md.py`, `bib_do_indice.py`) seguem a regra de caminho de
`revisao-bibliografica`: procure-os relativos à raiz deste plugin e não invente um caminho.

## Passo 1 — A pasta de entrada

Se `tcc-kit/referencias/minhas/` não existir ou estiver vazia, crie a pasta e diga ao aluno o que
colocar lá, e pare:

> "Coloque em `tcc-kit/referencias/minhas/` o que você tiver: os PDFs dos artigos, um arquivo `.bib`
> exportado do Zotero ou do Mendeley, e/ou um `lista.txt` com uma referência por linha (DOI, link ou a
> referência escrita). Depois me chame de novo."

## Passo 2 — Montar a lista de itens

- **Cada PDF**: converta para texto e leia só o começo (título, autores, ano, DOI):
  ```bash
  uv run --with pdfplumber "<caminho do plugin>/scripts/pdf_to_md.py" "tcc-kit/referencias/minhas/<arquivo>.pdf" "tcc-kit/referencias/md/_minhas-<arquivo>.md"
  ```
- **Cada entrada de `.bib`**: tipo, chave do aluno, título, autores, ano, veículo, DOI.
- **Cada linha útil de `lista.txt`**: ignore linhas em branco e as que começam com `#`. Um link
  `https://doi.org/<doi>` ou `https://dx.doi.org/<doi>` vale como DOI. Outro link: abra com WebFetch e
  procure título e DOI na página. Texto livre: extraia título, primeiro autor e ano.

Leia `tcc-kit/referencias/index.yaml`, se existir, e pule os itens cujo DOI ou título (sem diferenciar
maiúsculas) já estão lá. Guarde a lista dos pulados para o resumo.

## Passo 3 — Conferir cada item

- **Com DOI**: WebFetch em `https://api.crossref.org/works/<doi>`. Resposta 404 ou sem `message`:
  `nao-encontrado`. Com resposta: compare título, primeiro autor e ano com o que o aluno trouxe.
- **Sem DOI**: WebFetch em
  `https://api.crossref.org/works?query.bibliographic=<título codificado em URL>&rows=3`. Aceite só um
  resultado com título praticamente igual e mesmo primeiro autor. Sem isso, tente o arXiv
  (`https://export.arxiv.org/api/query?search_query=ti:"<título>"`) quando o item parecer preprint.
  Nada claro: `nao-encontrado`.

Classifique:

- `verificado`: a base confirma e os dados do aluno batem;
- `divergente`: a base confirma a obra, mas algum dado do aluno está diferente (ano, autor, título,
  veículo): guarde os dois valores;
- `nao-encontrado`: nenhuma base confirmou.

## Passo 4 — Mostrar e perguntar

Mostre uma tabela: item (arquivo ou linha), título, autor e ano, classificação, e, para `divergente`, o
dado do aluno e o da base lado a lado. Liste também os itens pulados por já estarem no índice.

Pergunte quais entram, e, para cada divergente, se vale o dado da base ou o do aluno. Para
`nao-encontrado`, explique que pode entrar como pendente, se o aluno tiver a fonte em mãos, e que a
revisão de citações vai continuar acusando até alguém confirmar. **Pare aqui e termine a sua resposta
com essa pergunta.** Nada de índice, `.bib` ou cópia de arquivo antes de o aluno responder.

## Passo 5 — Indexar

Para cada item aprovado, defina a `chave`: item vindo de `.bib` mantém a chave que o aluno já usa (os
`.tex` dele podem citar essa chave), a menos que ela colida com o índice ou com outra chave desta rodada;
nos demais casos, ou na colisão, gere no padrão da `revisao-bibliografica` (`sobrenomeAno`, com `b`,
`c`...). Diga ao aluno toda chave que mudou em relação ao `.bib` dele e acrescente em
`tcc-kit/referencias/index.yaml` (crie com `referencias:` se não existir), no formato do Passo 6 da
`revisao-bibliografica`, com o campo novo:

```yaml
    origem: aluno
```

- `verificado` ou `divergente` aprovado: `status: verificado`, com os dados escolhidos pelo aluno. Se
  numa divergência o aluno ficou com o dado dele (e não com o da base), acrescente `fonte_bib: indice`:
  assim o `.bib` é montado com os dados do índice, e não com o BibTeX oficial do DOI.
- `nao-encontrado` aprovado: `status: nao-confirmada`, e o `resumo` começa com "Não confirmada em base
  oficial; fonte fornecida pelo aluno." **Não copie o PDF para `pdfs/`**: o original fica só em
  `minhas/`. O status `nao-confirmada` não é convertido nem promovido a `verificado` por nenhuma skill;
  só uma nova conferência desta skill, com dados que a base confirme, muda o status.
- Item vindo de PDF (verificado ou divergente aprovado): copie o PDF para `tcc-kit/referencias/pdfs/<chave>.pdf` e gere
  `tcc-kit/referencias/md/<chave>.md` com o `pdf_to_md.py` (o original fica em `minhas/`); preencha
  `arquivo_pdf` e `arquivo_md`, e escreva o `resumo` a partir do texto.
- Item sem PDF: `arquivo_pdf` e `arquivo_md` omitidos; `resumo` a partir do abstract da base, se houver.

Entradas antigas do índice sem o campo `origem` contam como `origem: busca`. Não as altere.

Apague os arquivos temporários `tcc-kit/referencias/md/_minhas-*.md` do Passo 2.

## Passo 6 — `.bib`

```bash
uv run "<caminho do plugin>/scripts/bib_do_indice.py" --chaves <chaves aprovadas com status verificado>
```

Só entradas `status: verificado` vão para o `.bib`; `nao-confirmada` fica de fora, e a revisão de
citações continua acusando se o texto a citar.

## Passo 7 — Registrar e resumir

Se `tcc-kit/checklist.md` existir, atualize a seção `## Referências` com a contagem total de entradas
`status: verificado` no índice (`- [x] Pelo menos 1 referência verificada (N verificada(s))`) e a linha
final `Atualizado em: <data de hoje, AAAA-MM-DD>, por: adicionar-referencias`. Se não existir, não crie.

Acrescente no fim de `tcc-kit/historico.md` (crie com `# Histórico — TCC` se não existir):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — adicionar-referencias
<n> itens lidos, <v> verificados, <d> divergentes, <x> não encontrados, <k> pulados (já no índice).
<a> entraram no índice (<p> como pendentes).
```

Resuma ao aluno: o que entrou, o que ficou de fora, e lembre que confirmar que o artigo existe não é o
mesmo que confirmar que ele diz o que o texto vai afirmar. Essa leitura é dele.
