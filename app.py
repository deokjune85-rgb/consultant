import streamlit as st
import time
import random

# ==========================================
# [1. 시스템 설정 & 카카오 비즈니스 디자인]
# ==========================================
st.set_page_config(
    page_title="Biz-Finder Pro: Profiler",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 디자인: 카카오 비즈니스 스타일 (가독성 최우선)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #ffffff;
    }
    
    /* 텍스트 강제 검정 */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {
        color: #191919 !important;
    }
    
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #f7f7f7 !important;
        border-right: 1px solid #ececec;
    }
    
    /* 입력창 디자인 */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        color: #191919 !important;
        border: 1px solid #dcdcdc;
        border-radius: 4px;
    }

    /* DNA 분석 카드 */
    .dna-card {
        background-color: #f9f9f9;
        border-left: 6px solid #3c1e1e; /* 카카오 브라운 */
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 리스크/기회 박스 */
    .alert-box-risk {
        background-color: #fff5f5;
        border: 1px solid #ffcccc;
        color: #c53030 !important;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
    }
    .alert-box-opp {
        background-color: #f0fff4;
        border: 1px solid #c6f6d5;
        color: #2f855a !important;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
    }

    /* 페르소나 문서 박스 */
    .doc-paper {
        background-color: #fff;
        border: 1px solid #ddd;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 300px;
        font-family: 'Noto Serif KR', serif; /* 명조체 느낌 */
        line-height: 1.8;
        font-size: 1rem;
        border-radius: 4px;
    }

    /* 버튼 스타일 (카카오 옐로우) */
    .stButton > button {
        background-color: #fee500 !important;
        color: #191919 !important;
        font-weight: 800 !important;
        border: none;
        padding: 15px;
        border-radius: 6px;
        width: 100%;
        font-size: 1.1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #fdd835 !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #fee500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 로직 엔진 (Profiler & Ghostwriter)]
# ==========================================

def analyze_dna(text):
    """기업 DNA 및 리스크 분석 로직"""
    dna_type = "일반형"
    risk = []
    opportunity = []
    
    # 키워드 기반 분석 시뮬레이션
    if "돈" in text or "자금" in text or "대출" in text:
        risk.append("현금 유동성 부족 (Cash-flow Warning)")
        dna_type = "기술 중심 흙수저형 (R&D-Rich, Cash-Poor)"
    if "담보" in text or "꽉" in text:
        risk.append("보증 한도 초과 예상 (신보/기보 거절 가능성 높음)")
    
    if "특허" in text or "기술" in text:
        opportunity.append("기술 가산점 확보 가능 (기술평가 우대)")
    if "수출" in text or "글로벌" in text:
        opportunity.append("글로벌 진출 지원사업 적합")
    if "직원" in text or "채용" in text:
        opportunity.append("고용연계형 R&D 가산점 대상")

    if not risk: risk.append("특이 리스크 미발견")
    if not opportunity: opportunity.append("일반적인 사업 구조")
    
    return dna_type, risk, opportunity

def ghostwrite(text, mode):
    """페르소나별 문서 생성 로직"""
    base_content = "귀사의 핵심 기술인 재활용 공정 효율화 기술을 바탕으로..."
    
    if mode == "PSST (정부/심사위원용)":
        return f"""
        <strong>[1. 과제명]</strong><br>
        폐자원 재활용 공정 효율 30% 향상을 위한 AI 기반 자동 분류 시스템 개발<br><br>
        <strong>[2. 문제인식 (Problem)]</strong><br>
        - 기존 수작업 분류 방식의 한계로 인한 생산성 저하 및 인건비 상승<br>
        - 폐기물 처리 비용 증가로 인한 수익성 악화 (영업이익률 5% 미만)<br><br>
        <strong>[3. 해결방안 (Solution)]</strong><br>
        - 딥러닝 비전 인식 기술을 적용한 자동 선별기 도입 (특허출원번호: 10-2024-XXXXX)<br>
        - 공정 자동화를 통해 처리 속도 2.5배 향상 및 불량률 0.1% 미만 달성<br><br>
        <strong>[4. 기대효과 (Effect)]</strong><br>
        - 연간 3억 원의 인건비 절감 및 매출 150% 성장 예상.<br>
        - 탄소 배출 저감을 통한 ESG 경영 실천 및 정부 그린 뉴딜 정책 부합.
        """
    elif mode == "Bank (은행 지점장용)":
        return f"""
        <strong>[여신 심사 참고 자료]</strong><br><br>
        <strong>1. 상환 능력 개요</strong><br>
        - 당사는 전년 대비 매출액 200% 성장을 기록하였으며, 영업이익률 15%를 달성하여 안정적인 현금 흐름을 보유하고 있습니다.<br>
        - 금번 운전 자금 대출 시, 생산 설비 확충을 통해 즉각적인 매출 증대가 확실시되어 1년 내 원금 상환이 가능합니다.<br><br>
        <strong>2. 담보 및 신용</strong><br>
        - 대표자 신용등급 1등급 유지 중이며, 공장 부지에 대한 추가 담보 여력이 존재합니다.<br>
        - 기술보증기금 보증서 발급 예정으로 은행 리스크가 최소화된 우량 차주입니다.
        """
    elif mode == "VC (투자 심사역용)":
        return f"""
        <strong>[Investment Highlight]</strong><br><br>
        <strong>🚀 Next Climate Tech Unicorn</strong><br>
        우리는 연간 50조 원 규모의 글로벌 폐기물 시장을 AI로 혁신하고 있습니다.<br><br>
        <strong>📈 Traction & Scalability</strong><br>
        - MVP 테스트 완료: 처리 속도 3배 검증<br>
        - SOM (수익 시장): 국내 5,000억 원 -> 3년 내 점유율 10% 달성 목표<br>
        - Exit Strategy: 5년 내 IPO 또는 대기업 환경 계열사 M&A 목표<br><br>
        단순한 재활용 회사가 아닙니다. <strong>'폐기물 데이터 플랫폼'</strong>입니다.
        """
    return ""

# ==========================================
# [3. 사이드바]
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Biz-Finder Pro")
    st.markdown("전문 컨설턴트를 위한 AI 파트너")
    st.markdown("---")
    st.button("📂 내 프로젝트 관리")
    st.button("📜 지난 상담 이력")
    st.button("⚙️ 설정 (회사 로고 변경)")
    st.markdown("---")
    st.info("**[Tip]** 상담 중 획득한 키워드를 메모장에 입력하면, AI가 즉시 분석을 시작합니다.")

# ==========================================
# [4. 메인 대시보드]
# ==========================================

# 헤더
st.markdown("""
<div style='padding:20px; background:#fff; border-bottom:3px solid #fee500; margin-bottom:30px;'>
    <h1 style='margin:0; font-size:2.2rem;'>Corporate DNA Profiler</h1>
    <p style='margin:5px 0 0 0; font-size:1.1rem; color:#555;'>기업 성향 분석 및 맞춤형 문서 생성 엔진</p>
</div>
""", unsafe_allow_html=True)

# --- [Step 1] 상담 노트 입력 ---
st.markdown("### 1. 📝 상담 메모 입력 (Raw Data)")
st.markdown("<p style='font-size:0.9rem; color:#666;'>미팅 중 받아 적은 내용을 날것 그대로 입력하세요. AI가 행간을 읽어냅니다.</p>", unsafe_allow_html=True)

col_input, col_dna = st.columns([1, 1])

with col_input:
    raw_text = st.text_area(
        "CEO 인터뷰 내용", 
        height=250, 
        value="사장님이 기술 욕심은 엄청 많음. 이번에 폐플라스틱 재활용하는 기계 특허 냈다고 함. 근데 당장 공장 돌릴 돈이 없어서 허덕임. 담보 대출은 이미 꽉 차서 은행은 힘들 것 같음. 해외 수출도 생각하고 있는데 아직 영어 카탈로그도 없음. 직원은 5명인데 다 엔지니어 출신.",
        help="여기에 상담 내용을 자유롭게 적으세요."
    )
    analyze_btn = st.button("🔍 AI 정밀 분석 실행")

# --- [Step 2] DNA 분석 결과 ---
if analyze_btn:
    with col_dna:
        with st.status("🧠 기업 DNA를 해독 중입니다...", expanded=True) as status:
            time.sleep(0.7)
            st.write("📡 텍스트 마이닝으로 핵심 키워드 추출...")
            time.sleep(0.7)
            st.write("⚖️ 재무/비재무 리스크 팩터 스캐닝...")
            time.sleep(0.5)
            status.update(label="분석 완료!", state="complete", expanded=False)
        
        dna_type, risks, opps = analyze_dna(raw_text)
        
        st.markdown(f"""
        <div class='dna-card'>
            <h3 style='margin:0; color:#3c1e1e;'>🧬 기업 DNA 진단 결과</h3>
            <hr style='border-color:#ddd;'>
            <p style='font-size:1.2rem; font-weight:bold;'>유형: <span style='background:#fee500; padding:2px 8px;'>{dna_type}</span></p>
            <br>
            <div class='alert-box-risk'>
                🚨 [RISK] {risks[0]}<br>
                <span style='font-size:0.8rem; font-weight:normal;'>→ 솔루션: 신용보증기금 대신 '중진공 직접대출' 또는 'R&D 출연금'으로 우회 전략 필요.</span>
            </div>
            <div style='margin-top:10px;'></div>
            <div class='alert-box-opp'>
                💡 [OPPORTUNITY] {', '.join(opps)}<br>
                <span style='font-size:0.8rem; font-weight:normal;'>→ 솔루션: '기술평가 우수기업' 전형으로 가점 공략 가능.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- [Step 3] 페르소나 고스트라이터 (여기가 하이라이트) ---
    st.markdown("---")
    st.markdown("### 2. 🎭 페르소나 고스트라이터 (Persona Ghostwriter)")
    st.markdown("<p style='font-size:0.9rem; color:#666;'>제출처(정부/은행/VC)에 따라 AI가 가장 합격률 높은 톤앤매너로 문서를 다시 씁니다.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["👨‍⚖️ 심사위원용 (PSST)", "🏦 은행 지점장용 (여신)", "🤝 투자 심사역용 (VC)"])

    with tab1:
        st.markdown("#### 📄 정부 과제 사업계획서 (개조식/수치 강조)")
        if st.button("✍️ PSST 초안 생성하기", key="btn_psst"):
            with st.spinner("정부 표준 양식에 맞춰 작성 중..."):
                time.sleep(1.5)
            content = ghostwrite(raw_text, "PSST (정부/심사위원용)")
            st.markdown(f"<div class='doc-paper'>{content}</div>", unsafe_allow_html=True)
            st.success("✅ 복사해서 한글(HWP) 파일에 붙여넣으세요.")

    with tab2:
        st.markdown("#### 📄 여신 심사 상담 자료 (상환능력/안정성 강조)")
        if st.button("✍️ 은행용 요약서 생성하기", key="btn_bank"):
            with st.spinner("보수적인 은행원 관점으로 작성 중..."):
                time.sleep(1.5)
            content = ghostwrite(raw_text, "Bank (은행 지점장용)")
            st.markdown(f"<div class='doc-paper'>{content}</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("#### 📄 투자 유치용 IR (비전/시장성 강조)")
        if st.button("✍️ VC용 IR 스크립트 생성하기", key="btn_vc"):
            with st.spinner("실리콘밸리 스타일로 포장 중..."):
                time.sleep(1.5)
            content = ghostwrite(raw_text, "VC (투자 심사역용)")
            st.markdown(f"<div class='doc-paper'>{content}</div>", unsafe_allow_html=True)

else:
    # 분석 전에는 우측 컬럼 비워두기
    with col_dna:
        st.info("👈 왼쪽 입력창에 상담 메모를 입력하고 [분석 실행]을 눌러주세요.")
