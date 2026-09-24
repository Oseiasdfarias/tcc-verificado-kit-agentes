import perfil_dados as pd


def test_csv_virgula_com_colunas_numericas_e_texto(tmp_path):
    arq = tmp_path / "ensaio.csv"
    arq.write_text("tempo,angulo,rotulo\n0,1.5,a\n1,2.5,b\n2,3.5,c\n3,4.5,d\n")
    r = pd.perfil(arq, amostra=2)
    assert r["linhas"] == 4
    tempo, angulo, rotulo = r["colunas"]
    assert (angulo["minimo"], angulo["maximo"], angulo["media"]) == (1.5, 4.5, 3.0)
    assert tempo["nao_vazios"] == 4
    assert "media" not in rotulo
    assert r["amostra"] == [["0", "1.5", "a"], ["1", "2.5", "b"]]


def test_ponto_e_virgula_com_decimal_virgula(tmp_path):
    arq = tmp_path / "dados.csv"
    arq.write_text("taxa;n\n26,5;7043\n30,1;100\n")
    r = pd.perfil(arq)
    taxa, n = r["colunas"]
    assert taxa["minimo"] == 26.5 and taxa["maximo"] == 30.1
    assert n["maximo"] == 7043


def test_tsv(tmp_path):
    arq = tmp_path / "log.tsv"
    arq.write_text("a\tb\n1\t2\n3\t4\n")
    r = pd.perfil(arq)
    assert [c["nome"] for c in r["colunas"]] == ["a", "b"]
    assert r["colunas"][1]["media"] == 3.0


def test_coluna_mista_nao_e_numerica(tmp_path):
    arq = tmp_path / "m.csv"
    arq.write_text("x\n1\nerro\n3\n")
    assert "media" not in pd.perfil(arq)["colunas"][0]


def test_arquivo_vazio(tmp_path):
    arq = tmp_path / "vazio.csv"
    arq.write_text("")
    r = pd.perfil(arq)
    assert (r["linhas"], r["colunas"], r["amostra"]) == (0, [], [])


def test_formato_nao_suportado_sai_com_2(tmp_path, capsys):
    arq = tmp_path / "planilha.xlsx"
    arq.write_bytes(b"PK\x03\x04")
    assert pd.main([str(arq)]) == 2


def test_saida_formatada(tmp_path, capsys):
    arq = tmp_path / "e.csv"
    arq.write_text("v\n1\n3\n")
    assert pd.main([str(arq), "--amostra", "1"]) == 0
    saida = capsys.readouterr().out.splitlines()
    assert saida[0].startswith("leitura: encoding=utf-8")
    assert saida[1] == "linhas de dados: 2"
    assert saida[2] == "- v: 2 não vazios, numérica, mín 1, máx 3, média 2"
    assert saida[3:] == ["amostra:", "  1"]


def test_excel_brasileiro_latin1_com_milhar(tmp_path):
    arq = tmp_path / "planilha.csv"
    arq.write_bytes("nome;valor\nJoão;1.234,50\nMaria;26,5\n".encode("cp1252"))
    r = pd.perfil(arq)
    assert r["encoding"] == "cp1252"
    assert r["separador"] == ";"
    assert r["decimal"] == ","
    assert r["milhar"] == "."
    nome, valor = r["colunas"]
    assert (valor["minimo"], valor["maximo"]) == (26.5, 1234.5)
    assert r["amostra"][0][0] == "João"


def test_utf8_com_ponto_decimal(tmp_path):
    arq = tmp_path / "d.csv"
    arq.write_text("a,b\n1.5,x\n2.5,y\n", encoding="utf-8")
    r = pd.perfil(arq)
    assert (r["encoding"], r["separador"], r["decimal"], r["milhar"]) == ("utf-8", ",", ".", None)


def test_saida_informa_parametros_de_leitura(tmp_path, capsys):
    arq = tmp_path / "planilha.csv"
    arq.write_bytes("nome;valor\nJoão;26,5\n".encode("cp1252"))
    assert pd.main([str(arq)]) == 0
    saida = capsys.readouterr().out
    assert "leitura: encoding=cp1252, sep=';', decimal=','" in saida
