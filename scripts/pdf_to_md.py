#!/usr/bin/env python3
"""Converte um PDF em Markdown usando marker, validando que a saida nao ficou
vazia/curta demais antes de reportar sucesso. Ver secao "Tratamento de erro"
de docs/superpowers/specs/2026-08-21-motor-referencias-bibliograficas-design.md
no repo curso-tcc-ia.

Em CPU (o caso comum), o marker so liga seu backend de VLM/OCR (via um
binario externo, llama-server, do llama.cpp) quando o documento realmente
precisa -- formula, ou pagina escaneada/ilegivel. Um PDF digital limpo sem
formula converte normal, sem precisar desse binario. Quando precisa E o
binario nao esta instalado, a 1a tentativa falha -- esse script entao tenta
de novo com --disable_ocr (extracao pura de texto, sem formula/OCR, que nao
depende do binario) em vez de falhar a conversao inteira.

Uso:
    uv run --with marker-pdf scripts/pdf_to_md.py <entrada.pdf> <saida.md>

Codigo de saida:
    0 -- conversao ok (com reconhecimento de formula/OCR quando precisou)
    1 -- arquivo de entrada nao existe, ou uso incorreto dos argumentos
    2 -- conversao rodou (ou tentou rodar, inclusive apos o fallback) mas
         falhou de alguma forma: saida vazia/curta demais (provavel PDF
         escaneado sem texto extraivel, ou arquivo corrompido), ou qualquer
         excecao nao relacionada ao llama-server
    3 -- conversao ok, mas via fallback --disable_ocr: o binario llama-server
         nao foi encontrado nesta maquina, entao formula/OCR foram pulados
         (o texto restante do documento saiu normal). Pra reconhecimento de
         formula completo, instalar llama.cpp (brew install llama.cpp, ou
         baixar um release de https://github.com/ggml-org/llama.cpp/releases)
"""
import sys
from pathlib import Path

MIN_OUTPUT_CHARS = 200


def is_output_too_short(markdown_text: str, min_chars: int = MIN_OUTPUT_CHARS) -> bool:
    """Funcao pura, testavel sem rodar o marker de verdade -- decide se um
    texto convertido e curto/vazio demais pra ser um artigo academico real."""
    return len(markdown_text.strip()) < min_chars


def is_missing_llama_server_error(exc: Exception) -> bool:
    """Funcao pura, testavel sem o marker instalado -- detecta especificamente
    a falha de llama-server ausente (o backend de VLM/OCR do marker em CPU),
    pra so cair no fallback --disable_ocr nesse caso, nunca mascarando outro
    erro real de conversao."""
    return "llama-server" in str(exc).lower()


def convert(input_path: Path, output_path: Path) -> tuple[str, bool]:
    """Roda o marker de verdade sobre input_path e escreve o markdown em
    output_path. Levanta FileNotFoundError se input_path nao existir.

    Tenta a conversao completa primeiro (com reconhecimento de formula/OCR,
    quando o documento precisar). Se essa tentativa falhar especificamente
    por falta do binario llama-server, tenta de novo com --disable_ocr.
    Qualquer outra excecao sobe direto, sem fallback.

    Retorna (texto_convertido, usou_fallback_sem_ocr).
    """
    if not input_path.exists():
        raise FileNotFoundError(f"arquivo de entrada nao encontrado: {input_path}")

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    artifact_dict = create_model_dict()
    used_fallback = False
    try:
        converter = PdfConverter(artifact_dict=artifact_dict)
        rendered = converter(str(input_path))
    except Exception as e:
        if not is_missing_llama_server_error(e):
            raise
        from marker.config.parser import ConfigParser

        config_parser = ConfigParser({"disable_ocr": True, "output_format": "markdown"})
        converter = PdfConverter(
            config=config_parser.generate_config_dict(),
            artifact_dict=artifact_dict,
            processor_list=config_parser.get_processors(),
            renderer=config_parser.get_renderer(),
            llm_service=config_parser.get_llm_service(),
        )
        rendered = converter(str(input_path))
        used_fallback = True

    markdown_text, _, _ = text_from_rendered(rendered)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_text, encoding="utf-8")
    return markdown_text, used_fallback


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"uso: {argv[0]} <entrada.pdf> <saida.md>", file=sys.stderr)
        return 1

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    try:
        markdown_text, used_fallback = convert(input_path, output_path)
    except FileNotFoundError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"erro: conversao falhou -- {e}", file=sys.stderr)
        return 2

    if is_output_too_short(markdown_text):
        print(
            f"aviso: saida tem so {len(markdown_text.strip())} caracteres -- "
            f"provavelmente conversao falhou (PDF escaneado sem texto, ou corrompido)",
            file=sys.stderr,
        )
        return 2

    if used_fallback:
        print(
            "aviso: convertido sem reconhecimento de formula/OCR -- binario llama-server "
            "nao encontrado nesta maquina (ver docstring deste script pra instalar)",
            file=sys.stderr,
        )
        print(f"ok, sem formula/OCR: {output_path} ({len(markdown_text)} caracteres)")
        return 3

    print(f"ok: {output_path} ({len(markdown_text)} caracteres)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
