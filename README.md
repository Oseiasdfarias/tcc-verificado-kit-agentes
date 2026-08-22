# Kit de Agentes — TCC Verificado

[![Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-C98A52)](https://github.com/Oseiasdfarias/tcc-verificado-kit-agentes)
[![Versão](https://img.shields.io/badge/versão-1.1.0-4A2712)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3-3776AB?logo=python&logoColor=white)](scripts/pdf_to_md.py)

Plugin do Claude Code com agentes especialistas e um motor de revisão bibliográfica, pra escrever e
revisar um TCC sem dado inventado, citação falsa ou argumento fraco — parte do método ensinado no
curso [TCC Verificado](https://tccverificado.com.br).

## Ferramentas

| Ferramenta | Uso |
|---|---|
| [Claude Code](https://claude.com/claude-code) | Ambiente onde o plugin roda — agentes, skills, subagentes |
| [Semantic Scholar API](https://api.semanticscholar.org/) | Busca estruturada de artigos acadêmicos reais (metadado + link de acesso aberto) |
| [marker](https://github.com/datalab-to/marker) | Conversão de PDF pra Markdown, com reconhecimento de fórmula/equação em LaTeX |
| [uv](https://docs.astral.sh/uv/) | Executa o script de conversão sem instalação manual de dependência Python |
| YAML | Formato do índice de referências (`tcc/referencias/index.yaml`) |

## Instalar

Dentro do Claude Code, no terminal do seu projeto de TCC:

```
/plugin marketplace add Oseiasdfarias/tcc-verificado-kit-agentes
/plugin install tcc-kit@tcc-verificado-kit-agentes
```

Se pedir `/reload-plugins`, rode esse comando também.

**Requisito extra pra `revisao-bibliografica`:** essa skill converte PDF em Markdown usando `uv`
(gerenciador de pacotes Python). Instale antes de usar essa skill — veja o comando pro seu sistema em
https://docs.astral.sh/uv/getting-started/installation/. Os outros 5 agentes e a skill
`revisar-capitulo` não precisam disso.

## O que tem no kit

### Revisão bibliográfica

Peça "busca referências sobre [seu tema]" a qualquer momento — a skill `revisao-bibliografica` busca
artigos reais, mostra os candidatos pra você confirmar, baixa o PDF quando possível (ou te dá a lista
de links pra baixar manualmente), converte pra Markdown, e mantém tudo indexado em
`tcc/referencias/index.yaml`. Essa base é o que a escrita consulta pra nunca inventar referência — e
ela cresce ao longo do processo: se faltar uma referência no meio da escrita, o `revisor-citacoes`
sugere buscar mais, você confirma.

### Os 5 agentes de revisão

| Agente | O que faz |
|---|---|
| `guardiao-dados` | Confere se números e afirmações do capítulo batem com os dados reais do seu projeto |
| `revisor-citacoes` | Pesquisa cada citação na web, confirma se a referência existe, e sugere buscas quando encontra lacuna |
| `orientador-rigoroso` | Aponta afirmação sem sustentação e salto de lógica no argumento |
| `banca-critica` | Simula perguntas difíceis de banca examinadora |
| `revisor-forma` | Gramática, registro acadêmico ABNT, e tiques de escrita de IA |

### Auditoria completa

Peça "audita esse capítulo antes de eu considerar pronto" — a skill `revisar-capitulo` roda os 5
agentes na ordem certa (dado e citação primeiro, são bloqueantes; argumento e forma depois) e
consolida tudo num relatório único, incluindo qualquer lacuna de referência encontrada.

## Usar um agente específico

Peça em linguagem natural — "revisa esse capítulo como banca", "confere se esses dados batem", "revisa
a forma/português desse texto".

## Regra que vale pra todos

Nenhum agente edita seu texto — só relata. A decisão sobre o que mudar, e sobre qual referência entra
na base, é sempre sua (ver Aula 3.2 do curso: "raciocínio não se terceiriza").

## Atualizar

```
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```

Ver [CHANGELOG.md](CHANGELOG.md) pra histórico de versões.
