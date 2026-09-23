---
name: reproduzir-dados
description: Use quando o aluno precisar montar ou atualizar o resumo de dados real do TCC (tcc/dados/resumo-real.md) a partir dos próprios dados e scripts -- "monta meu resumo de dados", "roda meus scripts e confere os números", "de onde vieram os números do meu TCC?", "atualizei os dados, refaz o resumo". Inventaria dados e código, executa os scripts Python que já existem (em ambiente isolado), lê o código com perguntas dirigidas e grava o resumo com a procedência de cada número e a lista do que não existe como dado. Análise nova só com confirmação do aluno.
---

# Reproduzir Dados — resumo real com procedência

O kit inteiro confia em `tcc/dados/resumo-real.md`: `escrever-capitulo` só escreve número que está
nele, e `guardiao-dados` só aceita número que bate com ele. Esta skill monta esse arquivo **a partir do
que os dados e os scripts do aluno realmente produzem**, e não do que o aluno lembra ou do que o texto
já diz. Cada número sai com a procedência (script, linha, comando), e o que não foi medido fica
registrado como tal.

Regras que valem do começo ao fim:

- **Só executa scripts que já existem** no projeto, e só depois de o aluno confirmar quais (Passo 3).
  Análise nova só depois de mostrar ao aluno o que vai calcular e ele confirmar (Passo 7).
- **Nunca edita script do aluno** nem grava sobre arquivo de dado.
- **Nunca instala nada no ambiente do aluno** (`pip install`, `conda install`): execução sempre com
  `uv run`, que isola as dependências.
- **Git, só leitura** (`status`, `log`, `diff`, `show`), e nunca encadeado com outro comando.
- **MATLAB, R, Octave, C/C++, firmware**: só leitura, nunca execução.

Os comandos abaixo usam scripts do plugin. O caminho do plugin segue a mesma regra de
`revisao-bibliografica`: procure `scripts/estado_projeto.py` e `scripts/perfil_dados.py` relativos à raiz
deste plugin, e não invente um caminho. Se o `uv` não estiver disponível, siga só com leitura (Passos 2,
3 e 5), sem perfil nem execução, e diga no resumo que os números não foram reproduzidos.

## Passo 1 — Estado anterior

