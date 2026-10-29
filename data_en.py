# -*- coding: utf-8 -*-
"""영문 콘텐츠. data.py와 구조·slug·순서가 같아야 함 (test_smoke가 확인). 국문 수정 시 여기도 같이."""

COMPANY = {
    "name": "SEOHA P&D",
    "legal": "Seoha P&D Co., Ltd. (Agricultural Corporation)",
    "en": "SEOHA P&D CO., Ltd.",
    "brand": "Yongpyo",
    "ceo": "Kim Jae-hong",
    "addr": "34-5 Mujeonggongdan-gil, Mujeong-myeon, Damyang-gun, Jeollanam-do, Republic of Korea",
    "tel": "+82-61-382-7405",
    "fax": "+82-61-382-7407",
    "biz_no": "602-86-01416",
    "founded": 2019,
    "brand_line": "Growing together with farmers, sharing their harvest",
    "hours": "Weekdays 09:00 – 18:00 KST (closed weekends and public holidays)",
    "map_q": "전라남도 담양군 무정면 무정공단길 34-5",
}

PRODUCTS = [
    {
        "slug": "ld-mulching", "name": "LD Agricultural Mulching Film", "short": "LD Mulching", "box": True,
        "lead": "A basic mulching film with high light transmission and strong resistance to tearing",
        "features": [
            "Stabilizes soil temperature, keeps soil moisture, prevents loss of soil and nutrients, and suppresses weeds",
            "Higher light transmission than HD film and resistant to bursting, for an efficient mulching material",
            "Produced as black, clear or bicolor mulching depending on use",
        ],
        "colors": "Black · Clear · Green · Black bicolor · Green bicolor",
        "note": "Bicolor film combines the strengths of clear and black film: the clear part raises soil temperature and the black part suppresses weeds.",
        "spec": {"Thickness": "0.012 mm ~", "Width": "Up to 300 cm (600 cm folded)", "Perforation": "Available", "Packaging": "Box & Roll"},
    },
    {
        "slug": "hd-mulching", "name": "HD Agricultural Mulching Film", "short": "HD Mulching", "box": True,
        "lead": "A highly durable mulching film with excellent soil-warming effect",
        "features": [
            "Highly durable mulching film with an excellent soil-warming effect",
            "Produced as black, clear or bicolor mulching depending on use",
        ],
        "colors": "Black · Clear · Bicolor",
        "note": "Bicolor film combines the strengths of clear and black film: the clear part raises soil temperature and the black part suppresses weeds.",
        "spec": {"Thickness": "0.012 mm ~", "Width": "Up to 150 cm", "Perforation": "Available", "Packaging": "Roll"},
    },
    {
        "slug": "jangsu", "name": "Long-life Film / Black Long-life / Skirt Film / Band Film", "short": "Long-life · Skirt · Band", "box": True,
        "lead": "Long-life film that stands up to strong wind and heavy snow, plus skirt and band films for ventilation work",
        "features": [
            "Less oxidation on the side touching the greenhouse frame",
            "Excellent durability against strong wind and heavy snow",
            "Little shrinkage or fusion, for efficient installation",
            "Band film prevents tearing when ventilation openings are opened and closed",
            "Works with nylon, binder and CC-lon ties",
        ],
        "colors": "Clear · Black",
        "spec": {"Thickness": "0.05 ~ 0.2 mm", "Width": "Single band 40–250 cm · Double band 40–250 cm", "Perforation": "-", "Packaging": "Box / Roll"},
    },
    {
        "slug": "green", "name": "Green Agricultural Film", "short": "Green Mulching", "box": True,
        "lead": "The soil-warming effect of clear mulch and the weed control of black mulch in one film",
        "features": [
            "Transmits infrared light to warm the soil like clear mulch, while cutting visible light to suppress weeds like black mulch",
            "Soil runs 1–3 °C warmer than under black mulch, improving early growth, raising yield and bringing harvest forward",
            "Far fewer weeds than clear film",
            "Also available as green bicolor film",
        ],
        "colors": "Green · Green bicolor",
        "spec": {"Thickness": "Green 0.025 mm ~ / Green bicolor 0.02 mm ~", "Width": "Up to 300 cm (600 cm folded)", "Perforation": "Available", "Packaging": "Box & Roll"},
    },
    {
        "slug": "bw", "name": "Black & White Agricultural Film", "short": "Black & White", "box": True,
        "lead": "Summer mulching that lowers soil temperature to prevent heat damage",
        "features": [
            "Keeps soil 2–4 °C cooler on average than standard mulch in the summer heat, preventing heat damage",
            "Gives a highland-like cooling effect in open fields",
            "For open-field summer mulching from May–June, and for crops that need cool soil in summer",
            "Suppresses pests and disease",
        ],
        "colors": "Black & White",
        "spec": {"Thickness": "0.03 mm ~", "Width": "Up to 200 cm (400 cm folded)", "Perforation": "Available", "Packaging": "Box & Roll"},
    },
    {
        "slug": "perforated", "name": "Micro-perforated Film (Green / Black & White)", "short": "Micro-perforated", "box": True,
        "lead": "Breathable mulching that regulates moisture and gas through fine perforations",
        "features": [
            "Breathable film with fine perforations at regular intervals across the whole sheet",
            "Regulates moisture and gas to reduce root damage",
            "The film expands and contracts with temperature",
            "Suppresses soil-borne pests and disease",
        ],
        "colors": "Green · Black & White",
        "spec": {"Thickness": "Green 0.025 mm ~ / Black & White 0.03 mm ~", "Width": "Green up to 300 cm / Black & White up to 200 cm", "Perforation": "Micro-perforated", "Packaging": "Box & Roll"},
    },
    {
        "slug": "eroun-bio", "name": "E-Roun Biodegradable Film", "short": "E-Roun Biodegradable", "box": False, "bio": True,
        "lead": "Good for the soil, good for farmers, good for crops: a biodegradable mulching film",
        "intro": "E-Roun biodegradable film carries the Korea Eco-Label (EL724). Soil microorganisms break it down into water (H₂O), carbon dioxide (CO₂) and biomass, so it returns to the soil as compost.",
        "features": [
            "Broken down by microorganisms in nature and returned to the soil",
            "Keeps soil warm and moist to promote germination and growth",
            "Blocks light to suppress weeds effectively",
            "No collection or disposal needed, reducing pollution",
            "Saves the cost and time of collecting and disposing of film",
            "Durable with stable physical properties in the field",
        ],
        "crops": ["Tomato · Oriental melon · Watermelon", "Cabbage · Radish · Onion · Garlic", "Other open-field crops"],
        "cautions": [
            "Use only as agricultural mulching film (open-field cultivation)",
            "Do not use in tunnels or irrigated greenhouses, where it may break down early",
            "Ensure good drainage; standing water can cause early hydrolysis",
            "Use within one month of purchase; do not store or reuse",
            "Store in a shaded place away from direct sunlight (it may break down early in hot, humid or wet conditions)",
            "We are not responsible for early breakdown caused by compost or pesticides containing sulfur or chlorine",
            "Always rotary-till the field after harvest",
            "Breakdown timing varies with rainfall, temperature and soil conditions",
        ],
        "colors": "Black · Clear",
        "spec": {"Thickness": "0.012 mm ~", "Width": "Up to 200 cm", "Perforation": "Available", "Packaging": "Roll"},
    },
    {
        "slug": "duct", "name": "Duct Film", "short": "Duct Film", "box": True,
        "lead": "Film for greenhouse ventilation and heating ducts, in standard and long-life types",
        "features": ["Standard duct", "Long-life duct"],
        "colors": "Clear",
        "spec": {"Thickness": "Inquire", "Width": "Inquire", "Perforation": "Available", "Packaging": "Box / Roll"},
    },
]
PRODUCT_MAP = {p["slug"]: p for p in PRODUCTS}

