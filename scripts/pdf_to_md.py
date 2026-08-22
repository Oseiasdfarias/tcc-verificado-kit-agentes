#!/usr/bin/env python3
"""Converte um PDF em Markdown usando marker, validando que a saida nao ficou
vazia/curta demais antes de reportar sucesso. Ver secao "Tratamento de erro"
de docs/superpowers/specs/2026-08-21-motor-referencias-bibliograficas-design.md
no repo curso-tcc-ia.

Uso:
    uv run --with marker-pdf scripts/pdf_to_md.py <entrada.pdf> <saida.md>

Codigo de saida:
    0 -- conversao ok, saida.md escrito
    1 -- arquivo de entrada nao existe, ou uso incorreto dos argumentos
    2 -- conversao rodou mas produziu saida vazia/curta demais (provavel PDF
         escaneado sem texto extraivel, ou arquivo corrompido)
"""
import sys
from pathlib import Path

MIN_OUTPUT_CHARS = 200


def is_output_too_short(markdown_text: str, min_chars: int = MIN_OUTPUT_CHARS) -> bool:
    """Funcao pura, testavel sem rodar o marker de verdade -- decide se um
    texto convertido e curto/vazio demais pra ser um artigo academico real."""
    return len(markdown_text.strip()) < min_chars


def convert(input_path: Path, output_path: Path) -> str:
    """Roda o marker de verdade sobre input_path e escreve o markdown em
    output_path. Levanta FileNotFoundError se input_path nao existir."""
    if not input_path.exists():
        raise FileNotFoundError(f"arquivo de entrada nao encontrado: {input_path}")

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    converter = PdfConverter(artifact_dict=create_model_dict())
    rendered = converter(str(input_path))
    markdown_text, _, _ = text_from_rendered(rendered)

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

    if is_output_too_short(markdown_text):
        print(
            f"aviso: saida tem so {len(markdown_text.strip())} caracteres -- "
            f"provavelmente conversao falhou (PDF escaneado sem texto, ou corrompido)",
            file=sys.stderr,
        )
        return 2

    print(f"ok: {output_path} ({len(markdown_text)} caracteres)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
