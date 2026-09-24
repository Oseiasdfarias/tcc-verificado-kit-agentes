import re
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills"
BLOCO = re.compile(r"```markdown\n(# Checklist de progresso — TCC\n.*?)```", re.S)
ESPERADO = [
    "Configuração institucional",
    "Template",
    "Tema",
    "Dados",
    "Referências",
    "Metodologia",
    "Capítulos",
    "Formatação ABNT",
    "Auditoria completa do TCC",
    "Apresentação de defesa",
]


def esqueletos():
    achados = {}
    for arquivo in sorted(SKILLS.glob("*/SKILL.md")):
        m = BLOCO.search(arquivo.read_text(encoding="utf-8"))
        if m:
            achados[arquivo.parent.name] = m.group(1)
    return achados


def secao(bloco, nome):
    m = re.search(rf"^## {re.escape(nome)}\n(.*?)(?=^## |\Z)", bloco, re.M | re.S)
    return m.group(1) if m else ""


def test_existem_as_dez_copias():
    assert len(esqueletos()) == 10


def test_todas_as_copias_tem_as_mesmas_secoes_na_mesma_ordem():
    for skill, bloco in esqueletos().items():
        assert re.findall(r"^## (.+)$", bloco, re.M) == ESPERADO, skill


def test_secao_dados_completa():
    for skill, bloco in esqueletos().items():
        dados = secao(bloco, "Dados")
        assert "**Tipo:**" in dados, skill
        assert "Preparados (tcc-kit/dados/limpeza.md)" in dados, skill
        assert "Resumo real (tcc/dados/resumo-real.md)" in dados, skill


def test_secao_formatacao():
    for skill, bloco in esqueletos().items():
        assert "- [ ] Nunca rodada" in secao(bloco, "Formatação ABNT"), skill
