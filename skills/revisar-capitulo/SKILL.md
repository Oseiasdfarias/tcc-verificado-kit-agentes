---
name: revisar-capitulo
description: Use quando o aluno quiser uma auditoria completa de um capítulo do TCC antes de considerar ele pronto -- roda, em sequência, verificação de dados, verificação de citações, verificação de metodologia, e as 3 personas de revisão (orientador, banca, forma/português), e produz um relatório único.
---

# Revisar Capítulo — auditoria completa do TCC Verificado

Esta skill roda os 6 agentes especialistas do kit, na ordem certa, contra um capítulo do TCC, e
consolida tudo em um relatório único.

## Quando usar

O aluno pede algo como "audita esse capítulo antes de eu considerar pronto" ou "roda a revisão
completa". Peça o caminho do capítulo se não foi informado, o caminho do resumo de dados real
(normalmente `tcc/dados/resumo-real.md`) se o capítulo fizer qualquer afirmação sobre
dados/resultados, e o caminho de `tcc-kit/metodologia.md` se existir (usado pelo `guardiao-metodo`).

## Identificar o slug do capítulo

Mapeie o capítulo pedido pro slug correspondente:

| Aluno diz (exemplos) | Slug |
|---|---|
| introdução | `introducao` |
| referencial teórico, fundamentação teórica, revisão de literatura | `referencial-teorico` |
| metodologia, método | `metodologia` |
| resultados | `resultados` |
| discussão, considerações finais, conclusão | `discussao-consideracoes-finais` |

Se o aluno pedir um capítulo fora desses 5 (ex: um TCC com estrutura diferente), slugifique livre
(minúsculo, hífen, sem acento) — não force um dos 5 slugs fixos onde não se aplica.

## Ordem de disparo — importa

Revisar argumento e forma de um capítulo que ainda tem dado inventado ou citação falsa é desperdício
de tempo. Por isso, sempre nessa ordem:

1. **guardiao-dados** — primeiro. Se ele encontrar divergência bloqueante, ainda assim continue os
   próximos agentes (é o relatório final que decide a prioridade, não você) — mas garanta que o achado
   dele apareça em destaque no topo do relatório final.
2. **revisor-citacoes** — segundo, mesmo motivo (é factual, bloqueante).
3. **guardiao-metodo**, **orientador-rigoroso**, **banca-critica**, **revisor-forma** — nessa ordem,
   depois. Esses quatro são independentes entre si e podem ser despachados em qualquer ordem entre
   eles, mas sempre depois dos dois primeiros (são julgamento interpretativo, não checagem factual
   bloqueante contra uma fonte única).

## Como despachar cada agente

Use a ferramenta Task pra cada um dos 6 agentes, passando o caminho do capítulo (e, pro guardiao-dados,
também o caminho do resumo de dados; e, pro guardiao-metodo, também o caminho de
`tcc-kit/metodologia.md` quando existir). Espere cada um terminar e devolver seu relatório antes de
consolidar.

## Consolidando o relatório final

Salve em `tcc-kit/relatorios/<slug>-<data>.md`, nesta estrutura:

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
[relatório completo do agente, MENOS a seção "## Lacunas encontradas" se ela existir -- essa seção vai
separada, logo abaixo, pra não ficar aninhada como um H2 dentro de outro H2]

## Lacunas encontradas (revisor-citacoes)
[Só inclua esta seção se o relatório do revisor-citacoes tiver uma seção "## Lacunas encontradas" --
nesse caso copie o conteúdo dela aqui. Se o relatório do revisor-citacoes não tiver essa seção, omita
esta seção inteira (não escreva "nenhuma lacuna encontrada" -- só omita).]

## Metodologia (guardiao-metodo)
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
bloqueantes, se o revisor-citacoes encontrou alguma lacuna (afirmação sem citação, ou citação NÃO
ENCONTRADA que valeria buscar referência nova), e o tom geral dos outros 4 agentes (sólido / precisa de
ajuste / muitos apontamentos).

## Atualizar checklist e histórico

Depois de salvar o relatório consolidado (seção anterior), recalcule o estado do capítulo `<slug>` do
zero — não presuma qual era o estado anterior no checklist — nesta ordem:

1. `tcc-kit/capitulos/<slug>/plano.md` não existe → estado é "Não iniciado".
2. `plano.md` existe, mas `tcc/capitulos/<slug>.tex` não existe ou não tem conteúdo real (mesmo
   critério de julgamento de leitura que `revisor-forma`/`iniciar-tcc` já usam — não é limite fixo de
   caracteres, é conferir se há texto real, não só o placeholder do template) → estado é "Planejado".
3. `tcc/capitulos/<slug>.tex` tem conteúdo real, mas não existe nenhum arquivo
   `tcc-kit/relatorios/<slug>-*.md` → estado é "Escrito, ainda não revisado".
4. Existe pelo menos um `tcc-kit/relatorios/<slug>-*.md` → leia o mais recente (maior data no nome do
   arquivo) e confira a seção "Achados bloqueantes": se disser "nenhum achado bloqueante", estado é
   "Revisado, sem achados bloqueantes"; caso contrário (pelo menos um achado listado), estado é
   "Revisado, com achados bloqueantes pendentes".

Confira se `tcc-kit/checklist.md` existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a linha do capítulo `<slug>` já
  refletindo o estado recalculado acima (as demais linhas e seções ficam no estado inicial, como no
  esqueleto — use o nome do capítulo por extenso na tabela: Introdução, Referencial teórico,
  Metodologia, Resultados, ou Discussão/Considerações finais, conforme o slug):

```markdown
# Checklist de progresso — TCC

## Configuração institucional
- [ ] Configurado (tcc-kit/config.md)

## Template
- [ ] Escolhido/adaptado (tcc-kit/template.md)

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
Atualizado em: <data de hoje, AAAA-MM-DD>, por: revisar-capitulo
```

(edite a linha do capítulo correspondente na tabela antes de salvar, com o estado recalculado).

- **Se já existir**, edite só a linha do capítulo `<slug>` na tabela "Capítulos" pro estado recalculado
  acima (preservando as demais linhas e seções como estão), e atualize a linha final pra `Atualizado
  em: <data de hoje, AAAA-MM-DD>, por: revisar-capitulo`.
- **Se o arquivo existir mas não bater com o formato esperado** (seção removida, cabeçalho alterado, não
  reconhecível): não sobrescreva sem avisar. Avise o aluno explicitamente que `tcc-kit/checklist.md`
  existe mas não bate com o formato esperado, e pergunte se quer que a skill recrie o esqueleto (perdendo
  o que foi editado manualmente) ou se prefere corrigir o arquivo manualmente antes de continuar — mesmo
  padrão que `iniciar-tcc` já usa pra `tcc-kit/tema.md` corrompido.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — revisar-capitulo (<nome do capítulo>)
Auditoria rodada pro capítulo <nome do capítulo>. N achados bloqueantes. Relatório:
tcc-kit/relatorios/<slug>-<data>.md.
```

Preencha `N` com a contagem real de itens na seção "Achados bloqueantes" do relatório que acabou de ser
salvo (0 se disser "nenhum achado bloqueante").
