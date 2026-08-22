---
name: revisar-capitulo
description: Use quando o aluno quiser uma auditoria completa de um capítulo do TCC antes de considerar ele pronto -- roda, em sequência, verificação de dados, verificação de citações, e as 3 personas de revisão (orientador, banca, forma/português), e produz um relatório único.
---

# Revisar Capítulo — auditoria completa do TCC Verificado

Esta skill roda os 5 agentes especialistas do kit, na ordem certa, contra um capítulo do TCC, e
consolida tudo em um relatório único.

## Quando usar

O aluno pede algo como "audita esse capítulo antes de eu considerar pronto" ou "roda a revisão
completa". Peça o caminho do capítulo se não foi informado, e o caminho do resumo de dados real
(normalmente `tcc/dados/resumo-real.md`) se o capítulo fizer qualquer afirmação sobre
dados/resultados.

## Ordem de disparo — importa

Revisar argumento e forma de um capítulo que ainda tem dado inventado ou citação falsa é desperdício
de tempo. Por isso, sempre nessa ordem:

1. **guardiao-dados** — primeiro. Se ele encontrar divergência bloqueante, ainda assim continue os
   próximos agentes (é o relatório final que decide a prioridade, não você) — mas garanta que o achado
   dele apareça em destaque no topo do relatório final.
2. **revisor-citacoes** — segundo, mesmo motivo (é factual, bloqueante).
3. **orientador-rigoroso**, **banca-critica**, **revisor-forma** — nessa ordem, depois. Esses três são
   independentes entre si e podem ser despachados em qualquer ordem entre eles, mas sempre depois dos
   dois primeiros.

## Como despachar cada agente

Use a ferramenta Task pra cada um dos 5 agentes, passando o caminho do capítulo (e, pro
guardiao-dados, também o caminho do resumo de dados). Espere cada um terminar e devolver seu relatório
antes de consolidar.

## Consolidando o relatório final

Salve em `tcc/relatorios/<nome-do-capitulo>-<data>.md`, nesta estrutura:

```markdown
# Auditoria — [nome do capítulo] — [data]

## Achados bloqueantes
[Copie aqui qualquer item marcado BLOQUEANTE pelo guardiao-dados, e qualquer citação NÃO ENCONTRADA ou
SUSPEITA do revisor-citacoes — marque cada citação NÃO ENCONTRADA como *conferir manualmente*, não
como citação falsa (NÃO ENCONTRADA não é sinônimo de errada: pode ser uma referência real que a busca
não alcançou). Se nenhum dos dois agentes encontrou nada, escreva "nenhum achado bloqueante".]

## Integridade de dados (guardiao-dados)
[relatório completo do agente]

## Citações (revisor-citacoes)
[relatório completo do agente]

## Argumento — orientador (orientador-rigoroso)
[relatório completo do agente]

## Argumento — banca (banca-critica)
[relatório completo do agente]

## Forma e escrita (revisor-forma)
[relatório completo do agente]

---
Revisado por IA — a decisão final sobre cada capítulo é sua (TCC Verificado, Aula 3.2).
```

Depois de salvar, informe ao aluno o caminho do relatório e um resumo de 2-3 frases: quantos achados
bloqueantes, e o tom geral dos outros 3 agentes (sólido / precisa de ajuste / muitos apontamentos).
