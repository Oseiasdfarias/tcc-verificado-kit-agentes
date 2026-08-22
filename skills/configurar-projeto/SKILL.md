---
name: configurar-projeto
description: Use quando for a primeira vez configurando um projeto de TCC, ou quando o aluno quiser atualizar dados institucionais (universidade, curso, orientador, banca) -- "configura meu projeto", "define minha universidade e orientador", "atualiza os dados da minha banca". Coleta os dados institucionais que outros estágios do kit usam (ex: adaptar um template).
---

# Configurar Projeto — coleta os dados institucionais do TCC

Esta skill coleta os dados que identificam o projeto do aluno perante a universidade — usados depois
por `escolher-template` pra adaptar a capa/folha de rosto. Não força resposta pra dado que ainda não
existe (banca, por exemplo, normalmente só é definida mais tarde).

## Passo 1 — Checar configuração existente

Confira se `tcc-kit/config.md` já existe.

- Se existir: mostre todos os dados atuais e pergunte o que o aluno quer fazer. Aceite tanto um
  pedido específico ("atualiza a banca", "muda o orientador") quanto um pedido genérico ("quero revisar
  tudo de novo"). Pra cada campo que ele indicar, faça a pergunta correspondente do Passo 2 (a mesma
  pergunta, incluindo `Banca` — que o Passo 2 não cobre no fluxo do zero: se o aluno pedir pra atualizar
  a banca aqui, pergunte os nomes dos membros diretamente). Não recolete campos que ele não pediu pra
  mudar — mantenha os valores atuais deles como estão. Depois de coletar as respostas dos campos
  indicados, pule direto pro Passo 4 (Salvar), atualizando só esses campos e preservando os demais.
- Se não existir: siga pro Passo 2 (fluxo normal, do zero).

## Passo 2 — Perguntar, um de cada vez

Nesta ordem, uma pergunta por mensagem (não despeje todas de uma vez):

1. Universidade.
2. Curso/programa.
3. Orientador(a) — se o aluno já souber quem é; se não, registre como "a definir".
4. Nome completo do aluno.
5. Cidade.
6. Ano previsto de conclusão.

Banca fica de fora deste fluxo — normalmente ainda não existe nesse estágio inicial do projeto. Se o
aluno mencionar a banca espontaneamente, registre; senão, deixe como "a definir" sem perguntar. Quando a
banca for definida, o aluno pode rodar esta skill de novo e pedir pra atualizar só esse campo (Passo 1).

## Passo 3 — Logo da universidade

Pergunte se o aluno já tem o arquivo da logo/brasão da universidade salvo em algum lugar.
- Se tiver: peça o caminho do arquivo.
- Se não tiver: sugira que ele busque no site oficial da universidade (geralmente na seção de
  identidade visual/marca, ou no manual de normalização de trabalhos acadêmicos). **Nunca busque ou
  baixe uma logo sozinho** — é um documento acadêmico real, uma logo errada ou desatualizada é um erro
  visível e embaraçoso. Se o aluno não tiver o arquivo agora, registre "não informado" e siga em frente
  — ele pode voltar e rodar esta skill de novo depois.

## Passo 4 — Salvar

Crie `tcc-kit/config.md` (na primeira vez) ou atualize, dentro do arquivo já existente, só os campos
indicados no Passo 1 (numa atualização parcial), preservando os demais como estavam:

```markdown
# Configuração do Projeto
**Universidade:** <nome>
**Curso/Programa:** <nome>
**Orientador(a):** <nome, ou "a definir">
**Banca:** <nomes, ou "a definir">
**Aluno:** <nome completo>
**Cidade:** <cidade>
**Ano previsto de conclusão:** <ano>
**Logo:** <caminho do arquivo, ou "não informado">
Definido em: <data de hoje, AAAA-MM-DD>
```

`Definido em` é sempre a data de hoje, mesmo numa atualização parcial — não a data da primeira vez que o
arquivo foi criado.

## Passo 5 — Resumo final

Confirme ao aluno o que foi salvo (ou, numa atualização parcial, o que mudou especificamente). Se algum
campo ficou "a definir" ou "não informado", mencione isso explicitamente e avise que ele pode rodar esta
skill de novo mais tarde pra completar só esse campo (ex: quando a banca for definida) — sem precisar
refazer os outros.
