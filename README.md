<p align="center">
  <img src="https://img.shields.io/badge/claude%20code-plugin-C98A52?style=for-the-badge&logo=anthropic&logoColor=white">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white">
  <img src="https://img.shields.io/badge/versão-1.1.0-4A2712?style=for-the-badge">
  <img src="https://img.shields.io/badge/licença-uso%20livre%2C%20sem%20revenda-4A2712?style=for-the-badge">
</p>

<p align="center">
  <img width="220" src="assets/logo-kit.png" alt="Kit de Agentes — três passadas de revisão">
</p>

<p align="center">
  <a href="#ferramentas">Ferramentas</a> •
  <a href="#instalar">Instalar</a> •
  <a href="#o-que-tem-no-kit">O que tem no kit</a> •
  <a href="#atualizar">Atualizar</a>
</p>

<h3 align="center">Kit de Agentes</h3>
<p align="center">Revise seu TCC contra dado inventado, citação falsa e argumento fraco.</p>

---

## Sobre

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
| YAML | Formato do índice de referências (`tcc-kit/referencias/index.yaml`) |

## Instalar

Dentro do Claude Code, no terminal do seu projeto de TCC:

```bash
/plugin marketplace add Oseiasdfarias/tcc-verificado-kit-agentes
/plugin install tcc-kit@tcc-verificado-kit-agentes
```

Se pedir `/reload-plugins`, rode esse comando também.

> **Requisito extra pra `revisao-bibliografica`:** essa skill converte PDF em Markdown usando `uv`
> (gerenciador de pacotes Python). Instale antes de usar essa skill — veja o comando pro seu sistema em
> https://docs.astral.sh/uv/getting-started/installation/. Os outros 5 agentes e a skill
> `revisar-capitulo` não precisam disso.

## O que tem no kit

### Por onde começar

Não sabe por onde continuar? Peça "por onde eu continuo?" ou "vamos começar meu TCC" — a skill
`iniciar-tcc` olha o que você já tem em `tcc-kit/` e sugere o próximo passo: escolher tema, buscar
referências, ou planejar um capítulo. Nenhuma dessas etapas fica presa a essa skill — você pode pedir
qualquer uma delas direto, a qualquer momento.

### Escolher tema

Ainda não tem tema? Peça "me ajuda a escolher um tema" — a skill `escolher-tema` conversa com você até
convergir num tema específico e salva em `tcc-kit/tema.md`, já com termos de busca sugeridos pra
alimentar a próxima etapa.

### Revisão bibliográfica

Peça "busca referências sobre [seu tema]" a qualquer momento — a skill `revisao-bibliografica` busca
artigos reais, mostra os candidatos pra você confirmar, baixa o PDF quando possível (ou te dá a lista
de links pra baixar manualmente), converte pra Markdown, e mantém tudo indexado em
`tcc-kit/referencias/index.yaml`. Essa base é o que a escrita consulta pra nunca inventar referência — e
ela cresce ao longo do processo: se faltar uma referência no meio da escrita, o `revisor-citacoes`
sugere buscar mais, você confirma.

### Planejar um capítulo

Antes de escrever de verdade, peça "planeja o capítulo de [nome]" — a skill `planejar-capitulo` propõe
uma estrutura de seções, o argumento de cada uma, e quais referências já validadas entram em cada
seção. Você aprova ou pede ajuste antes do plano ser salvo em
`tcc-kit/capitulos/<capítulo>/plano.md`.

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

### Usar um agente específico

Peça em linguagem natural — "revisa esse capítulo como banca", "confere se esses dados batem", "revisa
a forma/português desse texto".

## Regra que vale pra todos

Nenhum agente edita seu texto — só relata. A decisão sobre o que mudar, e sobre qual referência entra
na base, é sempre sua (ver Aula 3.2 do curso: "raciocínio não se terceiriza").

## Licença

Uso livre para escrever seu próprio trabalho, incluindo em contexto acadêmico/institucional. Não é
permitido vender este software nem incluí-lo em curso, mentoria ou produto educacional pago de
terceiros. Ver [LICENSE.md](LICENSE.md).

## Atualizar

```bash
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```

Ver [CHANGELOG.md](CHANGELOG.md) pra histórico de versões.

---

<p align="center">
  <sub>Parte do curso <a href="https://tccverificado.com.br">TCC Verificado</a></sub>
</p>
