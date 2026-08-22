---
name: escolher-template
description: Use quando o aluno quiser escolher ou trocar o template LaTeX do TCC -- "acha um template pra minha universidade", "quero usar o template oficial da minha faculdade", "não sei que template usar", ou quando iniciar-tcc detectar que ainda não há template e o aluno confirmar que quer esse apoio.
---

# Escolher Template — busca, valida e adapta o template LaTeX do TCC

Esta skill ajuda o aluno a encontrar um template LaTeX da própria universidade (se existir no
Overleaf) e adapta com os dados institucionais dele. O valor real aqui é poupar o garimpo de
candidatos relevantes — não existe forma de baixar um template do Overleaf automaticamente, então o
download continua sendo um passo manual do aluno em qualquer caso.

## Passo 1 — Confira se já existe um template escolhido

Confira se `tcc-kit/template.md` já existe.

Se existir: mostre a origem do template atual (`Origem`, `Campos preenchidos`, `Campos como
placeholder`) e pergunte ao aluno o que ele quer fazer:
- (a) reescolher o template do zero;
- (b) só readaptar com os dados atuais de `tcc-kit/config.md` (sem buscar de novo);
- (c) manter como está, não fazer nada agora.

Se (a): siga o fluxo normal a partir do Passo 2 (a pergunta buscar-ou-padrão). Se (b): pule direto
pro Passo 8 (adaptação). Se (c): encerre a skill sem fazer nada.

Se não existir: siga direto pro Passo 2.

## Passo 2 — Perguntar se quer buscar ou usar o padrão

Pergunte: "Quer que eu pesquise um template LaTeX específico da sua universidade no Overleaf, ou
prefere já usar o template ABNT padrão do curso?"

Se o aluno preferir o padrão do curso: pule direto pro Passo 8 (adaptação) — o template padrão já está
em `tcc/`, não precisa buscar nem baixar nada.

## Passo 3 — Buscar

Determine o nome da universidade: pergunte se não souber, ou leia de `tcc-kit/config.md` se já
existir. Busque com WebSearch:

```
site:overleaf.com <universidade> tese OR dissertação OR TCC
```

Se não encontrar nada claramente relevante, tente uma busca mais ampla:
`<universidade> template LaTeX tese overleaf`.

**Não existe API de busca estruturada do Overleaf** — essa busca é sempre WebSearch geral, menos
precisa que a Semantic Scholar API do motor de referências (`revisao-bibliografica`). Isso é esperado,
não um bug: o valor é poupar garimpo, não garantir precisão.

## Passo 4 — Apresentar candidatos

Apresente os candidatos encontrados (título do template, link, breve descrição de 1 linha) numa lista
numerada. **Sempre inclua também o link da galeria geral do Overleaf**
(`https://www.overleaf.com/gallery/tagged/thesis`), mesmo quando a busca automática encontrar
candidatos — o aluno pode preferir pesquisar sozinho.

Pergunte qual o aluno quer usar: um dos candidatos, o padrão do curso, ou se ele prefere pesquisar por
conta própria (nesse caso, pare aqui e espere ele voltar com uma escolha).

## Passo 5 — Orientar o download manual

Se o aluno escolheu um template do Overleaf: **não existe download direto de zip nas páginas de
template do Overleaf** (só "Open as Template", que abre o editor deles, ou "View Source", só
visualização) — oriente o passo manual:

1. Abra o link do template escolhido.
2. Clique em "Open as Template" (cria uma conta grátis no Overleaf se ainda não tiver).
3. No editor, use o menu de download (ícone de download, ou Menu → Download → Source) pra baixar como
   zip.
4. Extraia o conteúdo do zip pra dentro da pasta `tcc/` do projeto, substituindo os arquivos de
   template atuais.

Espere o aluno confirmar que terminou — nunca assuma que foi feito.

## Passo 6 — Confirmar que os arquivos mudaram

