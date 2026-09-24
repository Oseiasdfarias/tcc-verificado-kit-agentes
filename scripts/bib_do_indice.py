#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Garante no .bib as entradas das chaves citadas, a partir do índice de referências do kit.

Nunca altera nem remove entrada existente: só acrescenta no fim, com backup antes.
Com DOI, usa o BibTeX oficial (doi.org); sem DOI ou sem rede, monta a entrada pelo índice.
"""

import argparse
import re
import sys
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estado_projeto  # noqa: E402

CITACAO = re.compile(
    r"\\apud\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}\{([^}]*)\}"
    r"|\\[a-zA-Z]*[cC]ite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}"
)
COMENTARIO = re.compile(r"(?<!\\)%.*")
ESPECIAIS = re.compile(r"(?<!\\)([&%#_])")
ENTRADA = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
NOTA = "Entrada montada pelo kit: confira o tipo"


def chaves_citadas(pasta):
    vistas = []
    for tex in sorted(Path(pasta).rglob("*.tex")):
        texto = COMENTARIO.sub("", tex.read_text(encoding="utf-8", errors="replace"))
        grupos = [g for m in CITACAO.finditer(texto) for g in m.groups() if g]
        for grupo in grupos:
            for chave in grupo.split(","):
                chave = chave.strip()
                if chave and chave not in vistas:
                    vistas.append(chave)
    return vistas


def chaves_no_bib(texto):
    return set(ENTRADA.findall(texto))


def carregar_indice(caminho):
    dados = yaml.safe_load(Path(caminho).read_text(encoding="utf-8")) or {}
    return {str(r["chave"]): r for r in dados.get("referencias") or [] if r.get("chave")}


def _valor(v):
    if isinstance(v, list):
        v = " and ".join(str(x) for x in v)
    return ESPECIAIS.sub(r"\\\1", str(v))


def entrada_do_indice(ref):
    tipo = "article" if ref.get("veiculo") else "misc"
    campos = [
        ("author", ref.get("autores")),
        ("title", ref.get("titulo")),
        ("journal", ref.get("veiculo")),
        ("year", ref.get("ano")),
        ("doi", ref.get("doi")),
        ("note", NOTA),
    ]
    linhas = [f"  {k} = {{{_valor(v)}}}" for k, v in campos if v not in (None, "", [])]
    return f"@{tipo}{{{ref['chave']},\n" + ",\n".join(linhas) + "\n}\n"


def buscar_bibtex_doi(doi, timeout=15):
    pedido = urllib.request.Request(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex; charset=utf-8", "User-Agent": "tcc-kit"},
    )
    try:
        with urllib.request.urlopen(pedido, timeout=timeout) as resposta:
            texto = resposta.read().decode("utf-8", "replace").strip()
    except Exception:
        return None
    return texto if texto.startswith("@") else None


def renomear_chave(bibtex, chave):
    m = ENTRADA.search(bibtex)
    return bibtex[: m.start(1)] + chave + bibtex[m.end(1):] if m else bibtex


def garantir(raiz, indice, bib, chaves, buscar=buscar_bibtex_doi):
    raiz, bib = Path(raiz), Path(bib)
    alvo = raiz / bib
    texto = alvo.read_text(encoding="utf-8") if alvo.exists() else ""
    existentes = chaves_no_bib(texto)
    novas, sem_indice = [], []
    for chave in chaves:
        if chave in existentes:
            continue
        ref = indice.get(chave)
        if ref is None or ref.get("status") != "verificado":
            sem_indice.append(chave)
            continue
        usar_oficial = ref.get("doi") and ref.get("fonte_bib") != "indice"
        oficial = buscar(str(ref["doi"])) if usar_oficial else None
        entrada = renomear_chave(oficial, chave).strip() + "\n" if oficial else entrada_do_indice(ref)
        novas.append((chave, entrada))
        existentes.add(chave)
    if novas:
        if alvo.exists():
            estado_projeto.backup(raiz, [bib.as_posix()])
        alvo.parent.mkdir(parents=True, exist_ok=True)
        separador = "" if not texto or texto.endswith("\n\n") else ("\n" if texto.endswith("\n") else "\n\n")
        alvo.write_text(texto + separador + "\n".join(e for _, e in novas), encoding="utf-8")
    return [c for c, _ in novas], sem_indice


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indice", default="tcc-kit/referencias/index.yaml")
    parser.add_argument("--bib", default="tcc/referencias.bib")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--chaves", nargs="+")
    grupo.add_argument("--todas-citadas", metavar="PASTA")
    parser.add_argument("--sem-rede", action="store_true")
    args = parser.parse_args(argv)
    raiz = Path.cwd()
    indice = carregar_indice(raiz / args.indice) if (raiz / args.indice).exists() else {}
    chaves = args.chaves or chaves_citadas(raiz / args.todas_citadas)
    buscar = (lambda doi: None) if args.sem_rede else buscar_bibtex_doi
    novas, sem = garantir(raiz, indice, Path(args.bib), chaves, buscar)
    print("acrescentadas: " + (", ".join(novas) or "nenhuma"))
    print("citadas sem entrada verificada no índice: " + (", ".join(sem) or "nenhuma"))
    return 1 if sem else 0


if __name__ == "__main__":
    sys.exit(main())
