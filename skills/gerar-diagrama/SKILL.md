---
name: gerar-diagrama
description: Use quando o aluno quer criar um diagrama, fluxograma ou ilustração conceitual em TikZ pro TCC (não gráfico de dado/resultado -- barra, linha, dispersão, pizza) -- "preciso de um diagrama da minha metodologia", "quero ilustrar esse conceito", "como faço um fluxograma no LaTeX".
---

# Gerar Diagrama — diagrama ou ilustração conceitual em TikZ

Esta skill ajuda a criar diagramas e ilustrações conceituais (fluxogramas, frameworks, mapas de
relacionamento) diretamente em TikZ, dentro do próprio LaTeX. **Não cobre gráfico de dado real**
(barra, linha, dispersão, pizza a partir de resultados) -- isso é responsabilidade de uma frente
diferente, ainda não coberta pelo kit.

## Passo 1 — Entender o que desenhar

Pergunte:
1. O que o diagrama precisa representar (ex: as etapas da metodologia, um framework conceitual do
   referencial teórico, o relacionamento entre variáveis/constructos).
2. Qual capítulo ele ilustra (Metodologia, Referencial teórico, ou outro).
3. Os elementos/passos/conceitos específicos que entram no diagrama, e como se conectam (setas,
   hierarquia, ordem).

Se o pedido soar como gráfico de dado real (números, percentuais, barras, séries), avise o aluno que
essa skill não cobre isso ainda e não prossiga -- não tente gerar de qualquer jeito.

## Passo 2 — Conferir os pacotes que o diagrama exige no preâmbulo

Confira se os itens abaixo já estão no preâmbulo do documento (mesmo arquivo/local onde outros
pacotes do template já estão declarados). Se algum não estiver, adicione:

- `\usepackage{tikz}` -- necessário pra qualquer diagrama TikZ.
- `\usepackage{float}` -- necessário pro `[H]` usado no Passo 3 (o `abntex2` não carrega `float` por
  padrão; sem ele, o `[H]` quebra a compilação).
- `\usetikzlibrary{positioning}` -- necessário pra sintaxe de posicionamento relativo (ex:
  `right=of a`), comum em diagramas de fluxo.

## Passo 3 — Gerar o código do diagrama

Gere o código TikZ dentro de um ambiente `figure`, com `\centering` e `\caption{}` numerada (convenção
ABNT de figura), salvo em `tcc/diagramas/<nome>.tex` -- crie o diretório `tcc/diagramas/` se ainda não
existir. `<nome>` é um slug curto derivado do que o diagrama representa (ex: `fluxo-metodologia`,
`framework-conceitual`), decidido em conversa com o aluno no Passo 1.

Estrutura esperada do arquivo:

```latex
\begin{figure}[H]
  \centering
  \begin{tikzpicture}
    % código do diagrama aqui
  \end{tikzpicture}
  \caption{<legenda descritiva, combinada com o aluno>}
  \label{fig:<nome>}
\end{figure}
```

## Passo 4 — Incluir no capítulo certo

Confira se `tcc/capitulos/<slug-do-capítulo>.tex` já tem um `\input{diagramas/<nome>.tex}` ou se
precisa ser adicionado. Se o capítulo ainda não existir (aluno quer o diagrama antes de escrever o
capítulo), avise que o `\input` precisa ser adicionado manualmente (ou pela skill `escrever-capitulo`
depois) quando o capítulo for escrito -- não crie um arquivo de capítulo vazio só pra isso.

Peça a confirmação do aluno sobre onde no capítulo o `\input` deve entrar (normalmente perto do trecho
que menciona o que o diagrama ilustra).

## Passo 5 — Compilar e conferir

Rode `latexmk -pdf` e confira visualmente com o aluno: o diagrama está legível, as setas/conexões
fazem sentido, a legenda está clara. Se algo precisar de ajuste, pergunte se é ajuste de **conteúdo**
(muda o que o diagrama representa) ou de **aparência** (cor, espaçamento, tamanho) -- trate um de cada
vez, nunca misture os dois no mesmo pedido de ajuste (evita mudança de conteúdo acontecer sem querer
junto de um ajuste estético).

## Passo 6 — Atualizar histórico

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — gerar-diagrama
Diagrama "<nome>" gerado, ilustrando <capítulo/trecho>. Arquivo: tcc/diagramas/<nome>.tex.
```

**Esta skill não edita `tcc-kit/checklist.md`** -- diagrama é uma ação opcional e repetível, não um
estágio de ocorrência única do ciclo de vida do TCC (ver spec
`docs/superpowers/specs/2026-09-04-diagramas-tikz-design.md` no repositório curso-tcc-ia pra o
raciocínio completo).
