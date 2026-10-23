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


def write(name, sym, parts, box, white=False, pre="g"):
    x0, y0, x1, y1 = box
    fill = "#fff" if white else BLUE
    body, inner, head = (f'<path transform="matrix(1,0,0,-1,0,768)" d="{d}"' for d in sym)
    if white:
        symbol = f'{body} fill="#fff"/>{head} fill="#fff"/>'          # 흰색판은 겹침 그림자 없이
    else:
        symbol = f'{body} fill="url(#{pre}b)"/>{inner} fill="url(#{pre}i)"/>{head} fill="url(#{pre}h)"/>'
    text = f'<g fill="{fill}">{"".join(parts)}</g>' if parts else ""
    defs = "" if white else f"<defs>{GRAD.format(p=pre)}</defs>"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" '
           f'role="img" aria-label="(주)서하P&amp;D">{defs}{text}{symbol}</svg>\n')
    path = os.path.join(OUT, name)
    open(path, "w", encoding="utf-8").write(svg)
    print(name, f"{len(svg) // 1024}KB", f"{x1 - x0}x{y1 - y0}")
    return path


ICON_BG = (3, 110, 183, 255)   # 로고 글자색 #036eb7


def icon(white_svg, size, rounded=True, fill=0.74):
    """로고 파랑 사각형 + 흰 S 마크. 4배로 그린 뒤 줄여서 가장자리를 매끈하게."""
    from PIL import Image, ImageDraw
    pix = pymupdf.open(white_svg)[0].get_pixmap(dpi=1200, alpha=True)
    sym = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    sym = sym.crop(sym.getchannel("A").getbbox())
    big = size * 4
    canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).rounded_rectangle((0, 0, big - 1, big - 1), radius=int(big * 0.22) if rounded else 0, fill=ICON_BG)
    h = int(big * fill)
    sym = sym.resize((max(1, int(sym.width * h / sym.height)), h), Image.LANCZOS)
    canvas.alpha_composite(sym, ((big - sym.width) // 2, (big - sym.height) // 2))
    return canvas.resize((size, size), Image.LANCZOS)


def icon_svg(sym, mark, path):
    """벡터 파비콘: 둥근 파랑 사각형 안에 흰 심볼 (높이 74%)."""
    x0, y0, x1, y1 = mark
    body, _, head = sym
    inner = (f'<svg x="{50 - 37 * (x1 - x0) / (y1 - y0):.2f}" y="13" width="{74 * (x1 - x0) / (y1 - y0):.2f}" height="74" '
             f'viewBox="{x0} {y0} {x1 - x0} {y1 - y0}"><g fill="#fff">'
             f'<path transform="matrix(1,0,0,-1,0,768)" d="{body}"/><path transform="matrix(1,0,0,-1,0,768)" d="{head}"/></g></svg>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#036eb7"/>{inner}</svg>' + "\n"
    open(path, "w", encoding="utf-8").write(svg)
    print(os.path.basename(path), f"{len(svg) // 1024}KB")


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
    tight = (1026, 124, 1294, 643)       # 심볼 실제 외곽 (아이콘은 여백 없이 꽉 채움)
    w = write("symbol-white.svg", sym, [], tight, white=True)
    root = os.path.join(OUT, "..", "..")
    icon_svg(sym, tight, os.path.join(root, "favicon.svg"))
    icon(w, 32).save(os.path.join(root, "favicon-32.png"))
    icon(w, 256).save(os.path.join(root, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    icon(w, 180, rounded=False, fill=0.62).save(os.path.join(root, "apple-touch-icon.png"))   # iOS가 알아서 둥글게 깎음
    icon(w, 512, rounded=False, fill=0.62).save(os.path.join(root, "icon-512.png"))
    print("favicon.ico favicon-32.png apple-touch-icon.png icon-512.png")

if __name__ == "__main__":
    main()
