---
name: iniciar-tcc
description: Use quando o aluno perguntar por onde começar ou continuar, sem especificar o quê -- "por onde eu continuo?", "o que falta no meu TCC?", "vamos começar meu TCC", "me ajuda a organizar os próximos passos". Detecta em que estágio o aluno está (tema definido? referências verificadas?) e sugere o próximo passo mais lógico.
---

# Iniciar TCC — detecta o estágio e sugere o próximo passo

Esta skill nunca decide sozinha o que fazer — ela olha o que já existe no projeto, resume isso pro
aluno, e pergunta se ele quer seguir a sugestão ou fazer outra coisa. Automatiza a detecção, nunca a
decisão.

## Passo 1 — Verificar tema

Confira se `tcc-kit/tema.md` existe.
- Se não existir: sem tema definido.
- Se existir: leia o arquivo e extraia o valor do campo **Tema**.

## Passo 2 — Verificar referências

Confira se `tcc-kit/referencias/index.yaml` existe. Se existir, conte quantas entradas têm
`status: verificado`.

Critério exato: zero entradas verificadas, ou arquivo ausente, conta como "sem referências". Uma ou
mais conta como "com referências".

## Passo 3 — Apresentar o estado e perguntar

Resuma o que você encontrou em 1-2 frases e sugira o próximo passo — sempre como pergunta:

**Sem tema:**
> "Ainda não vejo um tema definido pro seu TCC. Quer que eu te ajude a escolher um agora?"

Se confirmado, continue seguindo o que a skill `escolher-tema` orienta.

**Com tema, sem referências:**
> "Vi que seu tema é '<tema de tcc-kit/tema.md>'. Você ainda não tem nenhuma referência verificada na
> base. Quer que eu busque referências sobre esse tema agora?"

Se confirmado, continue seguindo o que a skill `revisao-bibliografica` orienta — use os "Termos de
busca sugeridos" de `tcc-kit/tema.md` como ponto de partida, deixando claro ao aluno que ele pode pedir
outros termos.

**Com tema e referências:**
> "Vi que seu tema é '<tema>' e você já tem <N> referência(s) verificada(s). Quer planejar algum
> capítulo agora? (introdução, referencial teórico, metodologia, resultados, ou
> discussão/considerações finais)"

Se o aluno indicar um capítulo, continue seguindo o que a skill `planejar-capitulo` orienta, já
passando o capítulo escolhido.

## Nunca decida e execute no mesmo passo

Sempre espere a resposta do aluno depois de apresentar o estado — mesmo quando a sugestão parece óbvia.
Se o aluno responder com algo fora das 3 sugestões (ex: pedir pra revisar um capítulo já escrito em vez
de seguir a sugestão), siga o que ele pediu em vez de insistir na sugestão original.
