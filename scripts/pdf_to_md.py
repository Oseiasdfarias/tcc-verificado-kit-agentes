#!/usr/bin/env python3
"""Converte um PDF em Markdown usando pdfplumber (extracao de texto pura,
sem binario externo). Ver secao "Tratamento de erro" de
docs/superpowers/specs/2026-08-21-motor-referencias-bibliograficas-design.md
no repo curso-tcc-ia.

pdfplumber cobre bem a maioria dos PDFs digitais de artigo academico --
texto e tabela simples, sem precisar de nenhum binario externo nem modelo
de ML (funciona igual em qualquer sistema operacional, sem instalacao
extra alem do proprio uv). Quando a saida fica curta/vazia demais (sinal
de PDF escaneado, ou pagina com formula/layout complexo demais pra
extracao de texto simples), este script nao tenta nenhum OCR -- devolve o
codigo de saida 3, e quem chama (a skill) deve pedir pro proprio agente
ler o PDF original diretamente (ferramenta de leitura nativa, que ja
entende imagem/formula/tabela) e escrever o Markdown a mao. Isso elimina
qualquer dependencia de binario externo ou instalacao extra pro aluno.

Uso:
    uv run --with pdfplumber scripts/pdf_to_md.py <entrada.pdf> <saida.md>

Codigo de saida:
    0 -- conversao ok (texto extraido tem tamanho razoavel)
    1 -- arquivo de entrada nao existe, ou uso incorreto dos argumentos
    2 -- conversao rodou mas levantou uma excecao (ex: PDF corrompido)
    3 -- conversao rodou sem erro, mas a saida ficou curta/vazia demais --
         provavel PDF escaneado, ou pagina com formula/layout complexo
         demais. Quem chama deve pedir pro agente ler o PDF original
         direto e escrever o Markdown a mao, sem instalar nada.
"""
import sys
from pathlib import Path

MIN_OUTPUT_CHARS = 200


def is_output_too_short(markdown_text: str, min_chars: int = MIN_OUTPUT_CHARS) -> bool:
    """Funcao pura, testavel sem rodar pdfplumber de verdade -- decide se um
    texto convertido e curto/vazio demais pra ser um artigo academico real."""
    return len(markdown_text.strip()) < min_chars


def convert(input_path: Path, output_path: Path) -> str:
    """Extrai o texto de input_path com pdfplumber e escreve em output_path.
    Levanta FileNotFoundError se input_path nao existir. Qualquer outra
    excecao de extracao sobe direto -- quem chama trata.

    Retorna o texto extraido (pode ser curto/vazio -- quem chama decide se
    isso e aceitavel via is_output_too_short)."""
    if not input_path.exists():
        raise FileNotFoundError(f"arquivo de entrada nao encontrado: {input_path}")

    import pdfplumber

    partes = []
    with pdfplumber.open(str(input_path)) as pdf:
        for page in pdf.pages:
            texto_pagina = page.extract_text()
            if texto_pagina:
                partes.append(texto_pagina)

    markdown_text = "\n\n".join(partes)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_text, encoding="utf-8")
    return markdown_text


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"uso: {argv[0]} <entrada.pdf> <saida.md>", file=sys.stderr)
        return 1

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    try:
        markdown_text = convert(input_path, output_path)
    except FileNotFoundError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"erro: conversao falhou -- {e}", file=sys.stderr)
        return 2

    if is_output_too_short(markdown_text):
        print(
            f"aviso: saida tem so {len(markdown_text.strip())} caracteres -- "
            f"provavel PDF escaneado, ou pagina com formula/layout complexo. "
            f"Peca pro agente ler o PDF original direto e escrever o Markdown a mao.",
            file=sys.stderr,
        )
        return 3

    print(f"ok: {output_path} ({len(markdown_text)} caracteres)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
