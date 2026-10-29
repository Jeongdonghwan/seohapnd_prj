# -*- coding: utf-8 -*-
"""화면 문구 영문 사전. 키 = 템플릿의 국문 원문 그대로. 템플릿에서 {{ _('국문') }}, 파이썬에서 t('국문').
국문 문구를 고치면 여기 키도 같이 고칠 것 — test_smoke가 빠진 키와 영문 페이지의 한글을 잡는다."""
from flask import g

EN = {
    # 공통
    "홈": "Home", "홈으로": "Back to home", "메뉴": "Menu", "대표": "CEO", "사업자등록번호": "Business Reg. No.",
    "브로슈어 PDF": "Brochure PDF (Korean)", "닫기": "Close", "크게 보기": "enlarge", "확인": "OK",
    "농업용 멀칭필름 전문 제조": "Agricultural Mulching Film Manufacturer",
    "담양 농업회사법인 (주)서하P&D. 용표 농업용 LD·HD 멀칭필름, 녹색·흑백·침공 필름, 환경표지 인증 이로운 생분해 필름 제조.":
        "SEOHA P&D, an agricultural corporation in Damyang, Korea, manufactures LD/HD mulching film, green, black & white and micro-perforated film, and Eco-Label certified E-Roun biodegradable film.",
    "페이지를 찾을 수 없습니다": "Page not found",
    "주소가 바뀌었거나 준비 중인 페이지입니다.": "The address may have changed, or the page is not ready yet.",
    "페이지가 오래되어 다시 시도해 주세요.": "This page has expired. Please try again.",

    # 메인
    "농업회사법인 (주)서하P&D": "SEOHA P&D Agricultural Corporation",
    "작물의 품질 향상과<br>생산성 증대를 위해": "Better crops,<br>higher yields",
    "최고의 제품, 최고의 품질로 보답하겠습니다.<br>농업용 멀칭필름 · 이로운 생분해 필름 전문 제조":
        "We answer with the best products and the best quality.<br>Agricultural mulching film · E-Roun biodegradable film",
    "제품 보기": "View products", "문의하기": "Contact us", "소리 끄기": "Sound off", "소리 켜기": "Sound on", "아래로": "Scroll down",
    "제품": "Products",
    "작물과 계절에 맞는 멀칭필름 {n}종": "{n} mulching films for every crop and season",
    "LD·HD 기본 멀칭부터 지온을 올리는 녹색, 내리는 흑백, 통기성 침공, 그리고 땅으로 돌아가는 생분해까지.":
        "From standard LD/HD mulch to green film that warms the soil, black & white film that cools it, breathable micro-perforated film, and biodegradable film that returns to the earth.",
    "전체 제품 →": "All products →",
    "환경표지 인증 생분해 필름": "Eco-Label certified biodegradable film",
    "이로운 생분해 필름": "E-Roun Biodegradable Film",
    "생분해 필름 자세히": "About biodegradable film",
    "생산설비": "Facilities",
    "담양 무정공단에서 직접 압출·생산합니다": "Extruded and produced in-house in Damyang",
    "블로운 필름 압출 타워에서 두께 0.012mm부터 최대 폭 600cm까지. SPS 우수단체표준 인증 HD·LLD 농업용 폴리에틸렌 필름을 자체 라인에서 생산하고 출하합니다.":
        "Our blown film towers produce film from 0.012 mm thick and up to 600 cm wide. SPS-certified HD/LLD agricultural polyethylene film is made and shipped from our own lines.",
    "생산설비 더 보기": "More about our facilities",
    "인증 · 특허": "Certifications · Patents",
    "인증과 특허로 증명하는 품질": "Quality proven by certifications and patents",
    "인증·특허 전체 보기 →": "All certifications →",
    "문의": "Contact",
    "제품 구입·견적·규격 문의": "Purchasing, quotes and specifications",
    "문의게시판": "Inquiry Board",

    # 회사소개
    "회사소개": "About Us",
    "2019년 담양 무정공단에서 시작한 농업용 멀칭필름 전문 제조사. 인사말, 조직, 오시는 길.":
        "Agricultural mulching film manufacturer founded in 2019 in Damyang, Korea. Greeting, organization and location.",
    "농민과 함께 발전하고, 농민과 함께 행복해 하는 회사": "Growing together with farmers, sharing their harvest",
    "인사말": "Greeting",
    "지속 가능한 농업을 위한 친환경 혁신,<br>완벽한 품질과 엄격한 납기로<br>고객과의 약속을 지킵니다.":
        "Eco-friendly innovation for sustainable farming.<br>Uncompromising quality and on-time delivery<br>keep our promise to customers.",
    "(주)서하피엔디 대표이사": "CEO, Seoha P&D Co., Ltd.",
    "기업 정보": "Company", "회사 개요": "Company Overview", "상호": "Company name", "대표이사": "CEO",
    "설립": "Founded", "{y}년 2월": "February {y}", "업종": "Business",
    "농업용 폴리에틸렌 필름 제조 (멀칭필름 · 생분해필름)": "Agricultural polyethylene film manufacturing (mulching film · biodegradable film)",
    "브랜드": "Brands", "이로운(E-Roun)": "E-Roun", "소재지": "Address", "연락처": "Phone",
    "네트워크": "Network", "파트너십 네트워크": "Partnership Network",
    "전국<br>협력 네트워크": "Nationwide<br>partners",
    "전국 300+<br>파트너십 네트워크": "300+ partners<br>across Korea",
    "농협 · 대리점과 함께 구축한 전국 단위 협력 기반": "A nationwide supply base built with NongHyup cooperatives and dealers",
    "연혁": "History", "걸어온 길": "Our History", "조직": "Organization", "조직도": "Organization Chart",
    "오시는 길": "Location", "오시는 길 지도": "Location map", "본사 전경": "Head office",

    # 제품
    "농업용 LD·HD 멀칭필름, 장수·치마·끈 필름, 녹색·흑백·침공 필름, 환경표지 인증 이로운 생분해 필름.":
        "LD/HD agricultural mulching film, long-life, skirt and band film, green, black & white and micro-perforated film, and Eco-Label certified E-Roun biodegradable film.",
    "작물과 계절에 맞는 농업용 멀칭필름 {n}종을 담양 공장에서 직접 생산합니다.":
        "{n} agricultural films for every crop and season, made at our plant in Damyang.",
    "규격·두께·폭은 <a href=\"{L}/spec\">생산제품 규격표</a>에서 한눈에 확인하세요.":
        "See thickness, width and packaging at a glance in the <a href=\"{L}/spec\">specification table</a>.",
    "제품 문의하기": "Ask about a product", "제품 목록": "Products", "이 제품 문의": "Ask about this product",
    "색상": "Colors", "Box 포장": "Box packaging", "가능": "Available", "특징": "Features", "적용 분야": "Applications",
    "생분해 과정": "Biodegradation", "주의사항": "Precautions",
    "규격 외 주문, 유공 간격, 폭·두께 상담은 전화 또는 문의게시판으로 주세요.":
        "For custom sizes, perforation spacing, width or thickness, call us or use the inquiry board.",
    "규격표": "Specifications",

    # 규격표
    "생산제품 규격표": "Product Specifications",
    "생산제품 규격표. LD·HD·흑백·장수·닥트·생분해 필름의 두께, 폭, 유공, 포장 단위.":
        "Product specifications: thickness, width, perforation and packaging for LD, HD, black & white, long-life, duct and biodegradable film.",
    "두께 0.012mm부터, 최대 폭 600cm까지. 표에 없는 규격은 문의해 주세요.":
        "From 0.012 mm thick and up to 600 cm wide. Ask us for sizes not listed.",
    "생산품목": "Product", "두께 (mm)": "Thickness (mm)", "폭 (cm)": "Width (cm)", "유공": "Perforation", "포장": "Packaging",
    "※ '타계 시'는 두 겹으로 접어 생산하는 경우의 폭입니다. 유공(구멍) 간격·배열은 작물에 맞춰 주문 가능합니다.":
        "※ 'Folded' is the width when the film is produced folded in two. Perforation spacing and layout can be ordered to suit the crop.",
    "원하는 규격이 표에 없다면 전화로 바로 상담해 드립니다.": "If the size you need is not listed, call us and we will help right away.",
    "문의 남기기": "Send an inquiry",

    # 인증
    "인증·특허": "Certifications",
    "환경표지 인증, 이노비즈, 벤처기업, 뿌리기업, 소부장 전문기업, SPS 우수단체표준, 연구개발전담부서, 특허 2건.":
        "Korea Eco-Label, Inno-Biz, Venture Business, Root Industry, Materials & Parts Specialist, SPS group standard, dedicated R&D department and two patents.",
    "인증 {c}건, 특허 {p}건. 인증서를 클릭하면 크게 볼 수 있습니다.": "{c} certifications and {p} patents. Click a certificate to enlarge it.",

    # 생산설비
    "담양 무정공단 자체 공장. 블로운 필름 압출 라인에서 두께 0.012mm부터 최대 폭 600cm까지 농업용 필름을 생산합니다.":
        "Our own plant in Damyang produces agricultural film on blown film lines, from 0.012 mm thick and up to 600 cm wide.",
    "담양 무정공단 자체 공장에서 압출부터 권취·포장·출하까지 한 곳에서 이뤄집니다.":
        "Extrusion, winding, packing and shipping all happen under one roof at our Damyang plant.",
    "생산 공정": "Process", "압출 → 권취 → 검수 → 포장 · 출하": "Extrusion → Winding → Inspection → Packing · Shipping",
    "원료 투입 · 블로운 압출": "Resin feed · Blown extrusion", "LD · HD · LLD 수지, 생분해 수지": "LD, HD, LLD and biodegradable resins",
    "냉각 · 권취": "Cooling · Winding", "두께 0.012mm~, 최대 폭 600cm": "From 0.012 mm thick, up to 600 cm wide",
    "유공 · 침공 가공": "Perforation · Micro-perforation", "작물별 구멍 간격 주문 가능": "Hole spacing made to order for each crop",
    "검수 · Box/Roll 포장 · 출하": "Inspection · Box/Roll packing · Shipping", "SPS 우수단체표준 기준": "To SPS group standard",
    "공장 방문 상담을 원하시면 미리 연락 주세요.": "Please contact us in advance if you would like to visit the plant.",

    # 문의게시판
    "제품 구입·견적·규격 문의. 전화 {tel} 또는 문의게시판에 남겨주시면 답변 드립니다.":
        "Purchasing, quotes and specifications. Call {tel} or leave a message on the inquiry board.",
    "제품 구입 · 견적 · 규격 상담. 남겨주신 문의는 확인 후 답변 드립니다.":
        "Purchasing, quotes and specifications. We will reply after reviewing your inquiry.",
    "급하시면 전화로": "Need it fast? Call us", "번호": "No.", "제목": "Subject", "작성자": "Name", "상태": "Status", "날짜": "Date",
    "답변완료": "Answered", "답변대기": "Pending", "첫 문의를 남겨주세요.": "No inquiries yet. Be the first to ask.",
    "비밀글": "Private", "비밀번호를 입력해 주세요": "Enter your password",
    "작성 시 입력한 비밀번호로 열람할 수 있습니다.": "Use the password you set when posting.",
    "← 목록": "← Back to list", "목록": "List", "새 문의": "New inquiry", "{name} 답변": "Reply from {name}",
    "확인 후 답변 드리겠습니다. 급하시면 <a href=\"tel:{tel}\">{tel}</a>로 연락 주세요.":
        "We will reply after reviewing your inquiry. For urgent matters, call <a href=\"tel:{tel}\">{tel}</a>.",
    "연락처를 정확히 남겨주시면 전화 또는 게시판 답변으로 안내해 드립니다.":
        "Leave your contact details and we will reply by phone or on the board.",
    "이름": "Name", "010-0000-0000": "+82-10-0000-0000", "이메일": "Email", "회사 · 농장명": "Company / farm",
    "예: 흑색 LD 멀칭 폭 150cm 견적 문의": "e.g. Quote for black LD mulching film, 150 cm wide",
    "내용": "Message",
    "제품, 두께, 폭, 수량, 유공 여부, 배송 지역을 적어주시면 빠르게 답변 드립니다.":
        "Tell us the product, thickness, width, quantity, perforation and delivery country for a quick reply.",
    "비밀글 (작성자와 관리자만 열람)": "Private (only you and our staff can read it)",
    "비밀번호": "Password", "비밀글 열람용, 4자 이상": "To read it later, 4+ characters",
    "입력하신 개인정보는 문의 답변 용도로만 사용되며, 답변 완료 후 요청 시 삭제해 드립니다.":
        "Your personal information is used only to answer your inquiry and will be deleted on request.",
    "문의 등록": "Submit",
    "이름을 입력해 주세요 (2~20자)": "Please enter your name (2–20 characters).",
    "연락처를 확인해 주세요": "Please check your phone number.",
    "제목을 입력해 주세요 (2~100자)": "Please enter a subject (2–100 characters).",
    "내용을 입력해 주세요 (5~3000자)": "Please enter a message (5–3000 characters).",
    "비밀글 비밀번호는 4자 이상 입력해 주세요": "A private post needs a password of 4 or more characters.",
    "문의가 접수되었습니다. 확인 후 답변 드리겠습니다.": "Your inquiry has been received. We will reply soon.",
    "비밀번호가 맞지 않습니다": "Incorrect password.",
}


def t(s):
    return EN.get(s, s) if g.get("lang") == "en" else s


T = t   # 템플릿용 이름 (_)
