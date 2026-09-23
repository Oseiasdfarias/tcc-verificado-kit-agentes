---
name: auditoria-tcc-completo
description: Use quando o aluno quiser uma auditoria do TCC inteiro, não só um capítulo -- "confere meu TCC inteiro antes de eu entregar", "os capítulos estão consistentes entre si?", "quero uma visão geral antes da defesa". Lê todos os capítulos com conteúdo real de uma vez, confere consistência cross-capítulo, e inclui um lembrete de itens institucionais que variam por universidade.
---

# Auditoria Completa do TCC — consistência entre capítulos e checklist institucional

Esta skill lê o TCC inteiro — não capítulo a capítulo — e confere o que nenhum dos 6 agentes de
`revisar-capitulo` consegue ver isoladamente: se os capítulos, juntos, formam um documento coerente.

## Passo 1 — Ler os capítulos disponíveis

Pra cada um dos 5 slugs fixos (`introducao`, `referencial-teorico`, `metodologia`, `resultados`,
`discussao-consideracoes-finais`), confira se `tcc/capitulos/<slug>.tex` existe e tem conteúdo real —
mesmo critério de julgamento de leitura que `iniciar-tcc` e `revisor-forma` já usam (não é limite fixo
de caracteres, é conferir se há texto real, não só o placeholder do template).

Leia o conteúdo de todos os que existirem com conteúdo real. Se algum dos 5 estiver ausente ou vazio,
anote quais — a auditoria segue com o que existir, mas alguns achados do `guardiao-consistencia` (como
"objetivo respondido na Discussão") dependem de capítulos específicos existirem pra fazer sentido.

**Capítulo curto é conteúdo real.** Um parágrafo, ou mesmo uma frase de texto do aluno (e não o
placeholder do template), conta. Com **pelo menos 1 capítulo** com conteúdo real, a auditoria roda e o
relatório é salvo, mesmo que o TCC pareça cedo demais pra uma auditoria completa: não cabe a você
decidir que "não vale a pena". Se achar o TCC incipiente, diga isso no resumo ao aluno, depois de
salvar o relatório. A única situação que dispensa o relatório é zero capítulos com conteúdo real (ver
"Tratamento de erro").

## Passo 2 — Despachar o guardiao-consistencia

Antes do despacho, tire a foto do projeto (trava: o agente pode gravar só o próprio relatório):

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" foto --saida tcc-kit/relatorios/_brutos/auditoria-completa-<data>/.foto.json tcc tcc-kit
```

O caminho do plugin segue a mesma regra de `revisao-bibliografica`: procure `scripts/estado_projeto.py`
relativo à raiz deste plugin, e não invente um caminho. Se o comando falhar, siga sem a trava e registre
no relatório que a conferência de integridade não rodou.

Use a ferramenta Task para despachar o agente `guardiao-consistencia` **uma única vez**, passando os
**caminhos** de TODOS os capítulos com conteúdo real do Passo 1 (não o conteúdo: ele lê os arquivos
sozinho, e colar o texto na instrução dobraria o custo) e o caminho do relatório
`tcc-kit/relatorios/_brutos/auditoria-completa-<data>/guardiao-consistencia.md`, dizendo que ele deve
gravar ali e devolver só as 3 linhas. Um despacho só, não um por capítulo: este agente precisa ver tudo
junto pra comparar entre capítulos.

Depois que ele terminar, rode `estado_projeto.py comparar
tcc-kit/relatorios/_brutos/auditoria-completa-<data>/.foto.json tcc tcc-kit`. Se listar qualquer
arquivo, avise o aluno antes de qualquer outra coisa, com a lista, e sugira conferir e restaurar esses
arquivos; o mesmo aviso vai no topo do relatório. Se o agente devolveu o relatório inteiro na resposta
em vez de gravar, grave você mesmo no caminho do bruto.

## Passo 3 — Montar o checklist institucional

Sem nenhum agente, monte este bloco fixo:

```markdown
## Checklist institucional (lembrete — Aula 3.1)

Itens que variam por instituição e o curso não padroniza — confira com sua secretaria/orientador:
- [ ] Ficha catalográfica (se sua instituição exige)
- [ ] Folha de aprovação com campo de assinatura da banca
- [ ] Limite de páginas (se houver)
- [ ] Capa com brasão/identidade visual da instituição no formato exigido
- [ ] Outros requisitos específicos do seu curso/departamento
```

## Passo 4 — Consolidar e salvar

Salve em `tcc-kit/relatorios/auditoria-completa-<data>.md` (data no formato AAAA-MM-DD):

```markdown
# Auditoria completa — TCC — [data]