SPEC_ROWS = [
    ("LD", "Black", "0.012~", "Up to 300 · 600 folded", "O", "Box & Roll"),
    ("LD", "Clear", "0.012~", "Up to 300 · 600 folded", "O", "Box & Roll"),
    ("LD", "Green", "0.025~", "Up to 300 · 600 folded", "O", "Box & Roll"),
    ("LD", "Black bicolor", "0.012~", "Up to 300 · 600 folded", "O", "Roll"),
    ("LD", "Green bicolor", "0.02~", "Up to 300 · 600 folded", "O", "Roll"),
    ("HD", "Black", "0.012~", "Up to 150", "O", "Roll"),
    ("HD", "Clear", "0.012~", "Up to 150", "O", "Roll"),
    ("HD", "Bicolor", "0.012~", "Up to 150", "O", "Roll"),
    ("Black & White Film", "", "0.03~", "Up to 200 · 400 folded", "O", "Box & Roll"),
    ("Micro-perforated Film", "Green", "0.025~", "Up to 300", "Micro", "Box & Roll"),
    ("Micro-perforated Film", "Black & White", "0.03~", "Up to 200", "Micro", "Box & Roll"),
    ("Long-life / Black Long-life / Skirt / Band Film", "", "0.05~0.2", "Single band 40–250 · Double band 40–250", "", "Box / Roll"),
    ("Duct Film", "", "Inquire\nPerforation available", "Standard duct · Long-life duct", "Available", "Box / Roll"),
    ("E-Roun Biodegradable Film", "Black · Clear", "0.012~", "Up to 200", "O", "Roll"),
]

