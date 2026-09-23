import json

import pytest

import estado_projeto as ep


@pytest.fixture
def projeto(tmp_path):
    (tmp_path / "tcc/capitulos").mkdir(parents=True)
    (tmp_path / "tcc/capitulos/resultados.tex").write_text("texto original\n")
    return tmp_path


def estados(raiz):
    return {etapa: (estado, alterados) for etapa, _, estado, alterados in ep.verificar(raiz)}


def test_sem_estado_retorna_none_e_imprime_sem_registros(tmp_path, capsys):
    assert ep.verificar(tmp_path) is None
    assert ep.main(["--raiz", str(tmp_path), "verificar"]) == 0
    assert capsys.readouterr().out.strip() == "sem registros"


def test_registro_sem_mudanca_fica_atual(projeto):
    ep.registrar(projeto, "revisao:resultados", "rel.md", ["tcc/capitulos/resultados.tex"])
    assert estados(projeto) == {"revisao:resultados": ("atual", [])}


def test_entrada_alterada_fica_desatualizada(projeto):
    ep.registrar(projeto, "revisao:resultados", "rel.md", ["tcc/capitulos/resultados.tex"])
    (projeto / "tcc/capitulos/resultados.tex").write_text("texto novo\n")
    assert estados(projeto) == {
        "revisao:resultados": ("desatualizada", ["tcc/capitulos/resultados.tex"])
    }


def test_crlf_e_lf_tem_o_mesmo_hash(tmp_path):
    (tmp_path / "a.tex").write_bytes(b"linha 1\r\nlinha 2\r\n")
    (tmp_path / "b.tex").write_bytes(b"linha 1\nlinha 2\n")
    assert ep.hash_arquivo(tmp_path / "a.tex") == ep.hash_arquivo(tmp_path / "b.tex")


def test_entrada_ausente_que_passa_a_existir_fica_desatualizada(projeto):
    ep.registrar(projeto, "revisao:resultados", "rel.md",
                 ["tcc/capitulos/resultados.tex", "tcc/dados/resumo-real.md"])
    dados = json.loads((projeto / ep.ESTADO).read_text())
    assert dados["etapas"]["revisao:resultados"]["entradas"]["tcc/dados/resumo-real.md"] is None
    assert estados(projeto)["revisao:resultados"][0] == "atual"

    (projeto / "tcc/dados").mkdir()
    (projeto / "tcc/dados/resumo-real.md").write_text("dados\n")
    assert estados(projeto)["revisao:resultados"] == ("desatualizada", ["tcc/dados/resumo-real.md"])


def test_entrada_removida(projeto):
    ep.registrar(projeto, "revisao:resultados", "rel.md", ["tcc/capitulos/resultados.tex"])
    (projeto / "tcc/capitulos/resultados.tex").unlink()
    assert estados(projeto)["revisao:resultados"][0] == "entrada-removida"


def test_registrar_de_novo_sem_mudanca_e_deterministico(projeto):
    args = (projeto, "revisao:resultados", "rel.md", ["tcc/capitulos/resultados.tex"])
    ep.registrar(*args, data="2026-09-23")
    primeiro = (projeto / ep.ESTADO).read_bytes()
    ep.registrar(*args, data="2026-09-23")
    assert (projeto / ep.ESTADO).read_bytes() == primeiro


def test_registrar_mesma_etapa_substitui(projeto):
    ep.registrar(projeto, "revisao:resultados", "rel-1.md", ["tcc/capitulos/resultados.tex"])
    (projeto / "tcc/capitulos/resultados.tex").write_text("texto novo\n")
    ep.registrar(projeto, "revisao:resultados", "rel-2.md", ["tcc/capitulos/resultados.tex"])
    dados = json.loads((projeto / ep.ESTADO).read_text())
    assert list(dados["etapas"]) == ["revisao:resultados"]
    assert dados["etapas"]["revisao:resultados"]["saida"] == "rel-2.md"
    assert estados(projeto)["revisao:resultados"][0] == "atual"


def test_json_quebrado_sai_com_2_e_nao_altera(projeto, capsys):
    arquivo = projeto / ep.ESTADO
    arquivo.parent.mkdir(parents=True)
    arquivo.write_text("{quebrado")
    codigo = ep.main(["--raiz", str(projeto), "registrar", "--etapa", "x", "--saida", "y",
                      "--entradas", "tcc/capitulos/resultados.tex"])
    assert codigo == 2
    assert arquivo.read_text() == "{quebrado"
    assert ep.main(["--raiz", str(projeto), "verificar"]) == 2


def test_saida_formatada_lista_alterados(projeto, capsys):
    ep.registrar(projeto, "revisao:resultados", "rel.md", ["tcc/capitulos/resultados.tex"],
                 data="2026-09-21")
    (projeto / "tcc/capitulos/resultados.tex").write_text("texto novo\n")
    assert ep.main(["--raiz", str(projeto), "verificar"]) == 0
    saida = capsys.readouterr().out.splitlines()
    assert saida[0].split() == ["etapa", "data", "estado", "alterados"]
    assert saida[1].split() == ["revisao:resultados", "2026-09-21", "desatualizada",
                                "tcc/capitulos/resultados.tex"]
