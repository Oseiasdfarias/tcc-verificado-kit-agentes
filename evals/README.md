# Evals — suíte de avaliação das skills

Cada skill deste kit é um prompt, não código executável, então não existe "roda os testes e
recebe verde/vermelho" automático — nem a própria Anthropic oferece isso pronto pra esse formato
(ver `docs/superpowers/...` sobre o assunto, no repositório `curso-tcc-ia`). O que esta pasta dá é
o que falta hoje: um jeito de **rodar de novo, de forma consistente**, os mesmos cenários sempre
que uma skill for editada, em vez de depender de lembrar de testar manualmente — foi exatamente a
falta disso que deixou a Aula 2.0 do curso dizendo "cinco agentes" por um tempo depois do kit já
ter sete.

## Formato de um cenário

Cada arquivo `.json` dentro de `evals/<skill>/` descreve uma situação:

```json
{
  "skill": "escrever-capitulo",
  "title": "modo rápido usa só o dado real disponível",
  "query": "escreve minha introdução",
  "turns": ["escreve minha introdução", "rápido"],
  "fixtures": {
    "tcc-kit/capitulos/introducao/plano.md": "conteúdo do arquivo...",
    "tcc/dados/resumo-real.md": "conteúdo do arquivo..."
  },
  "setup_script": "opcional -- comando bash rodado no diretório de trabalho antes do primeiro turno, útil pra gerar um arquivo binário (ex: um PDF real de teste)",
  "expected_behavior": [
    "Frase específica e verificável sobre o que a skill deveria fazer",
    "..."
  ]
}
```

Campos:
- `skill`: nome da skill sendo testada (só documentação, o `run_eval.py` não usa pra roteamento).
- `query` **ou** `turns`: uma mensagem única, ou uma lista de mensagens enviadas em sequência
  (usa `--resume` entre elas — é assim que se testa uma skill que faz uma pergunta antes de agir,
  como o modo `co-piloto`/`rápido` de `escrever-capitulo`).
- `fixtures`: arquivos de texto a criar no diretório de trabalho antes do primeiro turno.
- `setup_script`: opcional, comando de shell pra fixture que não é texto simples (ex: gerar um PDF
  real com `uv run --with reportlab`).
- `expected_behavior`: lista de afirmações concretas e verificáveis — não "a skill funciona bem",
  e sim algo como "usa só o número 26,5% de resumo-real.md, nenhum outro número inventado".

## Rodando

```bash
# um cenário
python3 evals/run_eval.py evals/escrever-capitulo/scenario-1-modo-rapido-grounding.json

# todos os cenários de uma skill
python3 evals/run_eval.py evals/escrever-capitulo/

# a suíte inteira (34 cenários, ~1-2min cada -- roda sequencial, não em paralelo)
python3 evals/run_eval.py evals/
```

Cada cenário roda num diretório temporário isolado (nunca no repositório do plugin, nunca em um
projeto de TCC real), com `claude -p --plugin-dir <este repo> --dangerously-skip-permissions`.
No final, o script imprime a resposta de cada turno, a árvore de arquivos resultante, e a lista de
`expected_behavior` como checklist — a conferência de cada item é manual (ler a resposta e os
arquivos gerados contra o que a lista descreve). Use `--keep` pra manter o diretório temporário e
inspecionar os arquivos depois que o script terminar.

## Quando rodar

- Depois de editar qualquer `SKILL.md` ou `agents/*.md` — pelo menos os cenários da(s) skill(s)
  tocada(s), pra pegar regressão antes de publicar uma versão nova.
- Antes de um bump de versão maior (mudança de comportamento, não só correção de digitação).

## Cobertura atual

34 cenários: 2 por skill pras 12 skills originais, um caminho feliz e um caso de
guarda-corrim (grounding anti-alucinação, tratamento de erro, ou uma decisão condicional que a
própria skill documenta), mais 3 pra `estado-tcc` e 4 da v1.11 (rodada 2 com delta, backup, e dois
cenários que chamam `revisor-citacoes` e `guardiao-metodo` direto, em linguagem natural), e 3 da
v1.12 pra `reproduzir-dados` (um deles chama o `guardiao-dados` direto). Os outros
agentes não são cobertos isoladamente (rodam via `Task`, despachados por uma skill), e a suíte não
tem grader automático — é o degrau mínimo real acima de "testei uma vez na mão e esqueci", não uma
suíte exaustiva.
