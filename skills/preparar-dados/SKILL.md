---
name: preparar-dados
description: Use quando o aluno quiser limpar ou preparar os dados brutos do TCC antes da análise -- "limpa meus dados", "prepara o dataset", "trata os valores faltando", "meus dados estão bagunçados", ou quando iniciar-tcc sugerir preparar os dados. Faz o perfil dos arquivos, propõe cada decisão de limpeza com o motivo e o número de linhas afetadas, e só executa o que o aluno aprovar, com um script em tcc/dados/ que nunca grava sobre o dado bruto. Não se aplica a TCC com dados qualitativos ou sem dados.
---

# Preparar Dados — limpeza explicada e aprovada

Dado bruto quase nunca está pronto: valor faltando, categoria escrita de dois jeitos, número que veio
como texto, linha repetida. Cada correção muda os números do TCC, então cada uma precisa de um motivo
e da aprovação do aluno. Esta skill propõe, o aluno decide, e o que foi feito fica registrado com a
contagem real de linhas afetadas.

Regras que valem do começo ao fim:

- **Nunca grava sobre o dado bruto.** O resultado vai para um arquivo novo, `<nome>-limpo.csv`.
- **Só executa depois da aprovação** do aluno (Passo 4).
- **Nunca instala nada no ambiente do aluno**: execução sempre com `uv run --with`.
- **Git, só leitura.**
- Comandos que funcionem no PowerShell do Windows: para criar pasta ou copiar arquivo, use `uv run
  python -c "..."` com `pathlib`/`shutil`, nunca `mkdir -p` ou `cp`.

Os scripts do plugin (`perfil_dados.py`, `estado_projeto.py`) seguem a mesma regra de caminho de
`revisao-bibliografica`: procure-os relativos à raiz deste plugin e não invente um caminho. Sem `uv`
disponível: diga ao aluno que esta skill precisa dele (instalação na documentação do curso) e pare.

## Passo 1 — Aplicabilidade

Leia `tcc-kit/tema.md` e o campo **Dados**.

- `qualitativos` ou `nenhum`: diga em uma ou duas frases que a preparação de dados estruturados não se
  aplica a este TCC, e pare. Não crie nenhum arquivo.
- Campo ausente (tema de versão anterior): se houver algum arquivo em `tcc/dados/`, considere
  `estruturados` e grave `**Dados:** estruturados` no `tema.md`, logo depois de `**Área/curso:**`;
  senão, pergunte ao aluno qual dos três tipos descreve o TCC, grave, e aplique a regra acima.
- Sem `tema.md`: siga, tratando como `estruturados`.

## Passo 2 — Inventário

Liste os arquivos de dado em `tcc/dados/` (`.csv`, `.tsv`, `.xlsx`), ignorando os que terminam em
`-limpo.csv`. Nenhum arquivo: peça ao aluno para colocar os dados brutos em `tcc/dados/` e pare.

Arquivo `.xlsx`: converta cada planilha para CSV numa cópia, sem tocar o original:

```bash
uv run --with pandas --with openpyxl python -c "import pandas as pd, pathlib; p=pathlib.Path('tcc/dados/<arquivo>.xlsx'); [df.to_csv(p.with_name(f'{p.stem}-{nome}.csv'), index=False) for nome, df in pd.read_excel(p, sheet_name=None).items()]"
```

## Passo 3 — Perfil

Para cada arquivo:

```bash
uv run "<caminho do plugin>/scripts/perfil_dados.py" "tcc/dados/<arquivo>"
```

Nunca leia o arquivo de dados inteiro na conversa. Se precisar ver valores de uma coluna específica
(para achar categorias escritas de jeitos diferentes), conte com um comando curto:

```bash
uv run --with pandas python -c "import pandas as pd; df=pd.read_csv('tcc/dados/<arquivo>', sep=None, engine='python', decimal=','); print(df['<coluna>'].value_counts(dropna=False).head(30))"
```

Use `decimal=','` quando o perfil indicar número com vírgula.

## Passo 4 — Proposta e aprovação

Monte uma tabela, uma decisão por linha:

| # | Coluna | Problema | Decisão proposta | Por quê | Linhas afetadas |
|---|---|---|---|---|---|

Problemas a procurar: valor faltando, tipo errado (número como texto, data como texto), linha
duplicada, categoria escrita de jeitos diferentes, espaço sobrando, valor impossível (idade negativa,
percentual acima de 100).