Se `tcc-kit/dados/materiais.yaml` existir, esta não é a primeira execução. Rode:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" verificar
```

Na linha da etapa `reproducao`, a coluna `alterados` lista os dados e scripts que mudaram desde a
última reprodução. **Só esses** precisam ser perfilados, relidos e reexecutados; para os demais,
reaproveite o resumo de `materiais.yaml` e a linha correspondente do `resumo-real.md` atual. Se a etapa
estiver `atual`, diga ao aluno que nada mudou desde a última reprodução e pergunte se ele quer refazer
mesmo assim ou só acrescentar algo (ex: um número novo).

## Passo 2 — Inventário (sem abrir conteúdo)

Com Glob, fora de `tcc-kit/`, `.git/`, `.venv/`, `venv/`, `env/`, `node_modules/` e `__pycache__/`:

| Categoria | Padrões |
|---|---|
| Dados | `*.csv`, `*.tsv`, `*.json`, `*.mat`, `*.xlsx`, `*.txt` em pastas de dados ou logs |
| Scripts executáveis | `*.py`, `*.ipynb` |
| Código só de leitura | `*.m`, `*.R`, `*.c`, `*.cpp`, `*.h`, `*.ino` |
| Dependências | `requirements.txt`, `pyproject.toml`, `environment.yml` |

Se passar de 40 arquivos, pergunte ao aluno quais pastas importam antes de seguir.

## Passo 3 — Confirmar com o aluno

Mostre o inventário agrupado e pergunte: quais arquivos são os dados usados no TCC, e quais scripts
produzem os números que vão para o texto. Pergunte também se há algum número que o texto precisa e que
ele não sabe de onde vem.

**Pare aqui e termine a sua resposta com essa pergunta.** Nada de perfil, execução ou gravação antes de
o aluno responder, **mesmo que o inventário pareça óbvio** (um CSV e um script só, por exemplo).
Executar um script roda código no computador do aluno, com efeitos que você não controla; ele precisa
saber o que vai rodar antes que rode. Se o pedido do aluno já nomeou os arquivos e autorizou a execução
("os dados são X, o script é Y, pode rodar"), isso conta como a resposta, e você pode seguir.

Quando a escolha for fechada e couber em 2 a 4 opções, use a ferramenta AskUserQuestion (opção
recomendada primeiro); se não estiver disponível, ou se a lista for maior, pergunte em texto, listando os
arquivos.

## Passo 4 — Perfil dos dados

Para cada CSV/TSV confirmado:

```bash
uv run "<caminho do plugin>/scripts/perfil_dados.py" "<arquivo>"
```

**Nunca leia o CSV inteiro** para descrevê-lo: o perfil dá linhas, colunas, faixa e média, e 3 linhas de
amostra. Para outros formatos, registre só nome e tamanho, a menos que um script confirmado os leia (aí
a descrição vem do código).

## Passo 5 — Leitura dirigida do código

Leia cada script confirmado (e o código só de leitura relevante) procurando responder, e anote a linha
de cada resposta:

1. De qual arquivo lê os dados, e que colunas usa?
2. Que parâmetros fixos usa (constantes, janelas, limiares, ordem de modelo, período de amostragem)?
3. Em que unidade está cada grandeza?
4. Como divide os dados (treino/validação/teste, janelas, segmentos) e onde escolhe parâmetros?
5. Que números imprime ou salva, e onde?
6. Usa semente aleatória? Qual?
7. O que o código faz de diferente do que o nome ou o comentário dizem? (ex: um sinal chamado de PRBS
   que é outra coisa, um índice que pode sair do vetor)

Em projeto com git, para cada script: `git log -1 --format=%h -- <script>` (só esse comando, sem
encadear) dá o commit da versão lida.

## Passo 6 — Executar os scripts confirmados

Para cada script Python confirmado, nesta ordem:

1. **Foto e backup** (uma vez, antes do primeiro script):

   ```bash
   uv run "<caminho do plugin>/scripts/estado_projeto.py" foto --saida tcc-kit/dados/.foto-reproducao.json .
   uv run "<caminho do plugin>/scripts/estado_projeto.py" backup <arquivos de dado confirmados>
   ```

2. **Executar**, no diretório onde o script espera rodar (o do próprio script, se ele usa caminhos
   relativos a si):
   - com `requirements.txt` no projeto: `uv run --with-requirements requirements.txt python <script>`;
   - sem: `uv run --with <pacotes que o script importa, fora da biblioteca padrão> python <script>`.

   Notebook (`.ipynb`): não execute; leia as células de código como no Passo 5.
3. **Conferir**, depois de todos os scripts:

   ```bash
   uv run "<caminho do plugin>/scripts/estado_projeto.py" comparar tcc-kit/dados/.foto-reproducao.json .
   ```

   Arquivos novos gerados pelos scripts (figuras, CSVs de resultado) são esperados: registre-os. Se
   algum **arquivo de dado confirmado** aparecer como `alterado` ou `removido`, avise o aluno antes de
   qualquer outra coisa, com o caminho do backup.
4. **Falha** (código diferente de 0): registre comando, código e as últimas linhas do erro, siga com a
   leitura do código, e não tente consertar o script. Os números que dependiam dele ficam fora de
   "Resultados" e são mencionados ao aluno como pendentes.

Registre cada execução em `tcc-kit/dados/reproducao.md` (crie com o cabeçalho
`# Reprodução dos dados` se não existir; acrescente sempre no fim), numerando R1, R2… a partir da última
existente:

```markdown
## R<n> — <data e hora, AAAA-MM-DD HH:MM> — <script>
**Comando:** `<comando exato>`
**Código de saída:** <código>
**Script:** sha256 <12 primeiros caracteres> · commit <hash curto, ou "sem git">
**Dados:** <arquivo> sha256 <12 primeiros caracteres> (um por linha)
**Saída relevante:** <só as linhas com os números que vão para o resumo>
```

Os hashes vêm de `estado_projeto.py hash <arquivos>`, nunca de cálculo seu.

