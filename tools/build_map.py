# -*- coding: utf-8 -*-
"""회사소개 '파트너십 네트워크' 지도 → templates/_korea_map.html (인라인 SVG). 1회성.
남한 윤곽은 경위도 근사 다각형(정밀 지도 아님, 점 패턴용). 담양 본사에서 권역으로 곡선 연결.
사용: python -I -X utf8 tools/build_map.py
"""
import math
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
REGIONS = [  # 이름, 경도, 위도, 라벨 위치
    ("서울·경기", 127.05, 37.45, "left"), ("강원", 128.30, 37.75, "right"), ("충남", 126.75, 36.55, "left"),
    ("충북", 127.75, 36.80, "right"), ("경북", 128.75, 36.30, "right"), ("전북", 127.25, 35.85, "right"),
    ("경남", 128.40, 35.30, "right"), ("제주", 126.55, 33.40, "right"),
]
MIN_GAP = 30      # 본사에서 출발하는 선끼리 최소 각도(°). 키우면 더 넓게 퍼짐


def fan(angles):
    """목표 방향이 비슷한 선들의 출발 각도를 MIN_GAP 이상 벌린다 (이웃끼리 반씩 밀어내기 반복)."""
    order = sorted(range(len(angles)), key=lambda i: angles[i])
    a = [angles[i] for i in order]
    for _ in range(200):
        for k in range(len(a) - 1):
            gap = a[k + 1] - a[k]
            if gap < MIN_GAP:
                a[k] -= (MIN_GAP - gap) / 2
                a[k + 1] += (MIN_GAP - gap) / 2
    out = [0.0] * len(a)
    for k, i in enumerate(order):
        out[i] = a[k]
    return out
K, LAT_K = 100, 124                      # 경도 1° = 100, 위도 1° = 124 (위도 36° 보정)


def xy(lon, lat):
    return round((lon - 125.7) * K, 1), round((38.75 - lat) * LAT_K, 1)


def main():
    pts = " ".join(f"{x},{y}" for x, y in (xy(*p) for p in MAINLAND))
    jx, jy = xy(JEJU[0], JEJU[1])
    hx, hy = xy(HQ[1], HQ[2])
    lines, marks = [], []
    pts_xy = [xy(lon, lat) for _, lon, lat, _ in REGIONS]
    deps = fan([math.degrees(math.atan2(y - hy, x - hx)) for x, y in pts_xy])
    for i, ((name, _, _, side), (x, y), dep) in enumerate(zip(REGIONS, pts_xy, deps)):
        ux, uy = math.cos(math.radians(dep)), math.sin(math.radians(dep))
        L = math.hypot(x - hx, y - hy)
        sx, sy = hx + ux * 17, hy + uy * 17                    # 본사 원 가장자리에서, 벌린 각도로 출발
        cx, cy = hx + ux * L * 0.5, hy + uy * L * 0.5        # 출발 방향으로 뻗다가 목표로 휘어 들어감
        lines.append(f'<path class="nl" style="--i:{i}" d="M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {x},{y}"/>')
        tx, anchor = (x - 12, "end") if side == "left" else (x + 12, "start")
        marks.append(f'<g class="nm" style="--i:{i}"><circle cx="{x}" cy="{y}" r="4"/><text x="{tx}" y="{y + 4.5}" text-anchor="{anchor}">{name}</text></g>')
    svg = f'''{{# tools/build_map.py 로 생성. 직접 고치지 말고 스크립트를 수정 후 재생성 #}}
<svg class="kmap" viewBox="0 0 420 700" role="img" aria-label="담양 본사와 전국 권역을 잇는 파트너십 네트워크 지도">
  <defs><pattern id="kdots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.6"/></pattern></defs>
  <g class="land"><polygon points="{pts}"/><ellipse cx="{jx}" cy="{jy}" rx="{JEJU[2] * K:.0f}" ry="{JEJU[3] * LAT_K:.0f}"/></g>
  <g class="lines">{"".join(lines)}</g>
  <g class="marks">{"".join(marks)}</g>
  <g class="hq"><circle class="pulse" cx="{hx}" cy="{hy}" r="8"/><circle class="ring" cx="{hx}" cy="{hy}" r="13"/><circle cx="{hx}" cy="{hy}" r="7"/><text x="{hx - 20}" y="{hy + 5}" text-anchor="end">{HQ[0]}</text></g>
</svg>
'''
    open(OUT, "w", encoding="utf-8").write(svg)
    print(os.path.basename(OUT), f"{len(svg)}B")


if __name__ == "__main__":
    main()
