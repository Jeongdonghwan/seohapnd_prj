# -*- coding: utf-8 -*-
"""회사소개 '파트너십 네트워크' 지도 → templates/_korea_map.html (인라인 SVG). 1회성.
경계: tools/data/korea_provinces_2013.json (통계청 2013 시도 경계, github.com/southkorea/southkorea-maps)
사용: python -I -X utf8 tools/build_map.py
"""
import json
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "tools", "data", "korea_provinces_2013.json")
OUT = os.path.join(ROOT, "templates", "_korea_map.html")

# 시도 코드 → 권역 (광역시는 둘러싼 도에 합침)
GROUP = {"11": "서울·경기", "23": "서울·경기", "31": "서울·경기", "32": "강원", "33": "충북", "34": "충남", "29": "충남",
         "25": "충남", "35": "전북", "36": "전남", "24": "전남", "37": "경북", "22": "경북", "38": "경남", "21": "경남",
         "26": "경남", "39": "제주"}
# 마커 위치 (경도, 위도) — 권역 중심 근처, 라벨 방향
MARK = {"서울·경기": (127.15, 37.45, "left"), "강원": (128.25, 37.70, "right"), "충북": (127.75, 36.75, "right"),
        "충남": (126.85, 36.50, "left"), "전북": (127.15, 35.75, "left"), "경북": (128.75, 36.35, "right"),
        "경남": (128.35, 35.30, "right"), "제주": (126.55, 33.38, "right")}
HQ = (126.99, 35.32)                    # 담양
K = 100
MIN_GAP = 33                            # 본사에서 나가는 선끼리 최소 각도(°)


def xy(lon, lat):
    return (lon - 125.75) * K, (38.65 - lat) * K * 1.236      # 위도 36° 보정


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for ring in poly:
            lons = [p[0] for p in ring]
            if min(lons) < 125.75 or max(lons) > 129.65:       # 백령도·울릉도 등 먼 섬은 생략 (지도를 꽉 차게)
                continue
            yield ring


def fan(angles):
    order = sorted(range(len(angles)), key=lambda i: angles[i]); a = [angles[i] for i in order]
    for _ in range(300):
        for k in range(len(a) - 1):
            g = a[k + 1] - a[k]
            if g < MIN_GAP:
                a[k] -= (MIN_GAP - g) / 2; a[k + 1] += (MIN_GAP - g) / 2
    out = [0.0] * len(a)
    for k, i in enumerate(order):
        out[i] = a[k]
    return out


def main():
    feats = json.load(open(SRC, encoding="utf-8"))["features"]
    shapes, allxy = [], []
    for f in feats:
        g = GROUP[f["properties"]["code"]]
        rs = [[xy(*p) for p in r] for r in rings(f["geometry"])]
        allxy += [q for r in rs for q in r]
        d = "".join("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in r) + "Z" for r in rs)
        if d:
            shapes.append(f'<path class="{"hq-area" if g == "전남" else "area"}" d="{d}"/>')
    hx, hy = xy(*HQ)
    names = list(MARK); pts = [xy(MARK[n][0], MARK[n][1]) for n in names]
    # 강원은 충북보다 멀어서, 출발 각도를 더 북쪽으로 줘야 두 선이 중간에 교차하지 않음
    bias = {"강원": -10}
    deps = fan([math.degrees(math.atan2(y - hy, x - hx)) + bias.get(n, 0) for n, (x, y) in zip(names, pts)])
    lines, marks = [], []
    for i, (n, (x, y), dep) in enumerate(zip(names, pts, deps)):
        ux, uy = math.cos(math.radians(dep)), math.sin(math.radians(dep)); L = math.hypot(x - hx, y - hy)
        lines.append(f'<path style="--i:{i}" d="M{hx + ux * 12:.1f},{hy + uy * 12:.1f} Q{hx + ux * L * .5:.1f},{hy + uy * L * .5:.1f} {x:.1f},{y:.1f}"/>')
        side = MARK[n][2]; tx, an = (x - 12, "end") if side == "left" else (x + 12, "start")
        marks.append(f'<g style="--i:{i}"><circle cx="{x:.1f}" cy="{y:.1f}" r="5.5"/><text x="{tx:.1f}" y="{y + 6.5:.1f}" text-anchor="{an}">{n}</text></g>')
    x0 = min(p[0] for p in allxy) - 8; y0 = min(p[1] for p in allxy) - 8
    vb = f"{x0:.0f} {y0:.0f} {max(p[0] for p in allxy) - x0 + 8:.0f} {max(p[1] for p in allxy) - y0 + 8:.0f}"
    svg = f'''{{# tools/build_map.py 로 생성. 직접 고치지 말고 스크립트 수정 후 재생성 #}}
<svg class="kmap" viewBox="{vb}" role="img" aria-label="담양 본사에서 전국 권역으로 이어지는 파트너십 네트워크 지도">
  <g class="areas">{"".join(shapes)}</g>
  <g class="lines">{"".join(lines)}</g>
  <g class="marks">{"".join(marks)}</g>
  <g class="hq"><circle class="pulse" cx="{hx:.1f}" cy="{hy:.1f}" r="8"/><circle cx="{hx:.1f}" cy="{hy:.1f}" r="8"/><text x="{hx - 16:.1f}" y="{hy + 6.5:.1f}" text-anchor="end">담양 본사</text></g>
</svg>
'''
    open(OUT, "w", encoding="utf-8").write(svg)
    print(os.path.basename(OUT), f"{len(svg) // 1024}KB")


if __name__ == "__main__":
    main()
