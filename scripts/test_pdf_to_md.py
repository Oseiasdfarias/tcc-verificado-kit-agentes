import sys
import types
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


def _install_fake_pdfplumber(monkeypatch, paginas_texto):
    """Substitui o modulo pdfplumber que convert() importa, sem precisar do
    pacote de verdade instalado -- simula um PDF com as paginas de texto
    dadas (uma string por pagina; None simula pagina sem texto extraivel,
    ex: escaneada ou so com formula/imagem)."""

    class FakePage:
        def __init__(self, texto):
            self._texto = texto

        def extract_text(self):
            return self._texto

    class FakePdf:
        def __init__(self, paginas):
            self.pages = [FakePage(t) for t in paginas]

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    fake_pdfplumber = types.ModuleType("pdfplumber")
    fake_pdfplumber.open = lambda path: FakePdf(paginas_texto)
    monkeypatch.setitem(sys.modules, "pdfplumber", fake_pdfplumber)


def test_convert_extracts_text_from_all_pages(tmp_path, monkeypatch):
    _install_fake_pdfplumber(monkeypatch, ["Pagina um. " * 20, "Pagina dois. " * 20])

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    markdown_text = convert(entrada, saida)

    assert "Pagina um." in markdown_text
    assert "Pagina dois." in markdown_text
    assert saida.read_text(encoding="utf-8") == markdown_text


def test_convert_skips_pages_without_extractable_text(tmp_path, monkeypatch):
    _install_fake_pdfplumber(monkeypatch, ["Pagina com texto. " * 20, None])

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    markdown_text = convert(entrada, saida)

    assert "Pagina com texto." in markdown_text


def test_convert_returns_short_text_when_no_page_has_extractable_text(tmp_path, monkeypatch):
    """PDF escaneado / so com formula-imagem: nenhuma pagina extrai texto --
    convert() nao falha, so devolve texto curto/vazio pra quem chama decidir
    (via is_output_too_short) que precisa do fallback de leitura direta."""
    _install_fake_pdfplumber(monkeypatch, [None, None])

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    markdown_text = convert(entrada, saida)

    assert is_output_too_short(markdown_text) is True


def test_convert_reraises_unrelated_exception(tmp_path, monkeypatch):
    class FakePdf:
        def __enter__(self):
            raise ValueError("PDF corrompido, nao e possivel ler")

        def __exit__(self, *args):
            return False

    fake_pdfplumber = types.ModuleType("pdfplumber")
    fake_pdfplumber.open = lambda path: FakePdf()
    monkeypatch.setitem(sys.modules, "pdfplumber", fake_pdfplumber)

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    with pytest.raises(ValueError, match="PDF corrompido"):
        convert(entrada, saida)


def test_main_returns_2_when_convert_raises_unexpected_exception(tmp_path, monkeypatch):
    def fake_convert(input_path, output_path):
        raise RuntimeError("erro de extracao qualquer")

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


def test_main_returns_3_when_output_too_short(tmp_path, monkeypatch):
    texto_curto = "abc"

    def fake_convert(input_path, output_path):
        output_path.write_text(texto_curto, encoding="utf-8")
        return texto_curto

    monkeypatch.setattr(pdf_to_md, "convert", fake_convert)

    entrada = tmp_path / "entrada.pdf"
    saida = tmp_path / "saida.md"
    codigo = pdf_to_md.main(["pdf_to_md.py", str(entrada), str(saida)])

    assert codigo == 3
    assert saida.read_text(encoding="utf-8") == texto_curto


def test_main_returns_1_on_wrong_argument_count():
    codigo = pdf_to_md.main(["pdf_to_md.py", "so-um-arg.pdf"])
    assert codigo == 1


def test_main_returns_1_when_input_missing(tmp_path):
    entrada = tmp_path / "nao-existe.pdf"
    saida = tmp_path / "saida.md"
    codigo = pdf_to_md.main(["pdf_to_md.py", str(entrada), str(saida)])
    assert codigo == 1
