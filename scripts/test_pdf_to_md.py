from pathlib import Path

import pytest
from pdf_to_md import convert, is_output_too_short


def test_short_text_is_too_short():
    assert is_output_too_short("abc") is True


def test_long_text_is_not_too_short():
    texto_longo = "palavra " * 100  # 800 caracteres
    assert is_output_too_short(texto_longo) is False


def test_empty_text_is_too_short():
    assert is_output_too_short("") is True


def test_custom_threshold():
    assert is_output_too_short("12345", min_chars=3) is False
    assert is_output_too_short("12", min_chars=3) is True


def test_convert_raises_when_input_missing(tmp_path):
    entrada_inexistente = tmp_path / "nao-existe.pdf"
    saida = tmp_path / "saida.md"
    with pytest.raises(FileNotFoundError):
        convert(entrada_inexistente, saida)
