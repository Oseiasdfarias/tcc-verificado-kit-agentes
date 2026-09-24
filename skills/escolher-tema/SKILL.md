---
name: escolher-tema
description: Use quando o aluno ainda não tem um tema definido pro TCC e quer ajuda pra escolher um -- "não sei que tema escolher", "me ajuda a definir o tema do meu TCC", "tenho várias ideias mas não sei qual seguir", ou quando a skill iniciar-tcc detectar que não há tema e o aluno confirmar que quer esse apoio.
---

# Escolher Tema — brainstorm guiado até um tema específico e confirmado

Esta skill conduz uma conversa de descoberta até o aluno confirmar um tema específico e viável. Você
propõe e refina, mas quem decide o tema final é sempre o aluno.

## Passo 1 — Explorar

Pergunte, uma pergunta por vez (não despeje todas de uma vez):

1. Área/curso do aluno, e se o orientador já indicou alguma linha ou restrição.
2. O que desperta interesse real: um problema que o aluno já vive no trabalho/estágio, uma leitura que
   marcou, uma área do curso que mais gostou.
3. Com que material ele vai trabalhar, e se já tem acesso a ele. Classifique a resposta em um de três
   tipos, e confirme com o aluno se ficou em dúvida:
   - **estruturados**: tabela, planilha, dataset, questionário com respostas tabuladas;
   - **qualitativos**: entrevistas, documentos, observação, textos;
   - **nenhum**: pesquisa bibliográfica ou teórica, sem coleta de dados.

   Os três tipos são válidos e o kit acompanha todos. Só sugira um dataset público (por exemplo, do
   Kaggle, na área de interesse dele) se o aluno **quiser** trabalhar com dados estruturados e ainda
   não tiver nenhuma fonte.

## Passo 2 — Convergir

A cada resposta do aluno, não fique só perguntando — proponha 1-3 formulações concretas de tema pra
ele reagir e refinar. Exemplo de formato de proposta:

> "Baseado no que você me contou, alguns temas possíveis:
> 1. 'Fatores associados à evasão em cursos EAD de Administração: uma análise com dados de [dataset]'
> 2. 'Rotatividade de funcionários em call centers: o que os dados dizem sobre os motivos reais'
>
> Algum desses te representa, ou quer que eu ajuste alguma direção?"

Continue esse ciclo até o aluno confirmar explicitamente UM tema específico (não uma área genérica —
"marketing digital" não é tema, "o impacto de campanhas de remarketing na taxa de conversão de
e-commerces de moda" é tema).

## Passo 3 — Gerar termos de busca

A partir do tema confirmado, gere de 3 a 5 termos de busca (em português e, se fizer sentido pro campo,
também em inglês) que sirvam de ponto de partida pra busca bibliográfica. Esses termos não precisam ser
perfeitos — são só o primeiro filtro, o aluno pode pedir busca com outros termos depois.

## Passo 4 — Salvar

Confira se `tcc-kit/tema.md` já existe.

**Se já existir:** avise o aluno e pergunte se quer substituir pelo novo tema ou manter o atual. Nunca
sobrescreva sem essa confirmação explícita.

**Se não existir (ou o aluno confirmou substituir):** crie o arquivo:

```markdown
# Tema do TCC

**Tema:** <título definido>
**Área/curso:** <área/curso>
**Dados:** <estruturados | qualitativos | nenhum>
**Fonte dos dados:** <de onde vêm os dados, em uma linha; ou "não se aplica">
**Justificativa:** <2-4 linhas do porquê esse tema, capturando o que o aluno disse no Passo 1>
**Termos de busca sugeridos:** <termo1, termo2, termo3>

Definido em: <data de hoje, AAAA-MM-DD>
```

## Passo 5 — Resumo final

**Se o Passo 4 salvou um tema novo (arquivo criado ou substituído):** informe o aluno que o tema está
salvo, e que o próximo passo natural é buscar referências reais sobre ele — pergunte se ele quer que
você já rode a skill `revisao-bibliografica` agora, usando os termos de busca sugeridos (do arquivo que
acabou de salvar) como ponto de partida.
Se o tema tem `Dados: estruturados` e os dados já estão no projeto, diga que o primeiro passo é
preparar esses dados (skill `preparar-dados`) e ofereça as duas opções, preparar os dados ou buscar
referências, deixando o aluno escolher a ordem. Se o aluno já tem artigos próprios, lembre que a skill
`adicionar-referencias` confere e inclui essas referências.

**Se o aluno optou por manter o tema existente no Passo 4:** deixe claro que nada foi alterado e que o
tema em uso continua sendo o que já estava salvo em `tcc-kit/tema.md` — não diga que "acabou de salvar".
Em seguida, pergunte se ele quer buscar referências usando os termos de busca sugeridos já registrados
nesse arquivo existente.

## Passo 6 — Atualizar checklist e histórico

**Se o Passo 4 não salvou nada novo** (aluno optou por manter o tema existente sem alteração), não
atualize nem o checklist nem o histórico — nada mudou de fato, não há execução nova pra registrar.

**Se o Passo 4 salvou um tema novo** (arquivo criado ou substituído), confira se `tcc-kit/checklist.md`
existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a seção "Tema" já marcada (as demais
  seções ficam no estado inicial, como no esqueleto):

```markdown
# Checklist de progresso — TCC

## Configuração institucional
- [ ] Configurado (tcc-kit/config.md)

## Template
- [ ] Escolhido/adaptado (tcc-kit/template.md)

## Tema
- [x] Definido (tcc-kit/tema.md)

## Dados
**Tipo:** <valor de Dados gravado no tema.md>
- [ ] Preparados (tcc-kit/dados/limpeza.md)
- [ ] Resumo real (tcc/dados/resumo-real.md)

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

## Formatação ABNT
- [ ] Nunca rodada

## Auditoria completa do TCC
- [ ] Nunca rodada

## Apresentação de defesa
- [ ] Nunca gerada

---
Atualizado em: <data de hoje, AAAA-MM-DD>, por: escolher-tema
```

- **Se já existir**, edite só a seção "Tema" pra `- [x] Definido (tcc-kit/tema.md)` (preservando as
  demais seções como estão), e atualize a linha final pra `Atualizado em: <data de hoje, AAAA-MM-DD>,
  por: escolher-tema`.
- **Nos dois casos (checklist criado ou editado)**, preencha também, na seção `## Dados`, a linha
  `**Tipo:**` com o valor gravado no `tema.md`. Se o tipo for `qualitativos` ou `nenhum`, troque as duas
  linhas de caixa da seção por `- não se aplica`.
- **Se o checklist existente não tiver as seções `## Dados` ou `## Formatação ABNT`** (versão anterior
  do kit), insira-as no lugar do esqueleto acima, no estado inicial, sem mexer nas outras seções.
- **Se o arquivo existir mas não bater com o formato esperado** (seção removida, cabeçalho alterado, não
  reconhecível): não sobrescreva sem avisar. Avise o aluno explicitamente que `tcc-kit/checklist.md`
  existe mas não bate com o formato esperado, e pergunte se quer que a skill recrie o esqueleto (perdendo
  o que foi editado manualmente) ou se prefere corrigir o arquivo manualmente antes de continuar — mesmo
  padrão que `iniciar-tcc` já usa pra `tcc-kit/tema.md` corrompido.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — escolher-tema
Tema definido: "<tema confirmado>".
```
