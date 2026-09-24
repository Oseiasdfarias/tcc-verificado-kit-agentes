---
name: formatar-abnt
description: Use quando o TCC já tiver os capítulos escritos e o aluno quiser fechar a formatação -- "formata meu TCC na ABNT", "arruma a formatação final", "meu PDF está com erro", "as citações estão com interrogação", "confere se está tudo na norma", ou quando iniciar-tcc sugerir a formatação antes da auditoria final. Compila, lê o log, garante as referências no .bib, confere os elementos obrigatórios e propõe correções de forma, com o antes e o depois. Só mexe na forma, nunca nas frases do aluno, e só aplica o que ele aprovar.
---

# Formatar ABNT — a forma final, sem tocar no texto

Nesta etapa o conteúdo já está escrito e revisado. O que falta é a forma: citação que sai como "?",
figura sem legenda ou fonte, elemento obrigatório faltando, aviso de compilação. Esta skill encontra,
propõe e aplica o que o aluno aprovar.

Regras:

- **Só forma**: comandos LaTeX, legendas, fontes de figuras e tabelas, `.bib`, elementos pré e
  pós-textuais do template. **Nunca altera uma frase do aluno**, nem para "melhorar".
- **Resumo, abstract, agradecimentos, dedicatória e epígrafe são texto do aluno**: se faltarem, viram
  pendência; esta skill não escreve.
- Toda edição com backup antes (`estado_projeto.py backup`) e listada no relatório.
- Nada é aplicado sem aprovação (Passo 5).
- A norma da instituição manda: se o `config.md` ou o template trazem regra própria, ela vale sobre o
  padrão ABNT genérico.

Os scripts do plugin (`estado_projeto.py`, `bib_do_indice.py`) seguem a regra de caminho de
`revisao-bibliografica`.

## Passo 1 — Arquivo principal e compilação

Identifique o arquivo principal em `tcc/` (o que tem `\documentclass`; se houver mais de um, o
indicado em `tcc-kit/template.md`). Compile a partir de `tcc/`:

```bash
latexmk -pdf -interaction=nonstopmode <arquivo principal>
```

Sem `latexmk` no computador (aluno que usa só o Overleaf): siga só com a leitura dos `.tex` e diga no
resumo que o documento não foi compilado aqui.

## Passo 2 — Referências no `.bib`

A partir da raiz do projeto:

```bash
uv run "<caminho do plugin>/scripts/bib_do_indice.py" --todas-citadas tcc/capitulos
```

Chave "citada sem entrada no índice" é pendência do aluno: a referência precisa passar por
`revisao-bibliografica` ou `adicionar-referencias`. Se entradas foram acrescentadas, compile de novo.

## Passo 3 — Ler o log

Leia `tcc/<arquivo principal>.log` e agrupe:

- citação ou referência indefinida (`Citation ... undefined`, `Reference ... undefined`);
- rótulo duplicado;
- pacote ou arquivo não encontrado;
- `Overfull \hbox` acima de 10pt (cite o arquivo e a linha).

Leia também os `.tex` de `tcc/capitulos/` procurando: `figure` ou `table` sem `\caption`; figura ou
tabela sem fonte (no abnTeX2, `\fonte{...}`; em outra classe, uma linha "Fonte: ..." logo abaixo);
`\caption` depois do conteúdo em tabela (na ABNT, o título da tabela vem acima); `\cite` usado onde o
texto pede o autor na frase (no abnTeX2, `\citeonline`).

## Passo 4 — Elementos obrigatórios

Confira no arquivo principal e no template: capa, folha de rosto, resumo com palavras-chave, abstract
com keywords, lista de figuras (se houver figura), lista de tabelas (se houver tabela), sumário,
referências. Confira capa e folha de rosto contra `tcc-kit/config.md` (universidade, curso, aluno,
orientador, cidade, ano).

Ausência de lista ou sumário: correção de forma (entra no Passo 5). Ausência de resumo ou abstract:
pendência do aluno.

## Passo 5 — Propor e perguntar

Numere as correções de forma, cada uma com arquivo, o antes e o depois (o trecho LaTeX exato). Separe,
em outra lista, as pendências do aluno (textos que faltam, referências sem entrada no índice, exigências
da instituição que não dá para conferir daqui).

Quando a correção precisa de um texto que só o aluno sabe (a legenda de uma figura, a fonte de uma
tabela), pergunte esse texto junto.

Pergunte quais correções aplicar. **Pare aqui e termine a sua resposta com essa pergunta.** Nenhum
arquivo editado antes de o aluno responder.

## Passo 6 — Aplicar e recompilar

Para cada arquivo que vai mudar, backup antes:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" backup <arquivos>
```

Aplique só as correções aprovadas, sem tocar em nenhuma frase. Compile de novo e compare o log com o
do Passo 3: o que sumiu, o que continua, o que apareceu.

## Passo 7 — Relatório

Grave `tcc-kit/relatorios/formatacao-<data de hoje, AAAA-MM-DD>.md` (backup antes se já existir um do
mesmo dia):

```markdown
# Formatação ABNT — <data>

## O que mudou
1. <arquivo>:<linha> — <o que foi feito>

## O que o log ainda acusa
- <aviso> (ou "nada")

## Pendências suas
- <texto que falta, referência sem entrada no índice, etc.>

## Confira no manual da sua instituição
Margens, fonte, espaçamento e numeração seguem o template. Se a sua instituição tiver manual de normas
próprio, confira esses pontos nele: é a regra que vale na entrega.
```

## Passo 8 — Registrar e resumir

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" registrar --etapa formatacao --saida tcc-kit/relatorios/formatacao-<data>.md --entradas <arquivo principal> tcc/capitulos tcc/referencias.bib
```

Se `tcc-kit/checklist.md` existir: na seção `## Formatação ABNT`, troque a linha por
`- [x] Rodada em <data de hoje, AAAA-MM-DD> (<n> correções, <p> pendências suas)` e atualize a linha
final `Atualizado em: <data de hoje, AAAA-MM-DD>, por: formatar-abnt`. Se a seção não existir
(checklist de versão anterior), insira-a antes de `## Auditoria completa do TCC`. Se o checklist não
existir, não crie.

Acrescente no fim de `tcc-kit/historico.md` (crie com `# Histórico — TCC` se não existir):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — formatar-abnt
<n> correções aplicadas, <m> recusadas, <p> pendências do aluno. Relatório:
tcc-kit/relatorios/formatacao-<data>.md.
```

Resuma ao aluno: o que mudou, o que o log ainda acusa, as pendências dele. Sugira abrir o PDF e
conferir as páginas com figura e a lista de referências, e depois `auditoria-tcc-completo`.
