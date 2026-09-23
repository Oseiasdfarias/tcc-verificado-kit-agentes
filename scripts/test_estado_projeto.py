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


FOTO = "tcc-kit/relatorios/_brutos/resultados-2026-09-23/.foto.json"


def test_foto_sem_mudanca(projeto):
    ep.foto(projeto, FOTO, ["tcc", "tcc-kit"])
    assert ep.comparar(projeto, FOTO, ["tcc", "tcc-kit"]) == []


def test_foto_detecta_alterado_novo_removido(projeto):
    (projeto / "tcc/capitulos/introducao.tex").write_text("intro\n")
    ep.foto(projeto, FOTO, ["tcc", "tcc-kit"])
    (projeto / "tcc/capitulos/resultados.tex").write_text("editado por agente\n")
    (projeto / "tcc/capitulos/introducao.tex").unlink()
    (projeto / "tcc/intruso.tex").write_text("x\n")
    assert ep.comparar(projeto, FOTO, ["tcc", "tcc-kit"]) == [
        ("removido", "tcc/capitulos/introducao.tex"),
        ("alterado", "tcc/capitulos/resultados.tex"),
        ("novo", "tcc/intruso.tex"),
    ]


def test_foto_ignora_relatorios_e_versoes(projeto):
    ep.foto(projeto, FOTO, ["tcc", "tcc-kit"])
    bruto = projeto / "tcc-kit/relatorios/_brutos/resultados-2026-09-23/guardiao-dados.md"
    bruto.write_text("relatório\n")
    (projeto / "tcc-kit/versoes/x").mkdir(parents=True)
    (projeto / "tcc-kit/versoes/x/a.tex").write_text("a\n")
    assert ep.comparar(projeto, FOTO, ["tcc", "tcc-kit"]) == []


def test_comparar_sem_foto_sai_com_2(projeto, capsys):
    assert ep.main(["--raiz", str(projeto), "comparar", FOTO, "tcc"]) == 2


def test_comparar_imprime_sem_alteracoes(projeto, capsys):
    ep.main(["--raiz", str(projeto), "foto", "--saida", FOTO, "tcc"])
    capsys.readouterr()
    assert ep.main(["--raiz", str(projeto), "comparar", FOTO, "tcc"]) == 0
    assert capsys.readouterr().out.strip() == "sem alterações"


def test_backup_de_arquivo_e_pasta_preserva_caminho(projeto):
    (projeto / "tcc/main.tex").write_text("preambulo\n")
    (projeto / "tcc/vazio.tex").write_text("")
    pasta, copiados = ep.backup(projeto, ["tcc", "nao-existe.tex"], momento="2026-09-23-101500")
    assert pasta == "tcc-kit/versoes/2026-09-23-101500"
    assert copiados == ["tcc/capitulos/resultados.tex", "tcc/main.tex"]
    copia = projeto / pasta / "tcc/capitulos/resultados.tex"
    assert copia.read_text() == "texto original\n"


def test_backup_sem_nada_para_copiar(projeto, capsys):
    assert ep.backup(projeto, ["nao-existe.tex"]) == (None, [])
    assert ep.main(["--raiz", str(projeto), "backup", "nao-existe.tex"]) == 0
    assert capsys.readouterr().out.strip() == "nada para copiar"