Se o aluno escolheu um template do Overleaf, confira se `tcc/` realmente tem arquivos novos/diferentes
dos que tinha antes (ex: nomes de arquivo `.tex` diferentes do padrão abnTeX2, ou conteúdo visivelmente
diferente). Se não notar mudança nenhuma, avise o aluno explicitamente e pergunte de novo — nunca finja
que os arquivos foram atualizados.

Se o aluno escolheu o padrão do curso (Passo 2), pule este passo — não há nada pra conferir.

## Passo 7 — Reestruturar se precisar

Olhe os arquivos `.tex` presentes em `tcc/` (e subpastas, se houver). Identifique: qual é o arquivo
principal (compila o documento inteiro, geralmente com `\documentclass` e vários `\input`/`\include`),
quais são os capítulos individuais, e onde fica a bibliografia (`.bib`).

Se a estrutura já bate com a convenção do kit (`tcc/capitulos/<slug>.tex` pros capítulos,
`tcc/referencias.bib` pra bibliografia, arquivo principal direto em `tcc/`), não faça nada neste passo
— registre "já estava no formato esperado" pro resumo do Passo 9.

Se a estrutura for diferente (ex: capítulos numa subpasta com nome diferente, tipo `chapters/ch1.tex`):
- Pra cada capítulo que der pra identificar com confiança um dos 5 slugs do curso (`introducao`,
  `referencial-teorico`, `metodologia`, `resultados`, `discussao-consideracoes-finais` — pelo título do
  capítulo ou pelo conteúdo), mova/renomeie o arquivo pra `tcc/capitulos/<slug>.tex`.
- Pra capítulo que não der pra mapear com confiança nesses 5 slugs, mantenha o nome original, só mova
  pra `tcc/capitulos/` se ainda não estiver lá.
- Ajuste todo `\input{...}`/`\include{...}` no arquivo principal (e em qualquer outro arquivo que
  referencie os caminhos movidos) pros novos caminhos.
- Confirme que a ordem de inclusão dos capítulos no arquivo principal continua a mesma de antes — só os
  caminhos mudam, o documento renderizado tem que ficar idêntico ao original.

Registre o que foi reorganizado (ou "já estava no formato esperado") pro resumo do Passo 9.

## Passo 8 — Adaptar com os dados do onboarding

Leia `tcc-kit/config.md`. Se não existir, avise o aluno que não há dados de onboarding ainda e sugira
rodar `configurar-projeto` primeiro — mas se ele preferir seguir sem isso, adapte só com o que tiver,
deixando o resto como placeholder.

No(s) arquivo(s) principal(is) de `tcc/` (capa, folha de rosto — geralmente comandos como
`\author{}`, `\title{}`, ou campos customizados da classe LaTeX usada), substitua:
- Onde `config.md` tem dado real: substitua o valor real.
- Onde `config.md` não tem dado (ex: banca "a definir"): insira um placeholder claro e visível, tipo
  `[BANCA A DEFINIR]` — nunca deixe em branco silenciosamente, nem invente um valor.

Se não conseguir identificar com segurança onde inserir algum dado (a estrutura do template é atípica
demais), não "chute" o lugar — avise o aluno que não conseguiu localizar automaticamente e peça pra
ele indicar o arquivo/linha.

## Passo 9 — Salvar e resumir

Salve `tcc-kit/template.md`:

```markdown
# Template do Projeto
**Origem:** <"Overleaf: <nome/link>" ou "Padrão abnTeX2 do curso">
**Estrutura:** <"reorganizada" ou "já estava no formato esperado">
**Campos preenchidos:** <lista>
**Campos como placeholder:** <lista, ou "nenhum">
Escolhido em: <data de hoje, AAAA-MM-DD>
Última adaptação: <data de hoje, AAAA-MM-DD>
```

Informe ao aluno, em 2-3 frases: origem do template, o que foi reorganizado (se algo foi), e quais
campos ficaram como placeholder pra ele conferir depois.
