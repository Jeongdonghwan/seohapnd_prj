# -*- coding: utf-8 -*-
"""로고 AI 원본 → static/img/logo/*.svg + 파비콘·애플 아이콘 PNG. 1회성.
사용: python -I -X utf8 tools/build_logo.py "<서하피엔디 로고.ai>"

원본 구성 (1366×768 아트보드 좌표): 위 '농·업·회·사·법·인'(y≈220~270), 가운데 '(주)서하P&D'(y≈300~495),
아래 영문(y≈510~545), 오른쪽 S 심볼(x≈1026~1294). S 심볼의 그라데이션은 AI 안에서 래스터 이미지라
클립 모양만 가져와 SVG linearGradient로 다시 칠한다 (색은 원본 이미지에서 샘플링).
"""
import os
import re
import sys

import pymupdf

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "img", "logo")
BLUE = "#036eb7"
FLAT = "#2e4871"   # PNG 아이콘용 단색 (MuPDF는 SVG 그라데이션을 못 그림)
GRAD = """<linearGradient id="{p}b" gradientUnits="userSpaceOnUse" x1="1026" y1="0" x2="1294" y2="0"><stop offset="0" stop-color="#3a6b9e"/><stop offset="1" stop-color="#0b0b1f"/></linearGradient>
<linearGradient id="{p}i" gradientUnits="userSpaceOnUse" x1="1132" y1="0" x2="1273" y2="0"><stop offset="0" stop-color="#0b0b1f"/><stop offset="1" stop-color="#2a3a5e"/></linearGradient>
<linearGradient id="{p}h" gradientUnits="userSpaceOnUse" x1="1171" y1="585" x2="1230" y2="644"><stop offset="0" stop-color="#3a6b9e"/><stop offset=".55" stop-color="#1a2244"/><stop offset="1" stop-color="#0b0b1f"/></linearGradient>"""


def parse(ai):
    svg = pymupdf.open(ai)[0].get_svg_image(text_as_path=True)
    clips = dict(re.findall(r'<clipPath id="(clip_\d+)">\s*<path transform="[^"]+" d="([^"]+)"', svg))
    sym = [clips["clip_2"], clips["clip_3"], clips["clip_4"]]          # 몸통, 안쪽 겹침, 머리
    rows = {"top": [], "main": [], "en": []}
    for tf, d in re.findall(r'<path transform="matrix\(([^)]+)\)" d="([^"]+)" fill="#036eb7"', svg):
        a, b, c, dd, e, f = map(float, tf.split(","))
        x0, y0 = map(float, re.findall(r"-?\d*\.?\d+", d)[:2])
        y = f - y0                                                     # matrix(1,0,0,-1,e,f): 화면 y = f - y
        rows["top" if y < 290 else "main" if y < 500 else "en"].append(f'<path transform="matrix({tf})" d="{d}"/>')
    assert len(sym) == 3 and all(rows.values()), {k: len(v) for k, v in rows.items()}
    return sym, rows


def write(name, sym, parts, box, white=False, pre="g", flat=None):
    x0, y0, x1, y1 = box
    fill = "#fff" if white else BLUE
    body, inner, head = (f'<path transform="matrix(1,0,0,-1,0,768)" d="{d}"' for d in sym)
    if white or flat:
        c = flat or "#fff"
        symbol = f'{body} fill="{c}"/>{head} fill="{c}"/>'            # 흰색·단색판은 겹침 그림자 없이
    else:
        symbol = f'{body} fill="url(#{pre}b)"/>{inner} fill="url(#{pre}i)"/>{head} fill="url(#{pre}h)"/>'
    text = f'<g fill="{fill}">{"".join(parts)}</g>' if parts else ""
    defs = "" if white or flat else f"<defs>{GRAD.format(p=pre)}</defs>"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" '
           f'role="img" aria-label="(주)서하P&amp;D">{defs}{text}{symbol}</svg>\n')
    path = os.path.join(OUT, name)
    open(path, "w", encoding="utf-8").write(svg)
    print(name, f"{len(svg) // 1024}KB", f"{x1 - x0}x{y1 - y0}")
    return path


def png(svg_path, out, size, bg=None, pad=0.12):
    """SVG → 정사각 PNG (심볼 아이콘용)."""
    from PIL import Image
    pix = pymupdf.open(svg_path)[0].get_pixmap(dpi=600, alpha=True)
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    inner = int(size * (1 - 2 * pad))
    im.thumbnail((inner, inner), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    canvas.alpha_composite(im, ((size - im.width) // 2, (size - im.height) // 2))
    canvas.save(out)
    print(os.path.basename(out), canvas.size)


def main():
    os.makedirs(OUT, exist_ok=True)
    sym, rows = parse(sys.argv[1])
    full = (60, 112, 1310, 655)          # 전체 (여백 약간)
    header = (66, 118, 1300, 649)        # (주)서하P&D + 심볼
    mark = (1020, 118, 1300, 649)        # 심볼만
    allp = rows["top"] + rows["main"] + rows["en"]
    write("logo.svg", sym, allp, full, pre="f")
    write("logo-white.svg", sym, allp, full, white=True)
    write("logo-h.svg", sym, rows["main"], header, pre="h")
    write("logo-h-white.svg", sym, rows["main"], header, white=True)
    write("symbol.svg", sym, [], mark, pre="s")
    m = write("symbol-flat.svg", sym, [], mark, flat=FLAT)
    root = os.path.join(OUT, "..", "..")
    png(m, os.path.join(root, "apple-touch-icon.png"), 180, bg=(255, 255, 255, 255))
    png(m, os.path.join(root, "favicon-32.png"), 32, pad=0.04)
    png(m, os.path.join(root, "icon-512.png"), 512, bg=(255, 255, 255, 255))


if __name__ == "__main__":
    main()
