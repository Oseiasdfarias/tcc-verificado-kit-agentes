<p align="center">
  <img src="https://img.shields.io/badge/claude%20code-plugin-C98A52?style=for-the-badge&logo=anthropic&logoColor=white">
  <img src="https://img.shields.io/badge/versão-1.13.0-4A2712?style=for-the-badge">
  <img src="https://img.shields.io/badge/licença-uso%20livre%2C%20sem%20revenda-4A2712?style=for-the-badge">
</p>

<p align="center">
  <img width="220" src="assets/logo-kit.png" alt="Kit de Agentes — três passadas de revisão">
</p>

<h3 align="center">Kit de Agentes</h3>
<p align="center">Revise seu TCC contra dado inventado, citação falsa e argumento fraco.</p>

---

## Sobre

Plugin do Claude Code que acompanha o curso [TCC Verificado](https://tccverificado.com.br). Ele reúne
agentes especialistas que ajudam a escrever e revisar um TCC com dado real, referência que existe de
verdade e argumento que se sustenta.

O jeito de usar o kit em cada etapa do trabalho é ensinado no curso.

## O que ele faz

- Confere se os números do texto batem com os seus dados.
- Confere se cada referência citada existe.
- Revisa método, argumento e forma, como um orientador e uma banca fariam.
- Mantém um registro do andamento do trabalho.

O kit relata e sugere. Nenhum agente edita o seu texto, e a decisão sobre o que mudar é sempre sua.

## Instalar

Dentro do Claude Code, no terminal do seu projeto:

```bash
/plugin marketplace add Oseiasdfarias/tcc-verificado-kit-agentes
/plugin install tcc-kit@tcc-verificado-kit-agentes
```

Se pedir `/reload-plugins`, rode esse comando também.

Se você usa o Claude Code pela extensão do VS Code, o comando `/plugin` não existe ali. Rode no
terminal do sistema e depois recarregue a janela do VS Code:

```bash
claude plugin marketplace add Oseiasdfarias/tcc-verificado-kit-agentes
claude plugin install tcc-kit@tcc-verificado-kit-agentes
```

Algumas partes do kit usam o [uv](https://docs.astral.sh/uv/getting-started/installation/). Instale
antes de começar.

## Atualizar

```bash
/plugin marketplace update tcc-verificado-kit-agentes
/plugin update tcc-kit@tcc-verificado-kit-agentes
```

Pela extensão do VS Code, no terminal do sistema: `claude plugin marketplace update
tcc-verificado-kit-agentes` e `claude plugin update tcc-kit@tcc-verificado-kit-agentes`.

O histórico de versões está no [CHANGELOG.md](CHANGELOG.md).

## Licença

Uso livre para escrever seu próprio trabalho, incluindo em contexto acadêmico ou institucional. Não é
permitido vender este software nem incluí-lo em curso, mentoria ou produto educacional pago de
terceiros. Ver [LICENSE.md](LICENSE.md).

---

<p align="center">
  <sub>Parte do curso <a href="https://tccverificado.com.br">TCC Verificado</a></sub>
</p>
