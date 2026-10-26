# -*- coding: utf-8 -*-
"""회사소개 '파트너십 네트워크' 지도 → templates/_korea_map.html (인라인 SVG). 1회성.
남한 윤곽은 경위도 근사 다각형(정밀 지도 아님, 점 패턴용). 담양 본사에서 권역으로 곡선 연결.
사용: python -I -X utf8 tools/build_map.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "_korea_map.html")

MAINLAND = [  # (경도, 위도) 시계방향
    (126.40, 37.75), (126.70, 37.95), (127.10, 38.30), (127.60, 38.33), (128.10, 38.30), (128.36, 38.60),
    (128.60, 38.20), (128.90, 37.80), (129.30, 37.30), (129.45, 36.80), (129.45, 36.20), (129.57, 36.00),
    (129.50, 35.70), (129.35, 35.40), (129.10, 35.10), (128.80, 35.05), (128.40, 34.85), (127.90, 34.75),
    (127.60, 34.65), (127.30, 34.50), (126.90, 34.40), (126.50, 34.30), (126.30, 34.55), (126.35, 34.90),
    (126.40, 35.30), (126.60, 35.60), (126.70, 35.95), (126.55, 36.20), (126.20, 36.60), (126.40, 36.95),
    (126.80, 37.00), (126.60, 37.30), (126.60, 37.55),
]
JEJU = (126.55, 33.38, 0.36, 0.14)          # 중심 경도, 위도, 반지름(경도), 반지름(위도)
HQ = ("담양 본사", 126.99, 35.32)
REGIONS = [  # 이름, 경도, 위도, 라벨 위치(left/right)
    ("서울·경기", 127.00, 37.45, "left"), ("강원", 128.30, 37.75, "right"), ("충남", 126.80, 36.50, "left"),
    ("충북", 127.75, 36.80, "right"), ("경북", 128.75, 36.30, "right"), ("전북", 127.10, 35.82, "left"),
    ("경남", 128.40, 35.30, "right"), ("제주", 126.55, 33.40, "right"),
]
K, LAT_K = 100, 124                      # 경도 1° = 100, 위도 1° = 124 (위도 36° 보정)


def xy(lon, lat):
    return round((lon - 125.7) * K, 1), round((38.75 - lat) * LAT_K, 1)


def main():
    pts = " ".join(f"{x},{y}" for x, y in (xy(*p) for p in MAINLAND))
    jx, jy = xy(JEJU[0], JEJU[1])
    hx, hy = xy(HQ[1], HQ[2])
    lines, marks = [], []
    for i, (name, lon, lat, side) in enumerate(REGIONS):
        x, y = xy(lon, lat)
        cx, cy = (hx + x) / 2 + (y - hy) * 0.18, (hy + y) / 2 - (x - hx) * 0.18      # 살짝 휘는 곡선
        lines.append(f'<path class="nl" style="--i:{i}" d="M{hx},{hy} Q{cx:.1f},{cy:.1f} {x},{y}"/>')
        tx, anchor = (x - 12, "end") if side == "left" else (x + 12, "start")
        marks.append(f'<g class="nm" style="--i:{i}"><circle cx="{x}" cy="{y}" r="5"/><text x="{tx}" y="{y + 5}" text-anchor="{anchor}">{name}</text></g>')
    svg = f'''{{# tools/build_map.py 로 생성. 직접 고치지 말고 스크립트를 수정 후 재생성 #}}
<svg class="kmap" viewBox="0 0 420 700" role="img" aria-label="담양 본사와 전국 권역을 잇는 파트너십 네트워크 지도">
  <defs><pattern id="kdots" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.1"/></pattern></defs>
  <g class="land"><polygon points="{pts}"/><ellipse cx="{jx}" cy="{jy}" rx="{JEJU[2] * K:.0f}" ry="{JEJU[3] * LAT_K:.0f}"/></g>
  <g class="lines">{"".join(lines)}</g>
  <g class="marks">{"".join(marks)}</g>
  <g class="hq"><circle class="pulse" cx="{hx}" cy="{hy}" r="9"/><circle cx="{hx}" cy="{hy}" r="9"/><text x="{hx - 16}" y="{hy + 6}" text-anchor="end">{HQ[0]}</text></g>
</svg>
'''
    open(OUT, "w", encoding="utf-8").write(svg)
    print(os.path.basename(OUT), f"{len(svg)}B")


if __name__ == "__main__":
    main()
