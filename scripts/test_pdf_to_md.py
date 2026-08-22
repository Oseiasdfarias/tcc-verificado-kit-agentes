import sys
import types
from pathlib import Path

import pytest

import pdf_to_md
from pdf_to_md import convert, is_missing_llama_server_error, is_output_too_short


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


def test_is_missing_llama_server_error_detects_real_message():
    exc = RuntimeError(
        "llama-server binary not found. Install with:\n"
        "  macOS:  brew install llama.cpp"
    )
    assert is_missing_llama_server_error(exc) is True


def test_is_missing_llama_server_error_ignores_unrelated_exception():
    assert is_missing_llama_server_error(ValueError("PDF corrompido")) is False


def _install_fake_marker_modules(monkeypatch, first_call_raises):
    """Substitui os modulos marker.* que convert() importa, sem precisar do
    pacote de verdade instalado -- simula a 1a chamada falhando com o erro
    real do llama-server, e a 2a chamada (apos fallback --disable_ocr)
    tendo sucesso."""
    calls = []

    class FakeRendered:
        pass

    class FakePdfConverter:
        def __init__(self, artifact_dict=None, config=None, processor_list=None,
                     renderer=None, llm_service=None):
            calls.append(config)

        def __call__(self, path):
            if len(calls) == 1 and first_call_raises:
                raise RuntimeError("llama-server binary not found. Install with: ...")
            return FakeRendered()

    class FakeConfigParser:
        def __init__(self, config):
            self._config = config

        def generate_config_dict(self):
            return self._config

        def get_processors(self):
            return None

        def get_renderer(self):
            return None

        def get_llm_service(self):
            return None

    marker_converters_pdf = types.ModuleType("marker.converters.pdf")
    marker_converters_pdf.PdfConverter = FakePdfConverter
    marker_models = types.ModuleType("marker.models")
    marker_models.create_model_dict = lambda: {}
    marker_output = types.ModuleType("marker.output")
    marker_output.text_from_rendered = lambda rendered: ("texto convertido " * 50, None, None)
    marker_config_parser = types.ModuleType("marker.config.parser")
    marker_config_parser.ConfigParser = FakeConfigParser

    monkeypatch.setitem(sys.modules, "marker.converters.pdf", marker_converters_pdf)
    monkeypatch.setitem(sys.modules, "marker.models", marker_models)
    monkeypatch.setitem(sys.modules, "marker.output", marker_output)
    monkeypatch.setitem(sys.modules, "marker.config.parser", marker_config_parser)
    return calls


def test_convert_falls_back_to_disable_ocr_when_llama_server_missing(tmp_path, monkeypatch):
    calls = _install_fake_marker_modules(monkeypatch, first_call_raises=True)

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    markdown_text, used_fallback = convert(entrada, saida)

    assert used_fallback is True
    assert markdown_text.strip() != ""
    assert saida.read_text(encoding="utf-8") == markdown_text
    assert len(calls) == 2
    assert calls[0] is None  # 1a tentativa: sem config especial
    assert calls[1] == {"disable_ocr": True, "output_format": "markdown"}  # 2a tentativa: fallback


def test_convert_succeeds_without_fallback_when_no_llama_server_error(tmp_path, monkeypatch):
    calls = _install_fake_marker_modules(monkeypatch, first_call_raises=False)

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    markdown_text, used_fallback = convert(entrada, saida)

    assert used_fallback is False
    assert len(calls) == 1


def test_convert_reraises_unrelated_exception_without_fallback(tmp_path, monkeypatch):
    class FakePdfConverter:
        def __init__(self, **kwargs):
            pass

        def __call__(self, path):
            raise ValueError("PDF corrompido, nao e possivel ler")

    marker_converters_pdf = types.ModuleType("marker.converters.pdf")
    marker_converters_pdf.PdfConverter = FakePdfConverter
    marker_models = types.ModuleType("marker.models")
    marker_models.create_model_dict = lambda: {}
    marker_output = types.ModuleType("marker.output")
    marker_output.text_from_rendered = lambda rendered: ("", None, None)

    monkeypatch.setitem(sys.modules, "marker.converters.pdf", marker_converters_pdf)
    monkeypatch.setitem(sys.modules, "marker.models", marker_models)
    monkeypatch.setitem(sys.modules, "marker.output", marker_output)

    entrada = tmp_path / "entrada.pdf"
    entrada.write_bytes(b"%PDF-1.4 fake")
    saida = tmp_path / "saida.md"

    with pytest.raises(ValueError, match="PDF corrompido"):
        convert(entrada, saida)


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
        return texto_longo, False

    monkeypatch.setattr(pdf_to_md, "convert", fake_convert)

    entrada = tmp_path / "entrada.pdf"
    saida = tmp_path / "saida.md"
    codigo = pdf_to_md.main(["pdf_to_md.py", str(entrada), str(saida)])

    assert codigo == 0
    assert saida.read_text(encoding="utf-8") == texto_longo


def test_main_returns_3_when_convert_used_fallback(tmp_path, monkeypatch):
    texto_longo = "palavra " * 100

    def fake_convert(input_path, output_path):
        output_path.write_text(texto_longo, encoding="utf-8")
        return texto_longo, True

    monkeypatch.setattr(pdf_to_md, "convert", fake_convert)

    entrada = tmp_path / "entrada.pdf"
    saida = tmp_path / "saida.md"
    codigo = pdf_to_md.main(["pdf_to_md.py", str(entrada), str(saida)])

    assert codigo == 3
    assert saida.read_text(encoding="utf-8") == texto_longo
