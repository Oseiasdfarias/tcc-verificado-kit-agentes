<p align="center">
  <img src="https://img.shields.io/badge/claude%20code-plugin-C98A52?style=for-the-badge&logo=anthropic&logoColor=white">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white">
  <img src="https://img.shields.io/badge/versão-1.6.0-4A2712?style=for-the-badge">
  <img src="https://img.shields.io/badge/licença-uso%20livre%2C%20sem%20revenda-4A2712?style=for-the-badge">
</p>

<p align="center">
  <img width="220" src="assets/logo-kit.png" alt="Kit de Agentes — três passadas de revisão">
</p>

<p align="center">
  <a href="#como-funciona">Como funciona</a> •
  <a href="#ferramentas">Ferramentas</a> •
  <a href="#instalar">Instalar</a> •
  <a href="#o-que-tem-no-kit">O que tem no kit</a> •
  <a href="#atualizar">Atualizar</a>
</p>

<h3 align="center">Kit de Agentes</h3>
<p align="center">Revise seu TCC contra dado inventado, citação falsa e argumento fraco.</p>

---

## Sobre

Plugin do Claude Code com agentes especialistas, um motor de revisão bibliográfica e uma camada de
orquestração adaptativa que sugere o próximo passo guiado, pra escrever e revisar um TCC sem dado
inventado, citação falsa ou argumento fraco — parte do método ensinado no curso
[TCC Verificado](https://tccverificado.com.br).

## Como funciona

```mermaid
flowchart TD
    Aluno["Aluno<br/>(linguagem natural)"] --> Hub1["iniciar-tcc<br/>(detecta estágio, sugere)"]

    Hub1 --> S1["1. configurar-projeto"]
    Hub1 --> S2["2. escolher-template"]
    Hub1 --> S3["3. escolher-tema"]
    Hub1 --> S4["4. revisao-bibliografica"]
    Hub1 --> S5["5. validar-metodologia"]
    Hub1 --> S6["6. planejar-capitulo"]
    Hub1 --> S7["7. escrever-capitulo"]

    S7 --> Hub2["revisar-capitulo<br/>(auditoria completa)"]
    Hub2 --> Agentes["6 agentes especialistas<br/>(dados, citações, método, argumento, forma)"]

    Hub2 --> S8["8. auditoria-tcc-completo"]
    S8 --> S9["9. preparar-defesa"]

    classDef hub fill:#ffd8a8,stroke:#e8590c,stroke-width:2px,color:#1e1e1e
    classDef hub2 fill:#a5d8ff,stroke:#1971c2,stroke-width:2px,color:#1e1e1e
    classDef skill fill:#b2f2bb,stroke:#2f9e44,stroke-width:2px,color:#1e1e1e
    classDef agente fill:#eebefa,stroke:#9c36b5,stroke-width:2px,color:#1e1e1e

    class Hub1 hub
    class Hub2 hub2
    class S1,S2,S3,S4,S5,S6,S7,S8,S9 skill
    class Agentes agente
```

`iniciar-tcc` é só um atalho pra quem não sabe por onde começar — nenhuma das 9 skills numeradas
fica presa a passar por ela primeiro, e `revisar-capitulo` pode ser chamada a qualquer momento,
direto. Cada skill salva o que produz em `tcc-kit/` (ou edita `tcc/`, no caso de
`escolher-template`/`escrever-capitulo`) — detalhes na seção "O que tem no kit" abaixo.

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
> https://docs.astral.sh/uv/getting-started/installation/. Os outros 7 agentes, a skill
> `revisar-capitulo` e as skills de orquestração (`iniciar-tcc`, `configurar-projeto`,
> `escolher-template`, `escolher-tema`, `validar-metodologia`, `planejar-capitulo`,
> `escrever-capitulo`, `auditoria-tcc-completo`, `preparar-defesa`) não precisam disso.

## O que tem no kit

### Por onde começar

Não sabe por onde continuar? Peça "por onde eu continuo?" ou "vamos começar meu TCC" — a skill
`iniciar-tcc` olha o que você já tem em `tcc-kit/` e sugere o próximo passo: configurar o projeto,
escolher um template, escolher tema, buscar referências, validar a metodologia, planejar um capítulo,
escrever um capítulo já planejado, auditar o TCC inteiro, ou preparar a defesa. Nenhuma dessas etapas
fica presa a essa skill — você pode pedir qualquer uma delas direto, a qualquer momento.

### Configurar o projeto

Primeira coisa a fazer num projeto novo: peça "configura meu projeto" — a skill `configurar-projeto`
coleta universidade, curso, orientador e outros dados institucionais, e salva em
`tcc-kit/config.md`. Você pode rodar de novo mais tarde pra completar dados que ainda não tinha (ex: a
banca, quando for definida).

### Escolher template

Peça "acha um template LaTeX pra minha universidade" — a skill `escolher-template` pesquisa no
Overleaf, te mostra as opções encontradas (mais o link da galeria geral, pra você pesquisar sozinho se
preferir), orienta o download (sempre manual — o Overleaf não permite baixar automaticamente), e adapta
a capa do template com os dados de `tcc-kit/config.md`, preenchendo com placeholder o que ainda não
tiver definido.

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

### Validar metodologia

Antes de rodar sua análise ou escrever sobre o método, peça "valida minha metodologia" ou "que teste eu
uso pra isso?" — a skill `validar-metodologia` cobre qualquer tipo de TCC (quantitativo, qualitativo,
bibliográfico/teórico, ou misto). Você escolhe: define o método você mesmo, ou aponta uma base real
(dataset, entrevistas, documentos) pra ela analisar e propor. Em qualquer um dos casos, explica os
pressupostos/critérios de rigor do método antes de salvar em `tcc-kit/metodologia.md`.

