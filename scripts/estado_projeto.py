"""Registro de versões (sha256), trava de integridade e backup do tcc-kit.

registrar: grava o hash das entradas usadas por uma etapa (ex: revisao:resultados).
verificar: compara os hashes gravados com os arquivos atuais e imprime uma tabela curta.
foto/comparar: detecta arquivos alterados enquanto agentes rodavam.
backup: copia arquivos para tcc-kit/versoes/<momento>/ antes de uma skill sobrescrevê-los.

Só biblioteca padrão. Nunca executa git.
"""

import argparse
import datetime
import hashlib
import json
import shutil
import sys
from pathlib import Path

ESTADO = Path("tcc-kit/.estado.json")
VERSAO = 1


class EstadoIlegivel(Exception):
    pass


def hash_arquivo(caminho):
    conteudo = Path(caminho).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(conteudo).hexdigest()


def normalizar(caminho):
    return Path(caminho).as_posix()


def carregar(raiz):
    arquivo = raiz / ESTADO
    if not arquivo.exists():
        return None
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise EstadoIlegivel(str(erro)) from erro
    if not isinstance(dados, dict) or not isinstance(dados.get("etapas"), dict):
        raise EstadoIlegivel("formato inesperado")
    return dados


def salvar(raiz, dados):
    arquivo = raiz / ESTADO
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    texto = json.dumps(dados, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    arquivo.write_text(texto, encoding="utf-8", newline="\n")


def registrar(raiz, etapa, saida, entradas, data=None):
    dados = carregar(raiz) or {"versao": VERSAO, "etapas": {}}
    hashes = {}
    for entrada in entradas:
        caminho = raiz / entrada
        hashes[normalizar(entrada)] = hash_arquivo(caminho) if caminho.is_file() else None
    dados["etapas"][etapa] = {
        "data": data or datetime.date.today().isoformat(),
        "saida": normalizar(saida),
        "entradas": hashes,
    }
    salvar(raiz, dados)


def verificar(raiz):
    dados = carregar(raiz)
    if dados is None:
        return None
    linhas = []
    for etapa in sorted(dados["etapas"]):
        registro = dados["etapas"][etapa]
        alterados, removidos = [], []
        for entrada, esperado in sorted(registro.get("entradas", {}).items()):
            caminho = raiz / entrada
            atual = hash_arquivo(caminho) if caminho.is_file() else None
            if atual == esperado:
                continue
            if atual is None:
                removidos.append(entrada)
            else:
                alterados.append(entrada)
        if removidos:
            estado = "entrada-removida"
        elif alterados:
            estado = "desatualizada"
        else:
            estado = "atual"
        linhas.append((etapa, registro.get("data", "-"), estado, alterados + removidos))
    return linhas


IGNORAR_NA_FOTO = ("tcc-kit/relatorios/", "tcc-kit/versoes/")


def arquivos_sob(raiz, pastas):
    for pasta in pastas:
        base = raiz / pasta
        candidatos = [base] if base.is_file() else sorted(p for p in base.rglob("*") if p.is_file())
        for caminho in candidatos:
            yield caminho.relative_to(raiz).as_posix()


def tirar_foto(raiz, pastas):
    return {
        rel: hash_arquivo(raiz / rel)
        for rel in arquivos_sob(raiz, pastas)
        if not rel.startswith(IGNORAR_NA_FOTO)
    }


def foto(raiz, saida, pastas):
    arquivo = raiz / saida
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    texto = json.dumps(tirar_foto(raiz, pastas), indent=2, sort_keys=True) + "\n"
    arquivo.write_text(texto, encoding="utf-8", newline="\n")


def comparar(raiz, arquivo_foto, pastas):
    caminho = raiz / arquivo_foto
    if not caminho.is_file():
        raise EstadoIlegivel(f"foto não encontrada: {arquivo_foto}")
    try:
        antes = json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise EstadoIlegivel(str(erro)) from erro
    depois = tirar_foto(raiz, pastas)
    mudancas = []
    for rel in sorted(set(antes) | set(depois)):
        if rel not in depois:
            mudancas.append(("removido", rel))
        elif rel not in antes:
            mudancas.append(("novo", rel))
        elif antes[rel] != depois[rel]:
            mudancas.append(("alterado", rel))
    return mudancas


def backup(raiz, caminhos, momento=None):
    momento = momento or datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    destino = raiz / "tcc-kit/versoes" / momento
    copiados = []
    for rel in arquivos_sob(raiz, [c for c in caminhos if (raiz / c).exists()]):
        if rel.startswith(IGNORAR_NA_FOTO):
            continue
        origem = raiz / rel
        if origem.stat().st_size == 0:
            continue
        alvo = destino / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, alvo)
        copiados.append(rel)
    return (destino.relative_to(raiz).as_posix() if copiados else None), copiados


def formatar(linhas):
    if not linhas:
        return "sem registros"
    cabecalho = ("etapa", "data", "estado", "alterados")
    corpo = [(e, d, s, ", ".join(a) or "-") for e, d, s, a in linhas]
    larguras = [max(len(str(l[i])) for l in [cabecalho] + corpo) for i in range(3)]
    saida = []
    for linha in [cabecalho] + corpo:
        saida.append("  ".join(str(linha[i]).ljust(larguras[i]) for i in range(3)) + "  " + linha[3])
    return "\n".join(saida)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raiz", default=".", help="raiz do projeto do TCC (padrão: diretório atual)")
    sub = parser.add_subparsers(dest="comando", required=True)
    reg = sub.add_parser("registrar")
    reg.add_argument("--etapa", required=True)
    reg.add_argument("--saida", required=True)
    reg.add_argument("--entradas", nargs="+", required=True)
    sub.add_parser("verificar")
    fot = sub.add_parser("foto")
    fot.add_argument("--saida", required=True)
    fot.add_argument("pastas", nargs="+")
    com = sub.add_parser("comparar")
    com.add_argument("foto")
    com.add_argument("pastas", nargs="+")
    bkp = sub.add_parser("backup")
    bkp.add_argument("caminhos", nargs="+")
    args = parser.parse_args(argv)
    raiz = Path(args.raiz)

    try:
        if args.comando == "registrar":
            registrar(raiz, args.etapa, args.saida, args.entradas)
            print(f"registrado: {args.etapa}")
        elif args.comando == "verificar":
            print(formatar(verificar(raiz)))
        elif args.comando == "foto":
            foto(raiz, args.saida, args.pastas)
            print(f"foto: {args.saida}")
        elif args.comando == "comparar":
            mudancas = comparar(raiz, args.foto, args.pastas)
            print("\n".join(f"{tipo}  {rel}" for tipo, rel in mudancas) or "sem alterações")
        else:
            pasta, copiados = backup(raiz, args.caminhos)
            print(f"backup: {pasta} ({len(copiados)} arquivo(s))" if pasta else "nada para copiar")
    except EstadoIlegivel as erro:
        print(f"tcc-kit/.estado.json ilegível ({erro}); nada foi alterado", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
