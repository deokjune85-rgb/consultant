import streamlit as st
import plotly.graph_objects as go
import time
import random
import pandas as pd

# ==========================================
# [1. 시스템 설정 & 강제 화이트 모드 (Nuclear CSS)]
# ==========================================
st.set_page_config(
    page_title="Biz-Finder Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 디자인: 카카오 비즈니스 스타일 (가독성 최우선 + 강제성 부여)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #ffffff;
    }

    /* [핵심 1] 배경 무조건 화이트 (시스템 테마 무시) */
    [data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
    [data-testid="stHeader"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #f7f7f7 !important; border-right: 1px solid #ececec; }
    
    /* [핵심 2] 모든 텍스트 무조건 검정 (예외 없음) */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {
        color: #191919 !important;
    }
    
    /* [핵심 3] 입력창(Input) 강제 스타일링 (배경 흰색, 글자 검정) */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border-color: #dcdcdc !important;
    }
    
    /* 입력창 라벨 텍스트 색상 */
    .stTextInput label p, .stNumberInput label p, .stSelectbox label p, .stTextArea label p {
        color: #191919 !important;
        font-weight: 600 !important;
    }

    /* 카드 UI (정보 박스) */
    .info-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        margin-bottom: 20px;
    }

    /* KPI 숫자 스타일 */
    .kpi-title { font-size: 0.9rem; color: #666 !important; font-weight: 600; }
    .kpi-value { font-size: 2rem; font-weight: 900; color: #3c1e1e !important; } /* 카카오 브라운 */
    .kpi-sub { font-size: 0.8rem; color: #888 !important; }

    /* 성공 사례 박스 */
    .success-case {
        background-color: #fffae0;
        border: 1px solid #fee500;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* DNA 분석 카드 */
    .dna-card {
        background-color: #f9f9f9;
        border-left: 6px solid #3c1e1e;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
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

    /* 페르소나 문서 박스 (A4 용지 느낌) */
    .doc-paper {
        background-color: #fff;
        border: 1px solid #ddd;
        padding: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 600px;
        font-family: 'Noto Serif KR', serif; /* 명조체 느낌 */
        line-height: 1.8;
        font-size: 1rem;
        border-radius: 2px;
    }
    /* 문서 내부 텍스트 강제 검정 */
    .doc-paper strong, .doc-paper p, .doc-paper div, .doc-paper h3, .doc-paper h4, .doc-paper h2 {
        color: #000000 !important;
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
    
    /* 헤더 박스 */
    .header-box {
        padding: 20px;
        background-color: #ffffff;
        border-bottom: 3px solid #fee500;
        margin-bottom: 20px;
    }

    /* 기타 위젯 텍스트 */
    .stAlert div { color: #191919 !important; }
    .streamlit-expanderHeader p { color: #191919 !important; font-weight: 600; }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
        color: #191919 !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #fee500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 데이터 및 로직 엔진]
# ==========================================

# 세션 상태 초기화 (화면 튕김 방지용 핵심 로직)
if 'run_analysis' not in st.session_state:
    st.session_state.run_analysis = False

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

def calculate_consulting(revenue, employee):
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

def analyze_dna(text):
    """DNA 프로파일링 로직"""
    dna_type = "안정지향 일반형"
    risk = []
    opportunity = []
    
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
    if not opportunity: opportunity.append("보편적 사업 구조")
    
    return dna_type, risk, opportunity

def get_real_psst_data(industry, item_name, target, strength):
    """High-Fidelity PSST 생성 엔진"""
    
    # 1. Problem
    problem = f"""
    <div style="margin-bottom: 15px;">
        <h4 style="color:#191919; font-weight:bold; margin-bottom:5px;">1-1. 개발 동기 및 필요성</h4>
        <p><strong>□ {target} 시장의 구조적 비효율과 디지털 전환(DX)의 지체</strong><br>
        ◦ 현재 {industry} 시장은 노동 집약적이고 아날로그적인 프로세스에 의존하고 있어, 
          데이터 누락 및 인적 오류(Human Error)로 인한 연간 손실액이 증가하는 추세임.<br>
        ◦ 특히, 기존 레거시(Legacy) 시스템은 도입 비용이 높고 유지보수가 어려워, 
          자금력이 부족한 중소기업 및 소상공인의 접근이 원천적으로 차단되어 있음.</p>
        <p><strong>□ '{item_name}' 도입을 통한 시장 패러다임 전환 시급</strong><br>
        ◦ 단순한 기능 개선이 아닌, 데이터 기반의 의사결정 구조를 확립하기 위해서는 
          '{item_name}'과 같은 혁신적 솔루션 도입이 필수적임.<br>
        ◦ 글로벌 시장에서는 이미 AI 및 빅데이터를 활용한 최적화가 표준이 되고 있으나, 
          국내 기술 수준은 이에 미치지 못해 기술 종속 및 해외 자본 유출이 우려되는 상황임.</p>
    </div>
    """

    # 2. Solution
    solution = f"""
    <div style="margin-bottom: 15px;">
        <h4 style="color:#191919; font-weight:bold; margin-bottom:5px;">2-1. 기술적 차별성 및 독창성</h4>
        <p><strong>□ 고도화된 알고리즘 적용을 통한 기술적 해자(Moat) 구축</strong><br>
        ◦ 경쟁사들이 단순 규칙(Rule-base) 기반의 매칭을 제공하는 것과 달리, 
          당사는 비정형 데이터를 벡터화하여 분석하는 고도화된 알고리즘을 적용함.<br>
        ◦ 핵심 강점인 <strong>'{strength}'</strong> 기술을 통해 데이터 처리 속도를 200% 향상시켰으며, 
          이를 통해 실시간 리스크 분석 및 최적화 제안이 가능함 (특허 출원 준비 중).</p>
        <h4 style='color:#191919; font-weight:bold; margin-top:10px; margin-bottom:5px;'>2-2. 사업화 실현 방안</h4>
        <p><strong>□ SaaS(서비스형 소프트웨어) 모델을 통한 초기 시장 진입</strong><br>
        ◦ 초기 도입 비용(Capex)을 0원으로 낮추고, 월 구독료(Opex) 모델을 채택하여 
          가격 저항성을 최소화하고 <strong>{target}</strong> 고객군을 빠르게 확보함.<br>
        ◦ 웹/앱 하이브리드 아키텍처를 통해 별도의 설치 없이 즉시 사용 가능한 환경을 제공하여 
          사용자 편의성(UX)을 극대화함.</p>
    </div>
    """

    # 3. Scale-up
    scaleup = f"""
    <div style="margin-bottom: 15px;">
        <h4 style="color:#191919; font-weight:bold; margin-bottom:5px;">3-1. 내수 시장 확보 전략 (Traction)</h4>
        <p><strong>□ 1단계: 거점 확보 (Targeting)</strong><br>
        - 수도권 내 {industry} 밀집 지역을 중심으로 테스트베드(Test-bed)를 구축하고, 
          베타 서비스를 통해 실증 데이터(Log Data)를 확보하여 알고리즘을 고도화함.<br>
        <strong>□ 2단계: 바이럴 및 제휴 (Expansion)</strong><br>
        - 관련 협회 및 커뮤니티와의 MOU를 통해 B2B 판로를 개척하고, 
          성공 사례(Best Practice)를 홍보하여 시장 점유율을 15%까지 확대함.</p>
        <h4 style='color:#191919; font-weight:bold; margin-top:10px; margin-bottom:5px;'>3-2. 글로벌 진출 전략</h4>
        <p><strong>□ K-솔루션의 현지화 (Localization)</strong><br>
        - 3차년도부터 동남아/북미 시장의 특성을 반영한 현지화 버전을 출시하고, 
          글로벌 클라우드 마켓플레이스(AWS, Azure)에 입점하여 해외 매출 비중을 30%까지 확대함.</p>
    </div>
    """

    # 4. Team
    team = f"""
    <div style="margin-bottom: 15px;">
        <h4 style="color:#191919; font-weight:bold; margin-bottom:5px;">4-1. 대표자 및 핵심 인력 역량</h4>
        <p><strong>□ 해당 분야 10년 이상의 업력과 노하우 보유</strong><br>
        ◦ 대표자는 {industry} 분야에서 실무 및 창업 경험을 보유하고 있으며, 
          시장 니즈에 대한 명확한 이해를 바탕으로 비즈니스 모델을 설계함.<br>
        ◦ CTO는 AI 석사 학위 소지자로 대기업 프로젝트 리딩 경험을 보유하여 
          안정적인 시스템 개발 및 유지보수가 가능함.</p>
        <p><strong>□ 고용 창출 및 조직 관리 계획</strong><br>
        ◦ 본 과제 수행을 통해 청년 개발자 및 마케터 3명을 신규 채용하여 
          정부의 일자리 창출 정책에 기여하고, 수평적 조직 문화를 확립할 계획임.</p>
    </div>
    """
    
    return {"problem": problem, "solution": solution, "scaleup": scaleup, "team": team}

# ==========================================
# [3. 사이드바: 입력 폼]
# ==========================================
with st.sidebar:
    st.markdown("### 🏢 기업 정보 입력")
    
    tab_basic, tab_memo = st.tabs(["기본정보", "상담노트"])
    
    with tab_basic:
        c_name = st.text_input("기업명", "미래테크")
        c_type = st.selectbox("업종", ["IT/소프트웨어", "제조업", "도소매/유통", "서비스/기타"])
        c_rev = st.number_input("연 매출(억)", 1.0, 1000.0, 10.0)
        c_emp = st.number_input("직원 수(명)", 1, 500, 5)
        
    with tab_memo:
        raw_text = st.text_area(
            "CEO 인터뷰 메모", 
            height=200,
            value="사장님이 기술 욕심은 많음. 특허도 하나 있음. 근데 당장 현금이 없어서 담보 대출은 꽉 찼다고 함. 수출도 하고 싶어 함.",
            help="상담 내용을 적으면 AI가 성향을 분석합니다."
        )
        
    st.markdown("---")
    # 버튼 클릭 시 상태값 변경 (화면 유지용)
    if st.button("🚀 AI 종합 진단 실행"):
        st.session_state.run_analysis = True

# ==========================================
# [4. 메인 대시보드]
# ==========================================

# 헤더
st.markdown("""
<div class='header-box'>
    <h1 style='margin:0; font-size:2.2rem;'>Biz-Finder Enterprise</h1>
    <p style='margin:5px 0 0 0; font-size:1.1rem; color:#555;'>AI 기반 정책자금/프로파일링 통합 솔루션</p>
</div>
""", unsafe_allow_html=True)

# 결과 화면 렌더링
if st.session_state.run_analysis:
    # 1. 재무 계산
    loan, hire, tax, total = calculate_consulting(c_rev, c_emp)
    ref = success_db.get(c_type, success_db["서비스/기타"])
    
    # 2. DNA 분석
    dna_type, risks, opps = analyze_dna(raw_text)

    # --- [Tab 구성] ---
    tab_finance, tab_dna, tab_doc = st.tabs(["💰 자금/재무 진단", "🧬 기업 프로파일링", "📝 PSST 자동 작성"])

    # --- 1. 자금/재무 진단 탭 ---
    with tab_finance:
        st.markdown(f"### 📊 {c_name} 예상 조달 규모: 총 {total:.1f}억원")
        
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>정책자금(융자)</div><div class='kpi-value'>{loan}억원</div><div class='kpi-sub'>중진공/신보</div></div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>고용지원금</div><div class='kpi-value'>{hire}천만원</div><div class='kpi-sub'>청년/특별고용</div></div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>세금 절세</div><div class='kpi-value'>{tax}천만원</div><div class='kpi-sub'>법인세 감면</div></div>""", unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown("#### 🏆 동종 업계 성공 사례")
        st.markdown(f"""
        <div class='success-case'>
            <strong>{ref['case']} 승인 내역</strong><br>
            💰 총 조달: <span style='color:#d97706; font-weight:bold;'>{ref['fund']}</span><br>
            🔑 성공 키워드: {ref['key']}
        </div>
        """, unsafe_allow_html=True)

    # --- 2. 기업 프로파일링 탭 ---
    with tab_dna:
        st.markdown("### 🧠 상담 노트 기반 AI 분석")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("#### 🧬 기업 DNA 유형")
            st.markdown(f"""
            <div class='dna-card' style='text-align:center;'>
                <h2 style='color:#3c1e1e !important; margin:0;'>{dna_type}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col_d2:
            st.markdown("#### ⚠️ 발견된 리스크 & 기회")
            st.markdown(f"""
            <div class='alert-box-risk'>🚨 [RISK] {risks[0]}</div>
            <div style='margin-top:10px;'></div>
            <div class='alert-box-opp'>💡 [OPPORTUNITY] {opps[0]}</div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.caption(f"분석 근거: 입력하신 상담 메모 '{raw_text[:20]}...'")

    # --- 3. PSST 자동 작성 탭 ---
    with tab_doc:
        st.markdown("### ✍️ 사업계획서(PSST) 초안 생성")
        
        # 추가 입력
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            item_name = st.text_input("아이템명", "AI 기반 물류 시스템")
            in_industry = st.selectbox("산업 분야", ["IT/플랫폼", "제조/소부장", "바이오/헬스", "콘텐츠/교육"], key="psst_ind")
        with col_p2:
            target_cust = st.text_input("타겟 고객", "중소기업 경영지원팀")
            strength = st.text_input("핵심 강점", "특허 기술 보유")
            
        if st.button("🤖 정밀 사업계획서 생성 (High-Fidelity)"):
            # 로딩 연출
            with st.status("📝 전문 컨설턴트 AI가 집필 중입니다...", expanded=True) as status:
                st.write("🔍 산업군별 기술 트렌드 및 경쟁사 약점 분석 중...")
                time.sleep(1)
                st.write("⚖️ 정부 평가 지표(기술성/사업성) 기반 논리 구조화...")
                time.sleep(1)
                st.write("✒️ 관료적 문체(Government Tone)로 문장 윤문 중...")
                time.sleep(1)
                status.update(label="✅ 핵심 요약본 생성 완료!", state="complete", expanded=False)
            
            # 데이터 생성
            psst_data = get_real_psst_data(in_industry, item_name, target_cust, strength)
            
            # 문서 프리뷰 (A4 스타일)
            st.markdown(f"""
            <div class='doc-paper'>
                <div style='text-align:center; border-bottom:2px solid #000; padding-bottom:10px; margin-bottom:30px;'>
                    <h2 style='margin:0; font-family:"Batang", serif;'>2025년도 창업성장기술개발사업 사업계획서</h2>
                    <p style='margin:5px 0 0 0; font-size:0.9rem;'>과제명: {item_name} 개발</p>
                </div>
                
                {psst_data['problem']}
                {psst_data['solution']}
                {psst_data['scaleup']}
                {psst_data['team']}
                
                <div style='margin-top:50px; text-align:center; border-top:1px solid #ddd; padding-top:10px; color:#888; font-size:0.8rem;'>
                    Generated by Biz-Finder Pro | 위 내용은 편집 가능한 초안입니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_copy1, col_copy2 = st.columns(2)
            with col_copy1:
                st.button("📋 전체 텍스트 클립보드 복사")
            with col_copy2:
                st.button("💾 HWP 파일로 변환 및 다운로드")

else:
    # 초기 대기 화면
    st.info("👈 왼쪽 사이드바에 정보를 입력하고 [진단 실행] 버튼을 눌러주세요.")
    st.markdown("""
    <div style='text-align:center; margin-top:50px;'>
        <h1 style='color:#ccc !important;'>Ready for Analysis</h1>
        <p style='color:#999 !important;'>데이터를 입력하면 AI가 3,400개 공고를 스캔합니다.</p>
    </div>
    """, unsafe_allow_html=True)
