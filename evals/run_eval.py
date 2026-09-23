#!/usr/bin/env python3
"""Runner dos cenários de avaliação das skills do kit-agentes.

Cria um diretório temporário isolado (nunca toca no repositório do plugin nem em
qualquer projeto de TCC real), escreve as fixtures do cenário, roda o setup_script
(se houver -- útil pra gerar um PDF real de teste, por exemplo), dispara `claude -p`
de verdade contra o plugin local (um ou mais turnos, via --resume entre eles quando
o cenário tem mais de uma mensagem), e imprime a resposta final de cada turno + a
árvore de arquivos resultante + o checklist de `expected_behavior` pra conferência
manual -- não existe grader automático (a Anthropic também não oferece um pronto pra
esse formato), então quem lê o output decide se cada item da lista foi atendido.

Uso:
    python3 run_eval.py evals/escrever-capitulo/scenario-1-modo-rapido-grounding.json
    python3 run_eval.py evals/escrever-capitulo/                 # roda todos os .json da pasta
    python3 run_eval.py evals/                                    # roda a suíte inteira
    python3 run_eval.py <cenario>.json --keep                     # mantém o dir temporário pra inspecionar
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CUSTOS: list[float] = []


def write_fixtures(cwd: Path, fixtures: dict) -> None:
    for rel_path, content in fixtures.items():
        full = cwd / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")


def run_claude(query: str, cwd: Path, session_id: str, resume: bool, timeout: int) -> str:
    cmd = [
        "claude", "-p", query,
        "--plugin-dir", str(REPO_ROOT),
        "--dangerously-skip-permissions",
        "--output-format", "json",
    ]
    cmd += ["--resume", session_id] if resume else ["--session-id", session_id]
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT após {timeout}s -- turno não completou]"
    if result.returncode != 0:
        print(f"[aviso] claude saiu com código {result.returncode}", file=sys.stderr)
        if result.stderr.strip():
            print(result.stderr, file=sys.stderr)
    try:
        dados = json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout.strip()
    uso = dados.get("usage", {})
    CUSTOS.append(dados.get("total_cost_usd") or 0.0)
    print(
        f"[custo do turno] US$ {dados.get('total_cost_usd') or 0:.4f} · "
        f"entrada {uso.get('input_tokens', 0)} · saída {uso.get('output_tokens', 0)} · "
        f"cache lido {uso.get('cache_read_input_tokens', 0)} · "
        f"cache criado {uso.get('cache_creation_input_tokens', 0)} · "
        f"turnos internos {dados.get('num_turns', '?')}"
    )
    return (dados.get("result") or "").strip()


def run_scenario(scenario_path: Path, keep: bool, timeout: int) -> None:
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    title = scenario.get("title", scenario_path.stem)
    skill = scenario["skill"]
    turns = scenario.get("turns") or [scenario["query"]]
    fixtures = scenario.get("fixtures", {})
    setup_script = scenario.get("setup_script")
    expected = scenario.get("expected_behavior", [])

    tmpdir = Path(tempfile.mkdtemp(prefix=f"eval-{skill}-"))
    print(f"\n{'=' * 70}")
    print(f"Cenário: {title}  (skill: {skill})")
    print(f"Arquivo: {scenario_path}")
    print(f"Diretório de trabalho: {tmpdir}")
    print("=" * 70)

    try:
        write_fixtures(tmpdir, fixtures)
        if setup_script:
            subprocess.run(["bash", "-c", setup_script], cwd=tmpdir, check=True)

        session_id = str(uuid.uuid4())
        for i, turn in enumerate(turns):
            print(f"\n--- Turno {i + 1}/{len(turns)}: {turn!r} ---")
            response = run_claude(turn, tmpdir, session_id, resume=(i > 0), timeout=timeout)
            print(response)

        print("\n--- Árvore de arquivos após a execução ---", flush=True)
        subprocess.run(
            ["find", ".", "-type", "f", "-not", "-path", "./.claude/*"],
            cwd=tmpdir,
        )

        print("\n--- Comportamento esperado (confira contra a resposta e os arquivos acima) ---")
        for item in expected:
            print(f"[ ] {item}")

    finally:
        if keep:
            print(f"\n(diretório mantido em {tmpdir} -- apague manualmente quando terminar)")
        else:
            shutil.rmtree(tmpdir, ignore_errors=True)


def collect_scenarios(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(target.rglob("*.json"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", help="Cenário .json, ou pasta (roda todos os .json dentro, recursivo)")
    parser.add_argument("--keep", action="store_true", help="Não apaga o diretório temporário no final")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout por turno em segundos (padrão: 300)")
    args = parser.parse_args()

    scenarios = collect_scenarios(Path(args.target))
    if not scenarios:
        print(f"Nenhum cenário .json encontrado em {args.target}", file=sys.stderr)
        sys.exit(1)

    for path in scenarios:
        run_scenario(path, keep=args.keep, timeout=args.timeout)

    if CUSTOS:
        print(f"\n[custo total] US$ {sum(CUSTOS):.4f} em {len(CUSTOS)} turno(s)")


if __name__ == "__main__":
    main()