## Capítulos avaliados
[Liste os slugs com conteúdo real encontrados no Passo 1. Se algum dos 5 estiver ausente ou vazio,
liste aqui explicitamente com uma nota de que a auditoria é parcial nesse ponto -- ex: "discussao-
consideracoes-finais: ausente -- não foi possível conferir se os objetivos da Introdução foram
respondidos".]

## Consistência entre capítulos (guardiao-consistencia)
[Só as linhas de achado do agente, pegas com Grep no bruto pelo padrão `^- \*\*CONS-[0-9]+\*\*`, na
ordem em que aparecem (não abra o bruto inteiro). Se não houver nenhuma: "nenhuma inconsistência
encontrada entre os capítulos avaliados". Termine com o link pro relatório completo:
`_brutos/auditoria-completa-<data>/guardiao-consistencia.md`.]

## Checklist institucional (lembrete — Aula 3.1)
[bloco do Passo 3]

---
Revisado por IA — a decisão final é sua (TCC Verificado, Aula 3.2).
```

Informe ao aluno o caminho do relatório salvo e um resumo de 2-3 frases: quantos capítulos foram
avaliados (de 5), quantos achados de consistência o `guardiao-consistencia` encontrou, e se algum
capítulo ficou de fora da auditoria por ainda não existir.

## Tratamento de erro

- **Nenhum capítulo com conteúdo real ainda**: avise que não há nada pra auditar ainda, sugira
  `escrever-capitulo` primeiro — não gere um relatório vazio.
- **Só alguns dos 5 capítulos existem**: rode normalmente com o que existir, listando explicitamente o
  que falta (Passo 4).

## Passo 4b — Registrar a versão das entradas

Só se o relatório foi salvo no Passo 4. Rode:

```bash
uv run "<caminho do plugin>/scripts/estado_projeto.py" registrar --etapa auditoria-completa --saida tcc-kit/relatorios/auditoria-completa-<data>.md --entradas tcc/capitulos/introducao.tex tcc/capitulos/referencial-teorico.tex tcc/capitulos/metodologia.tex tcc/capitulos/resultados.tex tcc/capitulos/discussao-consideracoes-finais.tex
```

Passe sempre os 5 caminhos, mesmo os que não existem: o script registra a ausência, e se um capítulo
que faltava passar a existir, a auditoria aparece como desatualizada (ela não cobriu esse capítulo).
O caminho do plugin segue a mesma regra de `revisao-bibliografica`: procure
`scripts/estado_projeto.py` relativo à raiz deste plugin, e não invente um caminho.

Isso grava em `tcc-kit/.estado.json` a versão exata dos capítulos auditados, pra skill `estado-tcc`
conseguir avisar depois que algum capítulo mudou desde a auditoria. Não leia `tcc-kit/.estado.json` nem
mostre a saída do comando ao aluno.

- **Comando falhou** (`uv` ausente, script não encontrado, código diferente de 0 e de 2): avise em uma
  linha que o registro de versão não foi gravado e siga para o Passo 5. O relatório já está salvo.
- **Código 2** (`tcc-kit/.estado.json` ilegível): avise o aluno e pergunte se quer apagar o arquivo
  (perdendo os registros de versão) ou corrigir à mão. Não apague sem confirmação. Siga para o Passo 5
  em qualquer caso.

## Passo 5 — Atualizar checklist e histórico

**Se o Passo 1 não encontrou nenhum capítulo com conteúdo real** (caso descrito em "Tratamento de
erro" — a skill recusou gerar o relatório), não atualize nem o checklist nem o histórico — nada foi
produzido.

Conte quantos achados a seção "Consistência entre capítulos (guardiao-consistencia)" do relatório que
acabou de ser salvo (Passo 4) lista no total, somando as 3 categorias (Objetivos, Números,
Terminologia).

Confira se `tcc-kit/checklist.md` existe.

- **Se não existir**, crie com o esqueleto completo abaixo, com a seção "Auditoria completa do TCC" já
  marcada (as demais seções ficam no estado inicial, como no esqueleto):

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
- [x] Rodada em <data de hoje, AAAA-MM-DD> (N achado(s) de consistência)

## Apresentação de defesa
- [ ] Nunca gerada

---
Atualizado em: <data de hoje, AAAA-MM-DD>, por: auditoria-tcc-completo
```

- **Se já existir**, edite só a seção "Auditoria completa do TCC" pra `- [x] Rodada em <data de hoje,
  AAAA-MM-DD> (N achado(s) de consistência)` (preservando as demais seções como estão), e atualize a
  linha final pra `Atualizado em: <data de hoje, AAAA-MM-DD>, por: auditoria-tcc-completo`.
- **Se o arquivo existir mas não bater com o formato esperado** (seção removida, cabeçalho alterado, não
  reconhecível): não sobrescreva sem avisar. Avise o aluno explicitamente que `tcc-kit/checklist.md`
  existe mas não bate com o formato esperado, e pergunte se quer que a skill recrie o esqueleto (perdendo
  o que foi editado manualmente) ou se prefere corrigir o arquivo manualmente antes de continuar — mesmo
  padrão que `iniciar-tcc` já usa pra `tcc-kit/tema.md` corrompido.

Confira se `tcc-kit/historico.md` existe.

- **Se não existir**, crie com o cabeçalho `# Histórico — TCC`.
- Acrescente, sempre no final do arquivo (nunca edite uma entrada antiga):

```markdown

## <data e hora de agora, AAAA-MM-DD HH:MM> — auditoria-tcc-completo
Auditoria completa rodada. N achado(s) de consistência (guardiao-consistencia). M de 5 capítulos
avaliados. Relatório: tcc-kit/relatorios/auditoria-completa-<data>.md.
```

Preencha `M` com a contagem de capítulos listados na seção "Capítulos avaliados" do relatório (Passo 1
da skill).
