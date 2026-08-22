from pathlib import Path

import pytest

import pdf_to_md
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


def test_main_returns_2_when_convert_raises_unexpected_exception(tmp_path, monkeypatch):
    """Qualquer falha de convert() que nao seja FileNotFoundError (ex.: uma
    dependencia de runtime do marker/surya ausente, como o llama-server) deve
    degradar para o codigo de saida 2, nunca vazar como traceback nao tratado."""

    def fake_convert(input_path, output_path):
        raise RuntimeError("llama-server binary not found")

    monkeypatch.setattr(pdf_to_md, "convert", fake_convert)

    entrada = tmp_path / "entrada.pdf"
    saida = tmp_path / "saida.md"
    codigo = pdf_to_md.main(["pdf_to_md.py", str(entrada), str(saida)])

    assert codigo == 2


def test_main_returns_0_on_success(tmp_path, monkeypatch):
    texto_longo = "palavra " * 100  # 800 caracteres, acima do MIN_OUTPUT_CHARS

    def fake_convert(input_path, output_path):
        output_path.write_text(texto_longo, encoding="utf-8")
        return texto_longo

    monkeypatch.setattr(pdf_to_md, "convert", fake_convert)

    entrada = tmp_path / "entrada.pdf"
    saida = tmp_path / "saida.md"
    codigo = pdf_to_md.main(["pdf_to_md.py", str(entrada), str(saida)])

    assert codigo == 0
    assert saida.read_text(encoding="utf-8") == texto_longo
