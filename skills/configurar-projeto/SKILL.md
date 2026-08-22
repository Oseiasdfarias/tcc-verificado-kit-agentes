---
name: configurar-projeto
description: Use quando for a primeira vez configurando um projeto de TCC, ou quando o aluno quiser atualizar dados institucionais (universidade, curso, orientador, banca) -- "configura meu projeto", "define minha universidade e orientador", "atualiza os dados da minha banca". Coleta os dados institucionais que outros estágios do kit usam (ex: adaptar um template).
---

# Configurar Projeto — coleta os dados institucionais do TCC

Esta skill coleta os dados que identificam o projeto do aluno perante a universidade — usados depois
por `escolher-template` pra adaptar a capa/folha de rosto. Não força resposta pra dado que ainda não
existe (banca, por exemplo, normalmente só é definida mais tarde).

## Passo 1 — Perguntar, um de cada vez

Nesta ordem, uma pergunta por mensagem (não despeje todas de uma vez):

1. Universidade.
2. Curso/programa.
3. Orientador(a) — se o aluno já souber quem é; se não, registre como "a definir".
4. Nome completo do aluno.
5. Cidade.
6. Ano previsto de conclusão.

Banca fica de fora deste fluxo — normalmente ainda não existe nesse estágio inicial do projeto. Se o
aluno mencionar a banca espontaneamente, registre; senão, deixe como "a definir" sem perguntar.

## Passo 2 — Logo da universidade

Pergunte se o aluno já tem o arquivo da logo/brasão da universidade salvo em algum lugar.
- Se tiver: peça o caminho do arquivo.
- Se não tiver: sugira que ele busque no site oficial da universidade (geralmente na seção de
  identidade visual/marca, ou no manual de normalização de trabalhos acadêmicos). **Nunca busque ou
  baixe uma logo sozinho** — é um documento acadêmico real, uma logo errada ou desatualizada é um erro
  visível e embaraçoso. Se o aluno não tiver o arquivo agora, registre "não informado" e siga em frente
  — ele pode voltar e rodar esta skill de novo depois.

## Passo 3 — Checar configuração existente

Confira se `tcc-kit/config.md` já existe.
- Se existir: mostre os dados atuais, pergunte se o aluno quer atualizar (sobrescrever) ou manter como
  está. Nunca sobrescreva sem essa confirmação explícita.
- Se não existir: siga direto pro Passo 4.

## Passo 4 — Salvar

Crie (ou sobrescreva, se confirmado no Passo 3) `tcc-kit/config.md`:

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

`Definido em` é sempre a data de hoje, mesmo numa atualização — não a data da primeira vez que o
arquivo foi criado.

## Passo 5 — Resumo final

Confirme ao aluno o que foi salvo. Se algum campo ficou "a definir" ou "não informado", mencione isso
explicitamente e avise que ele pode rodar esta skill de novo mais tarde pra completar (ex: quando a
banca for definida).