## Passo 7 — Lacunas e análise nova

Para cada número que o aluno pediu no Passo 3 (ou que o capítulo já escrito afirma, se ele pediu
conferência) e que nenhum script produziu:

1. **Proponha** a análise: o que calcular, a partir de quais arquivos e colunas, com que método, e onde
   o script novo ficaria (`tcc/dados/analises/<nome>.py`).
2. **Espere a confirmação.** Sem confirmação explícita, não crie nem execute nada: o item vai para "O
   que não existe como dado".
3. Com confirmação: escreva o script novo (arquivo novo; nunca edite script existente), execute com o
   protocolo do Passo 6 e registre como mais uma execução em `reproducao.md`.

## Passo 8 — Gravar o resumo

**Se `tcc/dados/resumo-real.md` já existir**: faça backup (`estado_projeto.py backup
tcc/dados/resumo-real.md`) e pergunte se o aluno quer substituir ou mesclar. Na mescla: linha antiga
confirmada pela reprodução ganha a procedência; linha antiga sem procedência que a reprodução não
confirmou fica marcada "fornecido pelo aluno, sem procedência"; linha antiga que **diverge** de um
número reproduzido é mostrada ao aluno, lado a lado, antes de gravar, e ele decide.

Formato:

```markdown
# Resumo real dos dados
Gerado por reproduzir-dados em <data>. Procedência completa: tcc-kit/dados/reproducao.md.

## Conjuntos de dados
- <arquivo>: <o que é, linhas, colunas relevantes, período/unidade>

## Resultados
- <número ou afirmação, com unidade> — <script:linha> [R<n>]
- <número informado pelo aluno> — fornecido pelo aluno, sem procedência

## O que não existe como dado
- <afirmação que o texto não pode fazer, e por quê>
```

- **Resultados**: um número por linha, com unidade e com a procedência. Arredonde como o script
  imprime; se o texto for usar outro arredondamento, anote o valor completo.
- **O que não existe como dado**: tudo que o aluno pediu e não foi calculado, e tudo que o código mostra
  que **não** foi medido mas que costuma aparecer em texto desse tipo de trabalho (ex: "não há medição de
  jitter", "o custo do protótipo não foi registrado", "a eficácia pedagógica não foi avaliada"). Esta
  seção é o que impede o capítulo de afirmar o que não foi medido.

Grave também `tcc-kit/dados/materiais.yaml`, uma entrada por arquivo do inventário confirmado:

```yaml
- caminho: <caminho relativo à raiz>
  tipo: dado          # dado | script | codigo | dependencias
  resumo: <uma linha, até 220 caracteres>
  sha256: <da saída de estado_projeto.py hash>
```

Na execução incremental (Passo 1), mantenha as entradas que não mudaram como estão.

## Passo 9 — Registrar e resumir

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" registrar --etapa reproducao --saida tcc/dados/resumo-real.md --entradas <todos os arquivos de dado e script confirmados>
```

Com isso, `estado-tcc` avisa quando algum dado ou script mudar depois deste resumo. Se o comando falhar,
avise em uma linha e siga.

Acrescente no fim de `tcc-kit/historico.md` (crie com `# Histórico — TCC` se não existir):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — reproduzir-dados
N scripts executados (M com falha), K números com procedência, J itens em "O que não existe como
dado". Resumo: tcc/dados/resumo-real.md. Execuções: tcc-kit/dados/reproducao.md.
```

Não edite `tcc-kit/checklist.md`: a metodologia passa a "Definida e executada" pelo campo `Status` de
`tcc-kit/metodologia.md`, que é da skill `validar-metodologia`. Se esse campo estiver "Pendente de
execução" e a reprodução produziu resultados, sugira ao aluno atualizá-lo.

Informe ao aluno, em poucas linhas: quantos números entraram com procedência, o que ficou em "O que não
existe como dado", qualquer divergência entre o que ele lembrava e o que o script produziu, e qualquer
coisa que o código faz de diferente do que o nome diz (Passo 5, pergunta 7). Sugira `revisar-capitulo`
nos capítulos que já usam esses números.