### Planejar um capítulo

Antes de escrever de verdade, peça "planeja o capítulo de [nome]" — a skill `planejar-capitulo` propõe
uma estrutura de seções, o argumento de cada uma, e quais referências já validadas entram em cada
seção. Você aprova ou pede ajuste antes do plano ser salvo em
`tcc-kit/capitulos/<capítulo>/plano.md`.

### Escrever um capítulo

Depois do plano aprovado, peça "escreve minha introdução" (ou qualquer outro capítulo) — a skill
`escrever-capitulo` transforma o plano em prosa de verdade. Você escolhe o modo: `co-piloto` (ela
pergunta antes de escrever cada seção, pra usar seu raciocínio de verdade) ou `rápido` (escreve direto
do plano, com o mínimo de perguntas) — sua escolha fica salva como padrão em `tcc-kit/config.md`, mas
dá pra trocar pontualmente a qualquer momento ("escreve rápido dessa vez"). Nos dois modos, todo dado
vem de `tcc/dados/resumo-real.md` e toda citação vem de referência já verificada — nunca inventa
nenhum dos dois. Sempre sugere `revisar-capitulo` no final, antes de considerar o capítulo pronto.

### Os 6 agentes de revisão

| Agente | O que faz |
|---|---|
| `guardiao-dados` | Confere se números e afirmações do capítulo batem com os dados reais do seu projeto |
| `revisor-citacoes` | Pesquisa cada citação na web, confirma se a referência existe, e sugere buscas quando encontra lacuna |
| `guardiao-metodo` | Confere se o método descrito no capítulo bate com o validado, e se a conclusão não extrapola o que o método permite |
| `orientador-rigoroso` | Aponta afirmação sem sustentação e salto de lógica no argumento |
| `banca-critica` | Simula perguntas difíceis de banca examinadora |
| `revisor-forma` | Gramática, registro acadêmico ABNT, e tiques de escrita de IA |

### Auditoria completa

Peça "audita esse capítulo antes de eu considerar pronto" — a skill `revisar-capitulo` roda os 6
agentes na ordem certa (dado e citação primeiro, são bloqueantes; argumento e forma depois) e
consolida tudo num relatório único, incluindo qualquer lacuna de referência encontrada.

### Auditoria do TCC completo

Depois que todos os capítulos estiverem escritos, peça "confere meu TCC inteiro antes de eu entregar"
— a skill `auditoria-tcc-completo` lê todos os capítulos de uma vez (não um por um) e confere o que
nenhum dos 6 agentes de `revisar-capitulo` consegue ver isoladamente: se todo objetivo da Introdução foi
respondido na Discussão, se números que você mesmo relata batem entre capítulos, e se a terminologia se
mantém estável. Inclui também um lembrete de itens que variam por instituição (ficha catalográfica,
folha de aprovação) e o curso não padroniza.

### Preparar apresentação de defesa

Com o TCC pronto, peça "me ajuda a preparar a defesa" — a skill `preparar-defesa` gera uma apresentação
em Beamer a partir dos capítulos já aprovados (nunca inventa conteúdo novo pro slide) e um material de
perguntas prováveis da banca, reaproveitando o `banca-critica` sobre o TCC inteiro.

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