CERTS = [
    {"key": "eco-label", "name": "Korea Eco-Label Certification", "short": "Korea Eco-Label", "org": "Korea Environmental Industry & Technology Institute",
     "detail": "No. 29524 · EL724 biodegradable resin products · Yongpyo biodegradable mulching film", "period": "2023.12.05 – 2026.12.04", "kind": "cert"},
    {"key": "innobiz", "name": "Innovative SME (Inno-Biz)", "short": "Inno-Biz Grade A", "org": "Ministry of SMEs and Startups",
     "detail": "No. 240401-00696 · Grade A", "period": "2024.06.17 – 2027.06.16", "kind": "cert"},
    {"key": "venture", "name": "Venture Business Certification", "short": "Venture Business", "org": "Venture Business Confirmation Agency",
     "detail": "Innovation growth type", "period": "2024.08.29 – 2027.08.28", "kind": "cert"},
    {"key": "root", "name": "Root Industry Company Certification", "short": "Root Industry Company", "org": "Korea Institute of Industrial Technology",
     "detail": "No. 24122-24995", "period": "2024.10.21 – 2027.10.20", "kind": "cert"},
    {"key": "sobujang", "name": "Materials, Parts & Equipment Specialist Company", "short": "Materials & Parts Specialist", "org": "Korea Evaluation Institute of Industrial Technology",
     "detail": "No. 41850", "period": "2026.04.21 – 2029.04.20", "kind": "cert"},
    {"key": "sps", "name": "Excellent Group Standard Product (SPS)", "short": "SPS Group Standard", "org": "Korea Federation of Plastic Industry Cooperatives",
     "detail": "Agricultural polyethylene film HD / LLD · SPS-KPS M 1001-0806", "period": "2025.08.19 – 2028.08.18 (first 2019.08.19)", "kind": "cert"},
    {"key": "rnd", "name": "Dedicated R&D Department", "short": "Dedicated R&D Department", "org": "Ministry of Science and ICT · Korea Industrial Technology Association",
     "detail": "No. 2023151655", "period": "First recognized 2023.03.13", "kind": "cert"},
    {"key": "patent-2262234", "name": "Patent No. 10-2262234", "short": "Patent · Perforated Film Spreader", "org": "Korean Intellectual Property Office",
     "detail": "Device for spreading the protrusions of perforated vinyl", "period": "Registered 2021.06.02", "kind": "patent"},
    {"key": "patent-1647358", "name": "Patent No. 10-1647358", "short": "Patent · Antibacterial Protein Film", "org": "Korean Intellectual Property Office",
     "detail": "Method for producing antibacterial makgeolli-lees protein film containing wasabi extract", "period": "Registered 2016.08.04 · transferred 2026.07", "kind": "patent"},
]

ORG = ["Production 1", "Production 2", "Management Support", "Sales", "Shipping", "R&D Team"]

FACTORY = [
    {"img": "line-tower", "cap": "Blown film extrusion tower 1"},
    {"img": "line-wide", "cap": "Blown film extrusion tower 2"},
    {"img": "line-green", "cap": "Film production & stacking 1"},
    {"img": "line-rolls", "cap": "Film production & stacking 2"},
    {"img": "packing", "cap": "Packing & shipping"},
    {"img": "exterior", "cap": "Head office & plant, Mujeong Industrial Complex, Damyang"},
]

NAV = [
    ("about", "About"), ("products", "Products"), ("spec", "Specifications"),
    ("certifications", "Certifications"), ("factory", "Facilities"), ("inquiry", "Contact"),
]

BIO_STEPS = ["Right after mulching", "Growing season", "Breakdown begins after harvest", "Returned to the soil"]

GREETING = [
    "Thank you for visiting Seoha P&D. We are grateful to every customer, farmer and partner who works with us.",
    "Seoha P&D researches and manufactures high-quality agricultural mulching film and eco-friendly biodegradable film for the future of farming, supplying farms and industry with the materials they need.",
    "We know how directly agricultural film affects soil protection and productivity. That is why, alongside eco-friendly innovation that reduces environmental burden, we hold two principles above all others: the highest product quality and strict on-time delivery.",
    "Even the best film cannot secure a harvest unless it arrives in time for the growing season and passes thorough quality checks. With our own technical know-how and tight process control, we deliver dependable film exactly when it is needed.",
    "Seoha P&D will keep advancing its film technology to make farming more sustainable, and to remain a partner that keeps every promise to its customers.",
]

HISTORY = [
    ("2019.02", "Seoha P&D founded; plant in Mujeong Industrial Complex, Damyang begins operation"),
    ("2019.08", "Certified as an Excellent Group Standard (SPS) product: agricultural PE film HD·LLD"),
    ("2021.06", "Patent registered: device for spreading the protrusions of perforated vinyl"),
    ("2021.07", "Mulching film registered with the National Agricultural Cooperative Federation (NongHyup)"),
    ("2023.03", "Dedicated R&D department recognized"),
    ("2023.12", "E-Roun biodegradable mulching film earns the Korea Eco-Label (EL724)"),
    ("2024", "Certified as Inno-Biz (Grade A), Venture Business and Root Industry Company"),
    ("2026.04", "Certified as a Materials, Parts & Equipment Specialist Company"),
    ("2026.07", "Patent transferred: antibacterial makgeolli-lees protein film containing wasabi extract"),
]
