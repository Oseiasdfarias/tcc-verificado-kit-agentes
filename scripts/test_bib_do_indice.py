from pathlib import Path

import bib_do_indice as b

INDICE = """referencias:
  - chave: silva2021
    titulo: "Evasão no ensino a distância"
    autores: ["Silva, A.", "Souza, B."]
    ano: 2021
    veiculo: "Revista Brasileira de Educação"
    status: verificado
  - chave: souza2020
    titulo: "Churn em telecom"
    autores: ["Souza, C."]
    ano: 2020
    veiculo: "Journal of Telecom"
    doi: "10.1000/xyz"
    status: verificado
  - chave: livro2019
    titulo: "Métodos"
    autores: ["Lima, D."]
    ano: 2019
    status: verificado
"""

SEM_REDE = lambda doi: None


def projeto(tmp_path, bib=None):
    (tmp_path / "tcc-kit/referencias").mkdir(parents=True)
    (tmp_path / "tcc-kit/referencias/index.yaml").write_text(INDICE, encoding="utf-8")
    (tmp_path / "tcc").mkdir()
    if bib is not None:
        (tmp_path / "tcc/referencias.bib").write_text(bib, encoding="utf-8")
    return tmp_path, b.carregar_indice(tmp_path / "tcc-kit/referencias/index.yaml")


def test_chaves_citadas_com_opcoes_espacos_e_variantes(tmp_path):
    cap = tmp_path / "capitulos"
    cap.mkdir()
    (cap / "a.tex").write_text(
        r"Texto \cite[p.~3]{silva2021, souza2020} e \citeonline*{livro2019}. De novo \cite{silva2021}.",
        encoding="utf-8",
    )
    assert b.chaves_citadas(cap) == ["silva2021", "souza2020", "livro2019"]


def test_chaves_no_bib():
    assert b.chaves_no_bib("@article{a2020,\n title={x}}\n@misc{ b2021 ,\n}") == {"a2020", "b2021"}


def test_bib_inexistente_e_criado_sem_backup(tmp_path):
    raiz, indice = projeto(tmp_path)
    novas, sem = b.garantir(raiz, indice, Path("tcc/referencias.bib"), ["silva2021"], SEM_REDE)
    assert novas == ["silva2021"] and sem == []
    texto = (raiz / "tcc/referencias.bib").read_text(encoding="utf-8")
    assert texto.startswith("@article{silva2021,")
    assert "author = {Silva, A. and Souza, B.}" in texto
    assert "journal = {Revista Brasileira de Educação}" in texto
    assert b.NOTA in texto
    assert not (raiz / "tcc-kit/versoes").exists()


def test_entrada_existente_fica_intocada_e_ha_backup(tmp_path):
    original = "@book{silva2021,\n  title = {Versão do aluno}\n}\n"
    raiz, indice = projeto(tmp_path, bib=original)
    novas, _ = b.garantir(raiz, indice, Path("tcc/referencias.bib"), ["silva2021", "livro2019"], SEM_REDE)
    assert novas == ["livro2019"]
    texto = (raiz / "tcc/referencias.bib").read_text(encoding="utf-8")
    assert texto.startswith(original)
    assert "@misc{livro2019," in texto
    backups = list((raiz / "tcc-kit/versoes").rglob("referencias.bib"))
    assert len(backups) == 1 and backups[0].read_text(encoding="utf-8") == original


def test_com_doi_usa_bibtex_oficial_e_troca_a_chave(tmp_path):
    raiz, indice = projeto(tmp_path)
    oficial = "@article{Souza_2020, title={Churn em telecom}, year={2020}}"
    novas, _ = b.garantir(raiz, indice, Path("tcc/referencias.bib"), ["souza2020"], lambda doi: oficial)
    texto = (raiz / "tcc/referencias.bib").read_text(encoding="utf-8")
    assert novas == ["souza2020"]
    assert "@article{souza2020," in texto and "Souza_2020" not in texto
    assert b.NOTA not in texto


def test_doi_sem_resposta_cai_para_o_indice(tmp_path):
    raiz, indice = projeto(tmp_path)
    b.garantir(raiz, indice, Path("tcc/referencias.bib"), ["souza2020"], SEM_REDE)
    texto = (raiz / "tcc/referencias.bib").read_text(encoding="utf-8")
    assert "@article{souza2020," in texto and "doi = {10.1000/xyz}" in texto and b.NOTA in texto


def test_chave_fora_do_indice_nao_e_escrita(tmp_path):
    raiz, indice = projeto(tmp_path)
    novas, sem = b.garantir(raiz, indice, Path("tcc/referencias.bib"), ["inventada2099"], SEM_REDE)
    assert novas == [] and sem == ["inventada2099"]
    assert not (raiz / "tcc/referencias.bib").exists()


def test_nada_a_fazer_nao_reescreve(tmp_path):
    original = "@article{silva2021,\n}\n"
    raiz, indice = projeto(tmp_path, bib=original)
    novas, sem = b.garantir(raiz, indice, Path("tcc/referencias.bib"), ["silva2021"], SEM_REDE)
    assert (novas, sem) == ([], [])
    assert not (raiz / "tcc-kit/versoes").exists()


def test_cli_todas_citadas_e_codigo_de_saida(tmp_path, monkeypatch, capsys):
    raiz, _ = projeto(tmp_path)
    (raiz / "tcc/capitulos").mkdir()
    (raiz / "tcc/capitulos/intro.tex").write_text(r"\cite{silva2021,fantasma2000}", encoding="utf-8")
    monkeypatch.chdir(raiz)
    codigo = b.main(["--todas-citadas", "tcc/capitulos", "--sem-rede"])
    saida = capsys.readouterr().out
    assert codigo == 1
    assert "acrescentadas: silva2021" in saida
    assert "citadas sem entrada no índice: fantasma2000" in saida
