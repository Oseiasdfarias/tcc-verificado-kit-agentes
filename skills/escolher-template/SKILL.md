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
existir. Se `tcc-kit/config.md` não existir, avise o aluno aqui mesmo que ainda não há dados de
onboarding e sugira rodar `configurar-projeto` antes de continuar — mas deixe claro que ele pode seguir
sem isso se preferir; isso não bloqueia, é só um aviso adiantado (os dados institucionais só fazem
falta de verdade lá no Passo 8, de adaptação).

Busque com WebSearch:

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

Registre o que foi reorganizado (ou "já estava no formato esperado") pro resumo do Passo 9 — incluindo,
se algum capítulo ficou com o nome original por falta de mapeamento confiável nos 5 slugs, a lista
desses arquivos especificamente.

## Passo 8 — Adaptar com os dados do onboarding

Leia `tcc-kit/config.md` (se ainda não tiver lido no Passo 3). Se não existir — o que só deve acontecer
nos caminhos que pulam o Passo 3 (padrão do curso, ou só readaptar) — trate como "sem dados": adapte só
com o que tiver, deixando o resto como placeholder, sem bloquear.

No(s) arquivo(s) principal(is) de `tcc/` (capa, folha de rosto — geralmente comandos como
`\author{}`, `\title{}`, campos customizados da classe LaTeX usada, e o campo `Logo`), substitua:
- Onde `config.md` tem dado real: substitua o valor real.
- Onde `config.md` não tem dado (ex: banca "a definir"): insira um placeholder claro e visível, tipo
  `[BANCA A DEFINIR]` — nunca deixe em branco silenciosamente, nem invente um valor.

`Logo`: se `config.md` tiver um caminho de arquivo em `Logo` (não "não informado"), copie o arquivo pra
dentro de `tcc/` (numa subpasta de imagens/figuras que já exista no template, ou crie `tcc/figuras/` se
não houver nenhuma). Antes de assumir `\includegraphics{}`, procure nos arquivos do template por um
comando de logo específico da classe LaTeX usada (algo como `\logo{}` ou `\brasao{}`) e use esse se
existir; senão, referencie a imagem via `\includegraphics{}` no local apropriado (capa e/ou folha de
rosto). Se `Logo` estiver "não informado", pule esse campo sem erro — não é uma falha, só um dado que
falta.

Se não conseguir identificar com segurança onde inserir algum dado (a estrutura do template é atípica
demais), não "chute" o lugar — avise o aluno que não conseguiu localizar automaticamente e peça pra
ele indicar o arquivo/linha.

## Passo 9 — Salvar e resumir

O que entra em `Origem`, `Estrutura` e `Escolhido em` depende de qual caminho foi seguido:

- **Buscou e escolheu um template do Overleaf (Passo 2 optou por buscar, levando ao Passo 3–7 — direto
  ou depois de reescolher do zero na opção "a" do Passo 1):** `Origem` é "Overleaf: <nome/link>".
  `Estrutura` vem do que o Passo 7 registrou: "reorganizada" ou "já estava no formato esperado".
  `Escolhido em` é a data de hoje.
- **Escolheu o padrão do curso (Passo 2 — direto ou depois de reescolher do zero na opção "a" do
  Passo 1):** `Origem` é "Padrão abnTeX2 do curso". `Estrutura` é sempre "Padrão do curso, já no formato
  esperado" — o Passo 7 não roda nesse caminho, então não há reestruturação real pra registrar.
  `Escolhido em` é a data de hoje.
- **Só readaptar (opção "b" do Passo 1):** o Passo 7 não roda nesse caminho. Antes de reescrever o
  arquivo, leia `Origem`, `Estrutura` e `Escolhido em` do `tcc-kit/template.md` já existente e mantenha
  os mesmos valores — não recalcule nem invente. Só `Campos preenchidos`, `Campos como placeholder` e
  `Última adaptação` são atualizados de verdade nesse caminho.

Salve `tcc-kit/template.md`:

```markdown
# Template do Projeto
**Origem:** <conforme o caminho seguido, ver acima>
**Estrutura:** <conforme o caminho seguido, ver acima>
**Campos preenchidos:** <lista>
**Campos como placeholder:** <lista, ou "nenhum">
Escolhido em: <conforme o caminho seguido, ver acima>
Última adaptação: <data de hoje, AAAA-MM-DD>
```

Informe ao aluno, em 2-3 frases: origem do template, o que foi reorganizado (se algo foi — e se algum
capítulo ficou com o nome original por falta de mapeamento confiável no Passo 7, liste esses arquivos
aqui explicitamente), e quais campos ficaram como placeholder pra ele conferir depois.

## Passo 10 — Atualizar checklist e histórico

**Se o Passo 1 encerrou a execução** (aluno optou por manter o template como está, opção (c)), não
atualize nem o checklist nem o histórico — nada mudou.

Confira se `tcc-kit/checklist.md` existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a seção "Template" já marcada (as
  demais seções ficam no estado inicial, como no esqueleto):

```markdown
# Checklist de progresso — TCC

## Configuração institucional
- [ ] Configurado (tcc-kit/config.md)

## Template
- [x] Escolhido/adaptado (tcc-kit/template.md)

## Tema
- [ ] Definido (tcc-kit/tema.md)

## Referências
- [ ] Pelo menos 1 referência verificada

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
Atualizado em: <data de hoje, AAAA-MM-DD>, por: escolher-template
```

- **Se já existir**, edite só a seção "Template" pra `- [x] Escolhido/adaptado (tcc-kit/template.md)`
  (preservando as demais seções como estão), e atualize a linha final pra `Atualizado em: <data de
  hoje, AAAA-MM-DD>, por: escolher-template`.
- **Se o arquivo existir mas não bater com o formato esperado** (seção removida, cabeçalho alterado, não
  reconhecível): não sobrescreva sem avisar. Avise o aluno explicitamente que `tcc-kit/checklist.md`
  existe mas não bate com o formato esperado, e pergunte se quer que a skill recrie o esqueleto (perdendo
  o que foi editado manualmente) ou se prefere corrigir o arquivo manualmente antes de continuar — mesmo
  padrão que `iniciar-tcc` já usa pra `tcc-kit/tema.md` corrompido.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — escolher-template
Template <origem — "encontrado no Overleaf: <nome/link>" ou "padrão abnTeX2 do curso"> escolhido e
adaptado com os dados institucionais.
```
