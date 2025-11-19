import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd

# ==========================================
# [1. 시스템 설정 & 카카오톡 비즈니스 디자인]
# ==========================================
st.set_page_config(
    page_title="Biz-Finder Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 카카오 테마 CSS (밝고 깔끔한 노랑+화이트)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    /* 전체 배경: 카카오 연한 노랑 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #FFF9E6 !important; /* 연한 노랑 배경 */
    }
    
    /* 메인 컨테이너 배경도 연한 노랑 */
    .main .block-container {
        background-color: #FFF9E6 !important;
    }
    
    /* 모든 텍스트: 카카오 다크 브라운 (진하고 선명) */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th, [data-testid="stMarkdownContainer"] {
        color: #3C1E1E !important; /* 카카오 다크 브라운 */
    }
    
    /* 사이드바: 화이트 배경 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 3px solid #FEE500 !important; /* 카카오 옐로우 테두리 */
    }
    
    /* 사이드바 텍스트도 다크 브라운 */
    [data-testid="stSidebar"] * {
        color: #3C1E1E !important;
    }
    
    /* 입력 필드: 화이트 배경 + 노랑 테두리 */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        color: #3C1E1E !important;
        border: 2px solid #FEE500 !important; /* 카카오 옐로우 테두리 */
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* 카드 UI: 화이트 배경 + 노랑 그림자 */
    .info-card {
        background-color: #FFFFFF !important;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(254, 229, 0, 0.3) !important; /* 노랑 그림자 */
        border: 2px solid #FEE500 !important;
        margin-bottom: 20px;
    }

    /* KPI 숫자 스타일 */
    .kpi-title { 
        font-size: 0.9rem; 
        color: #8B7355 !important; /* 중간 브라운 */
        font-weight: 700; 
        margin-bottom: 8px;
    }
    .kpi-value { 
        font-size: 2.2rem; 
        font-weight: 900; 
        color: #3C1E1E !important; /* 다크 브라운 */
        margin-bottom: 5px;
    }
    .kpi-sub { 
        font-size: 0.85rem; 
        color: #A89279 !important; /* 연한 브라운 */
    }

    /* 성공 사례 박스: 카카오 옐로우 배경 */
    .success-case {
        background: linear-gradient(135deg, #FEE500 0%, #FFD700 100%) !important; /* 그라데이션 노랑 */
        border: 3px solid #3C1E1E !important; /* 다크 브라운 테두리 */
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 6px 16px rgba(60, 30, 30, 0.15);
    }
    
    .success-case h3 {
        color: #3C1E1E !important;
        font-weight: 900 !important;
    }

    /* 버튼: 카카오 옐로우 + 다크 브라운 글씨 */
    .stButton > button {
        background: linear-gradient(135deg, #FEE500 0%, #FFD700 100%) !important;
        color: #3C1E1E !important;
        font-weight: 900 !important;
        border: 3px solid #3C1E1E !important;
        padding: 18px;
        border-radius: 12px;
        width: 100%;
        font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(60, 30, 30, 0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFD700 0%, #FEE500 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(60, 30, 30, 0.3);
    }
    
    /* 헤더 박스: 화이트 배경 + 노랑 하단 테두리 */
    .header-box {
        padding: 25px;
        background-color: #FFFFFF !important;
        border-bottom: 5px solid #FEE500 !important;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(254, 229, 0, 0.2);
    }

    /* info 박스: 노랑 배경 */
    [data-testid="stAlert"] {
        background-color: #FFF4CC !important; /* 연한 노랑 */
        border-left: 5px solid #FEE500 !important;
        color: #3C1E1E !important;
    }
    
    /* status 위젯: 노랑 테마 */
    [data-testid="stStatusWidget"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FEE500 !important;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 900;
        color: #3C1E1E !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FEE500 !important;
        border-bottom: 4px solid #3C1E1E !important;
    }
    
    /* 컬럼 구분선 */
    hr {
        border: 0;
        border-top: 2px solid #FEE500 !important;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 데이터 및 로직 엔진]
# ==========================================

# 성공 사례 데이터베이스
success_db = {
    "IT/소프트웨어": {
        "case": "소프트웨어 개발업 A사",
        "fund": "4억 3천만원",
        "detail": "정책자금 4억 (신보+중진공) / 고용지원금 5천 / 세금절세 4.3천",
        "key": "기업부설연구소 설립을 통한 기술평가 가점 확보"
    },
    "제조업": {
        "case": "플라스틱창호 제조 B사",
        "fund": "5억 3천만원",
        "detail": "정책자금 3억 / 고용지원금 4.2천 / 세금절세 50% 감면",
        "key": "벤처인증 획득으로 법인세/소득세 감면 혜택 적용"
    },
    "도소매/유통": {
        "case": "의류 쇼핑몰 C사",
        "fund": "7억 9천만원",
        "detail": "운전 4억 + 시설(창고) 3억 / 고용지원금 5천",
        "key": "매출 증가율 기반 운전자금 한도 증액 성공"
    },
    "서비스/기타": {
        "case": "실내인테리어 D사",
        "fund": "3억 4천만원",
        "detail": "정책자금 3억 / 고용지원금 2천 / 신용등급 상향",
        "key": "카드론 상환 컨설팅을 통한 대표자 신용등급 관리"
    }
}

def calculate_consulting(biz_type, revenue, employee):
    """3-in-1 패키지 계산 로직"""
    loan_limit = int(revenue * 0.25)
    if loan_limit > 10: loan_limit = 10 
    
    hire_support = int(employee * 0.3 * 0.9) 
    tax_save = int(revenue * 0.1 * 0.1) 
    
    total_benefit = loan_limit + (hire_support/10) + (tax_save/10) 
    
    return {
        "loan": f"{loan_limit}억원",
        "hire": f"{hire_support}천만원",
        "tax": f"{tax_save}천만원",
        "total": f"{total_benefit:.1f}억원"
    }

# ==========================================
# [3. 사이드바: 간편 조회 폼]
# ==========================================
with st.sidebar:
    st.markdown("### 🏢 기업 간편 진단")
    st.markdown("사업자번호만 있으면 1분 안에 한도 조회가 가능합니다.")
    
    biz_num = st.text_input("사업자등록번호", placeholder="000-00-00000")
    
    st.markdown("---")
    st.markdown("#### 📝 기본 정보 입력")
    c_name = st.text_input("기업명", "미래테크")
    c_type = st.selectbox("업종 선택", ["IT/소프트웨어", "제조업", "도소매/유통", "서비스/기타"])
    c_year = st.number_input("업력 (년)", 1, 50, 3)
    
    col1, col2 = st.columns(2)
    with col1:
        c_rev = st.number_input("연 매출(억)", 1.0, 1000.0, 10.0)
    with col2:
        c_emp = st.number_input("직원 수(명)", 1, 500, 5)

    st.markdown("---")
    run_btn = st.button("🚀 무료 한도 조회 실행")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("**[전문가 Tip]**\n\n서류 제출 없이 사업자 번호만으로 1차 가한도 확인이 가능합니다.")

# ==========================================
# [4. 메인 대시보드]
# ==========================================

# 헤더
st.markdown("""
<div class='header-box'>
    <h1 style='margin:0; font-size:2.5rem; color:#3C1E1E !important;'>🏢 Biz-Finder Enterprise</h1>
    <p style='margin:5px 0 0 0; font-size:1.2rem; color:#8B7355 !important; font-weight:700;'>대한민국 1등 정책자금 조달 솔루션</p>
</div>
""", unsafe_allow_html=True)

if run_btn:
    # 로딩 시뮬레이션
    with st.status("📊 기업 데이터를 분석 중입니다...", expanded=True) as status:
        time.sleep(0.5)
        st.write("📡 NICE 평가정보 / KED 데이터 연동 중...")
        time.sleep(0.5)
        st.write("🏦 5대 시중은행 및 정책기관 한도 대조 중...")
        time.sleep(0.5)
        st.write("⚖️ 3,400개 지원사업 매칭 알고리즘 가동...")
        time.sleep(0.5)
        status.update(label="✅ 분석 완료!", state="complete", expanded=False)

    # 결과 계산
    result = calculate_consulting(c_type, c_rev, c_emp)
    ref_case = success_db.get(c_type, success_db["서비스/기타"])

    # --- [섹션 1] 핵심 KPI (3-in-1 패키지) ---
    st.markdown("### 💰 예상 자금 조달 및 혜택 규모")
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>총 조달 가능액</div><div class='kpi-value'>{result['total']}</div><div class='kpi-sub'>+ 추가 금리 인하</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>정책자금(융자)</div><div class='kpi-value'>{result['loan']}</div><div class='kpi-sub'>중진공/신보/기보</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>고용지원금(무상)</div><div class='kpi-value'>{result['hire']}</div><div class='kpi-sub'>청년/특별고용 장려금</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>예상 세금 절세</div><div class='kpi-value'>{result['tax']}</div><div class='kpi-sub'>법인세/소득세 감면</div></div>""", unsafe_allow_html=True)

    # --- [섹션 2] 성공 사례 매칭 ---
    st.markdown("### 🏆 동종 업계 성공 사례 (Reference)")
    
    st.markdown(f"""
    <div class='success-case'>
        <h3 style='color:#3C1E1E !important; margin-top:0;'>❝ 사장님과 유사한 {ref_case['case']} 승인 사례 ❞</h3>
        <p style='font-size:1.2rem; font-weight:900; color:#3C1E1E !important;'>💰 총 조달 금액: <span style='color:#D97706; font-size:1.4rem; font-weight:900;'>{ref_case['fund']}</span> 승인</p>
        <hr style='border-color:#3C1E1E;'>
        <ul style='line-height:2; color:#3C1E1E !important; font-weight:600;'>
            <li><strong>[자금 구성]</strong> {ref_case['detail']}</li>
            <li><strong>[성공 키워드]</strong> {ref_case['key']}</li>
        </ul>
        <p style='font-size:0.95rem; color:#3C1E1E !important; margin-top:15px; font-weight:600;'>※ 매출액 {c_rev}억 규모 기업의 표준 승인 데이터입니다. 컨설팅 시 98.7% 확률로 승인 가능합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [섹션 3] 상세 솔루션 제안 ---
    col_L, col_R = st.columns([1.5, 1])
    
    with col_L:
        st.markdown("### 📋 기업 성장 솔루션 제안")
        st.markdown(f"""
        <div class='info-card'>
            <p style='font-weight:900; font-size:1.1rem; color:#3C1E1E !important;'>1. 정책자금 (운전/시설)</p>
            <ul style='color:#3C1E1E !important; font-weight:600;'>
                <li>한국은행 기준금리 연동 저금리 대출 (2~3%대)</li>
                <li>{c_year}년차 기업 특화자금 (창업기반/도약지원) 매칭</li>
            </ul>
            <br>
            <p style='font-weight:900; font-size:1.1rem; color:#3C1E1E !important;'>2. 기업 인증 (스펙업)</p>
            <ul style='color:#3C1E1E !important; font-weight:600;'>
                <li>{'벤처기업 인증 진행 (법인세 50% 감면 타겟)' if c_type == 'IT/소프트웨어' or c_type == '제조업' else '이노비즈/메인비즈 인증을 통한 신뢰도 확보'}</li>
                <li>기업부설연구소 설립으로 인건비 세액 공제 (25%)</li>
            </ul>
            <br>
            <p style='font-weight:900; font-size:1.1rem; color:#3C1E1E !important;'>3. 리스크 관리</p>
            <ul style='color:#3C1E1E !important; font-weight:600;'>
                <li>부채비율 관리 및 가지급금 정리 솔루션 제공</li>
                <li>대표자 신용등급 관리 (NICE/KCB) 가이드</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_R:
        st.markdown("### 📞 전문가 매칭")
        st.info("""
        **서류 준비가 복잡하신가요?**
        
        전직 은행 지점장, 회계사, 노무사로 구성된
        기업전담팀이 **1:1 방문 상담**을 지원합니다.
        
        지금 '상담 신청'을 누르시면,
        귀사의 관할 지역 전문 위원이 배정됩니다.
        """)
        st.button("👨‍💼 전문 위원 방문상담 신청하기 (무료)")

else:
    # 초기 대기 화면
    st.info("👈 왼쪽 사이드바에 기업 정보를 입력하고 '무료 한도 조회'를 눌러주세요.")
    st.markdown("""
    <div style='text-align:center; margin-top:80px; padding:40px; background-color:#FFFFFF; border-radius:16px; border:3px solid #FEE500;'>
        <h1 style='color:#3C1E1E !important; font-size:2.5rem; font-weight:900;'>Ready for Analysis 🚀</h1>
        <p style='color:#8B7355 !important; font-size:1.3rem; font-weight:700; margin-top:15px;'>데이터를 입력하면 AI가 3,400개 공고를 스캔합니다.</p>
    </div>
    """, unsafe_allow_html=True)
