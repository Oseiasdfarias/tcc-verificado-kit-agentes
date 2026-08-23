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

## Passo 2 — Despachar o guardiao-consistencia

Use a ferramenta Task para despachar o agente `guardiao-consistencia` **uma única vez**, passando o
conteúdo de TODOS os capítulos lidos no Passo 1 juntos (não um despacho por capítulo — este agente
precisa ver tudo simultaneamente pra comparar entre capítulos). Espere o relatório antes de continuar.

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
[relatório completo do agente, do Passo 2]

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