Para cada decisão, prefira a opção que menos altera os dados e diga a alternativa quando houver uma
escolha real (ex.: remover as 11 linhas sem mensalidade, ou manter e excluir só das análises dessa
coluna). Informe quantas linhas o arquivo tem e quantas sobrariam se todas as decisões fossem
aplicadas.

Pergunte quais decisões aplicar: todas, algumas, ou alguma com mudança. **Pare aqui e termine a sua
resposta com essa pergunta.** Nada de script, execução ou gravação antes de o aluno responder.

## Passo 5 — Script

Com a resposta, escreva `tcc/dados/preparar_dados.py` só com as decisões aprovadas:

- lê o arquivo bruto com os mesmos parâmetros usados no perfil (`sep`, `decimal`, `encoding`);
- um bloco por decisão, começando com o comentário `# Decisão <n>: <resumo>`;
- em cada bloco, imprime `Decisão <n>: <k> linha(s) afetada(s)`, com `k` calculado pelo próprio script;
- imprime linhas e colunas antes e depois;
- grava `tcc/dados/<nome>-limpo.csv` (separador `,`, decimal `.`, UTF-8).

Se `tcc/dados/preparar_dados.py` já existir, faça backup antes de sobrescrever:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" backup tcc/dados/preparar_dados.py
```

## Passo 6 — Executar

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" foto --saida tcc-kit/dados/.foto-preparacao.json tcc/dados
uv run --with pandas python tcc/dados/preparar_dados.py
uv run "<caminho do plugin>/scripts/estado_projeto.py" comparar tcc-kit/dados/.foto-preparacao.json tcc/dados
```

O arquivo `-limpo.csv` aparece como novo: esperado. Se algum **arquivo bruto** aparecer como
`alterado` ou `removido`, avise o aluno antes de qualquer outra coisa.

Se o script falhar, mostre as últimas linhas do erro, corrija **o script** (nunca o dado) e rode de
novo. Se falhar duas vezes, pare e explique o problema ao aluno.

## Passo 7 — Relatório

Grave `tcc-kit/dados/limpeza.md` (crie a pasta se preciso; backup antes se o arquivo existir), com os
números impressos pelo script, nunca estimados:

```markdown
# Preparação dos dados
Gerado por preparar-dados em <data>. Script: tcc/dados/preparar_dados.py.

**Entrada:** tcc/dados/<arquivo> (<linhas> linhas, <colunas> colunas)
**Saída:** tcc/dados/<nome>-limpo.csv (<linhas> linhas, <colunas> colunas)

## Decisões aplicadas
1. <coluna>: <o que foi feito>. <k> linha(s) afetada(s). Motivo: <por quê>.

## Decisões recusadas pelo aluno
- <decisão> (ou "nenhuma")

## Para você conferir
1. <pergunta sobre a decisão de maior impacto no número de linhas>
2. <pergunta sobre uma conversão de tipo ou de categoria>
3. <pergunta sobre algo que o aluno conhece e o perfil não mostra, ex.: se um valor extremo é real>
```

## Passo 8 — Registrar

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" registrar --etapa preparacao --saida tcc-kit/dados/limpeza.md --entradas tcc/dados/<arquivos brutos> tcc/dados/preparar_dados.py
```

Se `tcc-kit/checklist.md` existir: na seção `## Dados`, marque
`- [x] Preparados (tcc-kit/dados/limpeza.md)` e atualize a linha final para
`Atualizado em: <data de hoje, AAAA-MM-DD>, por: preparar-dados`. Se a seção `## Dados` não existir
(checklist de versão anterior), insira antes de `## Referências`:

```markdown
## Dados
**Tipo:** estruturados
- [x] Preparados (tcc-kit/dados/limpeza.md)
- [ ] Resumo real (tcc/dados/resumo-real.md)
```

Se o checklist não existir, não crie.

Acrescente no fim de `tcc-kit/historico.md` (crie com `# Histórico — TCC` se não existir):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — preparar-dados
<n> decisões aplicadas, <m> recusadas. <linhas antes> → <linhas depois> linhas. Relatório:
tcc-kit/dados/limpeza.md.
```

Resuma ao aluno em poucas linhas: linhas antes e depois, a decisão de maior impacto, e as 3 perguntas
de "Para você conferir". Sugira o próximo passo: referências (`revisao-bibliografica` ou
`adicionar-referencias`) e depois `validar-metodologia`. O script de preparação vai ser executado de
novo pela `reproduzir-dados` quando ela montar o resumo de dados.
