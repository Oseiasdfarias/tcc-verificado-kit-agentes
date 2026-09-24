"""Perfil de um CSV/TSV sem carregar o arquivo no contexto do modelo.

Imprime os parâmetros de leitura (encoding, separador, decimal, milhar), o total de linhas, e por coluna: nome, valores não vazios e, se numérica, mínimo, máximo e média.
Depois, algumas linhas de amostra. Só biblioteca padrão.
"""

import argparse
import csv
import re
import statistics
import sys
from pathlib import Path

EXTENSOES = {".csv", ".tsv", ".txt"}


MILHAR_VIRGULA = re.compile(r"^-?\d{1,3}(\.\d{3})+,\d+$")
DECIMAL_VIRGULA = re.compile(r"^-?\d+,\d+$")
DECIMAL_PONTO = re.compile(r"^-?\d+\.\d+$")


def numero(texto):
    texto = texto.strip()
    if not texto:
        return None
    if MILHAR_VIRGULA.match(texto):
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto and "." not in texto:
        texto = texto.replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def detectar_dialeto(amostra):
    try:
        return csv.Sniffer().sniff(amostra, delimiters=",;\t|")
    except csv.Error:
        return csv.excel_tab if amostra.count("\t") > amostra.count(",") else csv.excel


def ler_texto(caminho):
    dados = caminho.read_bytes()
    try:
        return dados.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        return dados.decode("cp1252", errors="replace"), "cp1252"


def formato_numerico(valores):
    virgula = sum(1 for v in valores if DECIMAL_VIRGULA.match(v) or MILHAR_VIRGULA.match(v))
    ponto = sum(1 for v in valores if DECIMAL_PONTO.match(v))
    milhar = "." if any(MILHAR_VIRGULA.match(v) for v in valores) else None
    return ("," if virgula > ponto else "."), milhar


def perfil(caminho, amostra=3):
    caminho = Path(caminho)
    if caminho.suffix.lower() not in EXTENSOES:
        raise ValueError(f"formato não suportado: {caminho.suffix or 'sem extensão'} (só CSV/TSV)")
    texto, encoding = ler_texto(caminho)
    if not texto.strip():
        return {"linhas": 0, "colunas": [], "amostra": [], "encoding": encoding, "separador": ",",
                "decimal": ".", "milhar": None}
    dialeto = detectar_dialeto(texto[:4096])
    leitor = csv.reader(texto.splitlines(), dialeto)
    cabecalho = next(leitor)
    linhas = [l for l in leitor if any(c.strip() for c in l)]
    colunas = []
    for i, nome in enumerate(cabecalho):
        valores = [l[i] for l in linhas if i < len(l) and l[i].strip()]
        numeros = [n for n in (numero(v) for v in valores) if n is not None]
        coluna = {"nome": nome.strip(), "nao_vazios": len(valores)}
        if valores and len(numeros) == len(valores):
            coluna.update(minimo=min(numeros), maximo=max(numeros), media=statistics.fmean(numeros))
        colunas.append(coluna)
    decimal, milhar = formato_numerico([c.strip() for l in linhas for c in l])
    return {"linhas": len(linhas), "colunas": colunas, "amostra": linhas[:amostra], "encoding": encoding,
            "separador": dialeto.delimiter, "decimal": decimal, "milhar": milhar}


def formatar(resultado):
    leitura = f"leitura: encoding={resultado['encoding']}, sep={resultado['separador']!r}, decimal={resultado['decimal']!r}"
    if resultado.get("milhar"):
        leitura += f", thousands={resultado['milhar']!r}"
    saida = [leitura, f"linhas de dados: {resultado['linhas']}"]
    for c in resultado["colunas"]:
        linha = f"- {c['nome']}: {c['nao_vazios']} não vazios"
        if "media" in c:
            linha += f", numérica, mín {c['minimo']:.6g}, máx {c['maximo']:.6g}, média {c['media']:.6g}"
        else:
            linha += ", texto ou misto"
        saida.append(linha)
    if resultado["amostra"]:
        saida.append("amostra:")
        saida.extend("  " + " | ".join(l) for l in resultado["amostra"])
    return "\n".join(saida)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arquivo")
    parser.add_argument("--amostra", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        print(formatar(perfil(args.arquivo, args.amostra)))
    except (ValueError, OSError) as erro:
        print(f"não foi possível perfilar {args.arquivo}: {erro}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
