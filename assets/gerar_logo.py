"""gerar_logo.py — marca própria do kit-agentes: três checks de tinta em
camadas, representando as passadas de revisão que o kit faz (dado, citação,
argumento, banca, forma) antes de um capítulo ser considerado pronto.

A geometria do traço (espinha de pontos + espessura variável, stampada como
círculos interpolados) é copiada de curso-tcc-ia/brand/traco.py -- é a MESMA
marca "check" do curso, só usada aqui em três instâncias sobrepostas em vez
de uma. Repositórios diferentes, sem import direto possível; se a forma do
check mudar lá, mudar aqui também (mesmo padrão de duplicação documentada já
usado pra esses dois arrays em três lugares dentro do curso-tcc-ia).

Uso: python3 gerar_logo.py
"""
import subprocess
from pathlib import Path

OUT = Path(__file__).parent
CHROME = "google-chrome"

# Copiado de curso-tcc-ia/brand/traco.py -- ver docstring acima.
ESPINHA: list[tuple[float, float]] = [
    (0.16, 0.46), (0.22, 0.55), (0.29, 0.65), (0.365, 0.735),
    (0.42, 0.70), (0.52, 0.575), (0.635, 0.42), (0.745, 0.265),
    (0.835, 0.145), (0.885, 0.075), (0.915, 0.038),
]
ESPESSURA: list[float] = [0.014, 0.026, 0.038, 0.05, 0.046, 0.04, 0.033, 0.026, 0.018, 0.010, 0.004]

COBRE = "#201812"
LATAO = "#C98A52"
LATAO_CLARO = "#DDAA79"


def check_circles(tamanho: int, passos_por_segmento: int = 50) -> str:
    circulos = []
    for i in range(len(ESPINHA) - 1):
        x0, y0 = ESPINHA[i]
        x1, y1 = ESPINHA[i + 1]
        w0, w1 = ESPESSURA[i], ESPESSURA[i + 1]
        for passo in range(passos_por_segmento + 1):
            f = passo / passos_por_segmento
            x = (x0 + (x1 - x0) * f) * tamanho
            y = (y0 + (y1 - y0) * f) * tamanho
            w = (w0 + (w1 - w0) * f) * tamanho
            circulos.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{w:.2f}"/>')
    return "".join(circulos)


def build_logo(tamanho: int = 512, out_name: str = "logo-kit.png"):
    """Três checks em camada: o de trás maior e mais claro/transparente (a
    primeira passada), o do meio médio, o da frente no tamanho base e na cor
    de tinta principal (a revisão final, "verificado"). Cada camada é
    deslocada um pouco pra cima-esquerda da anterior -- sugere profundidade,
    não um empilhamento reto."""
    base = tamanho * 0.56  # a marca em si ocupa ~56% do canvas -- menor que o ícone principal
    # pra sobrar espaço real pro deslocamento das camadas de trás
    layers = [
        # (escala relativa à base, deslocamento x, deslocamento y, cor, opacidade)
        (1.0, -0.15, -0.15, LATAO_CLARO, 0.45),
        (1.0, -0.075, -0.075, LATAO, 0.70),
        (1.0, 0.0, 0.0, COBRE, 1.0),
    ]
    groups = []
    for escala, dx, dy, cor, opacidade in layers:
        tam = base * escala
        off_x = tamanho * 0.275 + dx * tamanho
        off_y = tamanho * 0.36 + dy * tamanho
        groups.append(
            f'<g transform="translate({off_x:.2f},{off_y:.2f})" fill="{cor}" opacity="{opacidade}">'
            f'{check_circles(int(tam))}</g>'
        )
    svg = (
        f'<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 {tamanho} {tamanho}" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(groups)}</svg>'
    )
    html = (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        "html,body{margin:0;padding:0;background:transparent;}"
        "*{box-sizing:border-box;}</style></head><body>" + svg + "</body></html>"
    )
    tmp = OUT / "_tmp_logo.html"
    tmp.write_text(html, encoding="utf-8")
    out_path = OUT / out_name
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        f"--window-size={tamanho},{tamanho}",
        f"--screenshot={out_path}",
        "--default-background-color=00000000",
        tmp.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not out_path.exists():
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"chrome screenshot failed: {result.stderr}")
    tmp.unlink()
    print(f"-> {out_path.name} ({tamanho}x{tamanho})")


if __name__ == "__main__":
    build_logo()
