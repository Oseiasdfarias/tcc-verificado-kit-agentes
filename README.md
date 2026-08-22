# Kit de Agentes — TCC Verificado

Plugin do Claude Code com 5 agentes especialistas e uma skill de auditoria completa, pra revisar seu
TCC contra dado inventado, citação falsa, argumento fraco e tique de escrita de IA — parte do método
ensinado no curso [TCC Verificado](https://tccverificado.com.br).

## Instalar

Dentro do Claude Code, no terminal do seu projeto de TCC:

```
/plugin marketplace add Oseiasdfarias/tcc-verificado-kit-agentes
/plugin install tcc-kit@tcc-verificado-kit-agentes
```

Se pedir `/reload-plugins`, rode esse comando também.

## Usar

- **Auditoria completa de um capítulo**: peça "audita esse capítulo antes de eu considerar pronto" —
  a skill `revisar-capitulo` roda os 5 agentes na ordem certa e salva um relatório único.
- **Um agente específico**: peça em linguagem natural — "revisa esse capítulo como banca", "confere se
  esses dados batem", "revisa a forma/português desse texto".

## Os 5 agentes

| Agente | O que faz |
|---|---|
| `guardiao-dados` | Confere se números e afirmações do capítulo batem com os dados reais do seu projeto |
| `revisor-citacoes` | Pesquisa cada citação na web, confirma se a referência existe, e sugere buscas quando encontra lacuna |
| `orientador-rigoroso` | Aponta afirmação sem sustentação e salto de lógica no argumento |
| `banca-critica` | Simula perguntas difíceis de banca examinadora |
| `revisor-forma` | Gramática, registro acadêmico ABNT, e tiques de escrita de IA |

## Revisão bibliográfica

Peça "busca referências sobre [seu tema]" a qualquer momento — a skill `revisao-bibliografica` busca
artigos reais, mostra os candidatos pra você confirmar, baixa o PDF quando possível (ou te dá a lista
de links pra baixar manualmente), converte pra Markdown, e mantém tudo indexado em
`tcc/referencias/index.yaml`. Essa base é o que a escrita consulta pra nunca inventar referência — e
ela cresce ao longo do processo: se faltar uma referência no meio da escrita, o `revisor-citacoes`
sugere buscar mais, você confirma.

## Regra que vale pra todos

Nenhum agente edita seu texto — só relata. A decisão sobre o que mudar é sempre sua (ver Aula 3.2 do
curso: "raciocínio não se terceiriza").

## Atualizar

```
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```
