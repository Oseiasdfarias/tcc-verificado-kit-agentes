---
name: iniciar-tcc
description: Use quando o aluno perguntar por onde começar ou continuar, sem especificar o quê -- "por onde eu continuo?", "o que falta no meu TCC?", "vamos começar meu TCC", "me ajuda a organizar os próximos passos". Detecta em que estágio o aluno está (configuração institucional? template escolhido? tema definido? referências verificadas? metodologia validada? capítulo planejado? capítulo escrito?) e sugere o próximo passo mais lógico.
---

# Iniciar TCC — detecta o estágio e sugere o próximo passo

Esta skill nunca decide sozinha o que fazer — ela olha o que já existe no projeto, resume isso pro
aluno, e pergunta se ele quer seguir a sugestão ou fazer outra coisa. Automatiza a detecção, nunca a
decisão.

## Passo 1 — Verificar configuração do projeto

Confira se `tcc-kit/config.md` existe.

## Passo 2 — Verificar template

Confira se `tcc-kit/template.md` existe.
- Se `tcc-kit/config.md` também existir, compare a data em `Definido em` (config.md) com a data em
  `Última adaptação` (template.md). Se `Definido em` for mais recente, marque como "config atualizado
  depois da última adaptação".

## Passo 3 — Verificar tema

Confira se `tcc-kit/tema.md` existe.
- Se não existir: sem tema definido.
- Se existir: leia o arquivo e extraia o valor do campo **Tema**.
- Se o arquivo existir mas não for possível extrair um valor claro do campo **Tema** (arquivo
  corrompido, editado manualmente fora do formato esperado, campo ausente): não trave nem invente um
  valor. Avise o aluno explicitamente que `tcc-kit/tema.md` existe mas não conseguiu ler o tema dele, e
  pergunte como prosseguir (corrigir o arquivo manualmente, ou rodar `escolher-tema` de novo).

## Passo 4 — Verificar referências

Confira se `tcc-kit/referencias/index.yaml` existe. Se existir, conte quantas entradas têm
`status: verificado`.

Critério exato: zero entradas verificadas, ou arquivo ausente, conta como "sem referências". Uma ou
mais conta como "com referências".

## Passo 5 — Verificar metodologia

Confira se `tcc-kit/metodologia.md` existe.

Critério exato: arquivo ausente conta como "sem metodologia definida". Arquivo presente conta como "com
metodologia definida" — mesmo se o método ainda não tiver sido executado (`Status: Pendente de
execução`), o registro já existe e cobre o gap que esta etapa detecta.

## Passo 6 — Verificar plano e escrita de capítulo

Se o aluno já indicou (ou você já souber de uma interação anterior nesta conversa) qual capítulo está
em foco, confira, pra esse capítulo, e registre os dois sinais separadamente — o Passo 7 usa a
combinação dos dois pra escolher entre a ramificação 8 e a 9:
- **Plano aprovado?** `tcc-kit/capitulos/<slug>/plano.md` existe?
- **Conteúdo real escrito?** `tcc/capitulos/<slug>.tex` existe e tem conteúdo real escrito? Critério:
  não é um limite fixo de caracteres — é leitura de julgamento (mesmo tipo que `revisor-forma` já faz
  hoje), verificando se há texto real, não só o placeholder que o template deixou.

Se o aluno ainda não indicou nenhum capítulo específico, pule este passo — as ramificações 8 e 9 abaixo
só se aplicam quando já se sabe qual capítulo está em jogo.

## Passo 7 — Apresentar o estado e perguntar

Os passos acima detectam várias coisas ao mesmo tempo, mas você só apresenta **uma** sugestão por vez
— a do estágio mais cedo que ainda falta, nesta ordem de prioridade:

**1. Sem configuração:**
> "Ainda não tenho os dados do seu projeto (universidade, curso, orientador). Quer que eu colete isso
> agora?"

Se confirmado, continue seguindo o que a skill `configurar-projeto` orienta.

**2. Com configuração, sem template:**
> "Vi que seus dados estão configurados. Ainda não escolhemos um template LaTeX pro seu projeto. Quer
> que eu ajude a encontrar um da sua universidade, ou prefere já usar o padrão do curso?"

Se confirmado, continue seguindo o que a skill `escolher-template` orienta — como o aluno já respondeu
aqui se quer buscar um template da universidade ou usar o padrão do curso, leve essa resposta direto
pro Passo 2 dela, sem repetir a pergunta lá.

**3. Configuração atualizada depois da última adaptação do template:**
> "Vi que você atualizou os dados do projeto depois da última vez que o template foi adaptado. Quer
> que eu reaplique os dados atualizados no template agora?"

Se confirmado, continue seguindo o que a skill `escolher-template` orienta — a opção de só readaptar
com os dados atuais (oferecida quando já existe um `tcc-kit/template.md`) cobre esse caso.

**4. Sem tema:**
> "Ainda não vejo um tema definido pro seu TCC. Quer que eu te ajude a escolher um agora?"

Se confirmado, continue seguindo o que a skill `escolher-tema` orienta.

**5. Com tema, sem referências:**
> "Vi que seu tema é '<tema de tcc-kit/tema.md>'. Você ainda não tem nenhuma referência verificada na
> base. Quer que eu busque referências sobre esse tema agora?"

Se confirmado, continue seguindo o que a skill `revisao-bibliografica` orienta — use os "Termos de
busca sugeridos" de `tcc-kit/tema.md` como ponto de partida, deixando claro ao aluno que ele pode pedir
outros termos.

**6. Com tema e referências, sem metodologia definida:**
> "Vi que seu tema é '<tema>' e você já tem <N> referência(s) verificada(s). Ainda não vejo uma
> abordagem metodológica definida pro seu TCC. Quer que eu te ajude a decidir (ou confirmar) o método
> certo agora?"

Se confirmado, continue seguindo o que a skill `validar-metodologia` orienta.

**7. Com tema, referências e metodologia, sem plano pro capítulo em foco (ou nenhum capítulo em foco
ainda):**
> "Vi que seu tema é '<tema>' e você já tem <N> referência(s) verificada(s). Quer planejar algum
> capítulo agora? (introdução, referencial teórico, metodologia, resultados, ou
> discussão/considerações finais)"

Se o aluno indicar um capítulo, continue seguindo o que a skill `planejar-capitulo` orienta, já
passando o capítulo escolhido.

**8. Plano aprovado pro capítulo em foco, mas ainda sem conteúdo real escrito:**
> "Vi que você já tem um plano aprovado pro capítulo de <nome do capítulo>, mas ele ainda não foi
> escrito. Quer que eu escreva agora?"

Se confirmado, continue seguindo o que a skill `escrever-capitulo` orienta, já passando o capítulo em
foco.

**9. Capítulo em foco já escrito (plano aprovado e conteúdo real):**
> "Vi que o capítulo de <nome do capítulo> já está escrito. Quer que eu rode a auditoria completa
> (`revisar-capitulo`) antes de você considerar pronto?"

Se confirmado, continue seguindo o que a skill `revisar-capitulo` orienta, já passando o capítulo em
foco.

## Nunca decida e execute no mesmo passo

Sempre espere a resposta do aluno depois de apresentar o estado — mesmo quando a sugestão parece óbvia.
Se o aluno responder com algo fora da sugestão apresentada (ex: pedir pra revisar um capítulo já
escrito em vez de seguir a sugestão), siga o que ele pediu em vez de insistir na sugestão original.
