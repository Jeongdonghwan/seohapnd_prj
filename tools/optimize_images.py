# -*- coding: utf-8 -*-
"""원본 자료 → static/img WebP. 1회성. 사용: python tools/optimize_images.py "<자료 폴더>" """
import glob, os, sys
from PIL import Image, ImageChops, ImageOps
import pymupdf


def trim(im, pad=6):
    """팜플렛 크롭의 민트/흰 여백 제거: 네 모서리 색과 다른 영역의 bbox."""
    im = im.convert("RGB")
    for _ in range(2):
        bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
        bbox = ImageChops.difference(im, bg).point(lambda v: 255 if v > 40 else 0).getbbox()
        if not bbox:
            break
        im = im.crop(bbox)
    w, h = im.size
    return im.crop((pad, pad, w - pad, h - pad)) if w > 2 * pad and h > 2 * pad else im


SRC = sys.argv[1]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
IMG = os.path.join(ROOT, "img")


def save(im, path, max_side, q=82):
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((max_side, max_side))
    im.save(path, "WEBP", quality=q)
    print(os.path.relpath(path, ROOT), im.size)


# 현장 사진 → hero(1920) + factory(1200)
PHOTOS = {  # 원본 파일명: 저장명
    "KakaoTalk_20260323_143541991.jpg": "line-rolls",
    "KakaoTalk_20260323_143544214.jpg": "line-green",
    "KakaoTalk_20260323_143546476.jpg": "exterior",
    "KakaoTalk_20260323_144002441.jpg": "bio-rolls",
    "현장사진.JPG": "line-tower",
    "현장사진2.JPG": "line-wide",
}
for src, name in PHOTOS.items():
    im = Image.open(os.path.join(SRC, src))
    save(im, os.path.join(IMG, "factory", f"{name}.webp"), 1400)
    if name in ("line-rolls", "line-green", "line-tower"):
        save(im, os.path.join(IMG, "hero", f"{name}.webp"), 1920, 78)

# 팜플렛 → 브로슈어 PDF + 제품 썸네일 크롭
p1 = ImageOps.exif_transpose(Image.open(os.path.join(SRC, "웹사이트 팜플렛자료 (1).jpg"))).convert("RGB")
p2 = ImageOps.exif_transpose(Image.open(os.path.join(SRC, "웹사이트 팜플렛자료 (2).jpg"))).convert("RGB")
a, b = p2.copy(), p1.copy()
a.thumbnail((3000, 3000)); b.thumbnail((3000, 3000))
a.save(os.path.join(ROOT, "brochure.pdf"), "PDF", resolution=150, save_all=True, append_images=[b])
print("brochure.pdf")
W, H = p1.size  # 6531 x 3035, 3단 접지: 좌측 사진 컬럼 / 중앙 사진 컬럼 / 우측 생분해
# 좌표는 원본 비율 기준 (팜플렛 1 안쪽면 사진 컬럼). 대략값 → 제품 썸네일 임시용
CROPS = {
    "ld-mulching": (0.00, 0.02, 0.12, 0.21),
    "hd-mulching": (0.00, 0.41, 0.12, 0.60),
    "jangsu": (0.00, 0.78, 0.12, 0.98),
    "green": (0.345, 0.02, 0.465, 0.21),
    "bw": (0.345, 0.42, 0.465, 0.60),
    "perforated": (0.345, 0.80, 0.465, 0.98),
    "eroun-bio": (0.84, 0.23, 0.98, 0.42),
    "bio-step1": (0.675, 0.45, 0.755, 0.61),
    "bio-step2": (0.76, 0.45, 0.835, 0.61),
    "bio-step3": (0.84, 0.45, 0.915, 0.61),
    "bio-step4": (0.92, 0.45, 0.995, 0.61),
}
for name, (l, t, r, bt) in CROPS.items():
    save(trim(p1.crop((int(W * l), int(H * t), int(W * r), int(H * bt)))), os.path.join(IMG, "products", f"{name}.webp"), 900)
# 닥트용은 사진 없음 → 생산라인 사진 재사용
save(Image.open(os.path.join(SRC, "현장사진2.JPG")), os.path.join(IMG, "products", "duct.webp"), 900)

# 인증서 PDF 1페이지 → PNG(webp)
CERTS = {
    "환경표지인증.pdf": "eco-label", "이노비즈.pdf": "innobiz", "벤처기업확인서.pdf": "venture",
    "뿌리기업 확인서.pdf": "root", "소부장 확인서.pdf": "sobujang", "우수단체확인서.pdf": "sps",
    "기업부설연구소.pdf": "rnd", "특허등록증_10-1647358.pdf": "patent-1647358", "특허증.pdf": "patent-2262234",
}
for src, name in CERTS.items():
    pix = pymupdf.open(os.path.join(SRC, src))[0].get_pixmap(dpi=110)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    save(im, os.path.join(IMG, "certs", f"{name}.webp"), 1100, 80)
