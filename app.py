import streamlit as st
import plotly.graph_objects as go
import time
import random
import pandas as pd

# ==========================================
# [1. 시스템 설정 & 강제 화이트 모드]
# ==========================================
st.set_page_config(
    page_title="Biz-Finder Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 디자인: 전문가용 다크 모드 워룸 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* [CORE] 절대 다크 모드 베이스 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #0E1117 !important;
        color: #E5E7EB !important;
    }

    /* [배경] 무조건 어둡게 */
    [data-testid="stAppViewContainer"] { background-color: #0E1117 !important; }
    [data-testid="stHeader"] { background-color: #000000 !important; border-bottom: 1px solid #10B981; }
    [data-testid="stSidebar"] { 
        background-color: #1F2937 !important; 
        border-right: 2px solid #3B82F6 !important;
    }
    
    /* [텍스트] 기본은 밝은 회색, 중요한 건 형광색 */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {
        color: #E5E7EB !important;
    }
    
    /* [핵심 데이터] 볼드체 + 형광색 */
    .kpi-value { 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.5rem !important; 
        font-weight: 900 !important; 
        color: #10B981 !important; 
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    
    /* [입력창] 다크 모드 최적화 */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #374151 !important;
        color: #F3F4F6 !important;
        border: 2px solid #6B7280 !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* [사이드바 라벨] */
    .stTextInput label p, .stNumberInput label p, .stSelectbox label p, .stTextArea label p {
        color: #D1D5DB !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }

    /* [카드 UI] 전문가용 스타일 */
    .war-room-card {
        background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #374151;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        position: relative;
    }
    .war-room-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #3B82F6, #10B981);
    }

    /* [버튼] 강력한 CTA 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-family: 'Noto Sans KR', sans-serif !important;
        border: none;
        padding: 18px 30px !important;
        border-radius: 6px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* [문서 스타일] 전문 보고서 느낌 */
    .doc-paper {
        background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        border: 1px solid #374151;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        min-height: 600px;
        font-family: 'Noto Sans KR', sans-serif;
        line-height: 1.8;
        font-size: 1rem;
        color: #E5E7EB;
    }
    .doc-paper h4 {
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: bold;
        color: #10B981 !important;
        border-bottom: 2px solid #10B981;
        padding-bottom: 8px;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .doc-paper h2 {
        color: #3B82F6 !important;
        text-align: center;
        font-weight: 900;
    }

    /* [탭] 프로페셔널 스타일 */
    .stTabs [aria-selected="true"] {
        background-color: #374151 !important;
        border-bottom: 3px solid #10B981 !important;
        color: #10B981 !important;
    }
    .stTabs button {
        color: #9CA3AF !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* [헤더] 워룸 스타일 */
    .war-room-header {
        background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        padding: 30px;
        border: 1px solid #374151;
        border-left: 4px solid #10B981;
        margin-bottom: 30px;
        position: relative;
    }
    .war-room-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 900;
        color: #F3F4F6 !important;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .war-room-header p {
        margin: 8px 0 0 0;
        font-size: 1rem;
        color: #9CA3AF !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .status-indicator {
        position: absolute;
        top: 20px;
        right: 30px;
        color: #10B981 !important;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* [상태 표시등] */
    .api-status {
        background: #059669;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(5, 150, 105, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 10px rgba(5, 150, 105, 0.3); }
        50% { box-shadow: 0 0 20px rgba(5, 150, 105, 0.6); }
        100% { box-shadow: 0 0 10px rgba(5, 150, 105, 0.3); }
    }

    /* [경고/보안 메시지] */
    .security-notice {
        background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 100%);
        color: #FCA5A5;
        padding: 15px;
        border-radius: 6px;
        border-left: 4px solid #DC2626;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 20px;
    }

    /* [결과 카드들] */
    .result-card {
        background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #3B82F6;
    }
    .result-card h4 {
        color: #3B82F6 !important;
        margin-bottom: 10px;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 로직 엔진]
# ==========================================

# 성공 사례 DB
success_db = {
    "IT/소프트웨어": {"case": "SW개발 A사", "fund": "4.3억원", "key": "기업부설연구소"},
    "제조업": {"case": "부품제조 B사", "fund": "5.3억원", "key": "벤처인증"},
    "도소매/유통": {"case": "의류몰 C사", "fund": "7.9억원", "key": "매출성장"},
    "서비스/기타": {"case": "인테리어 D사", "fund": "3.4억원", "key": "신용관리"}
}

def calculate_consulting(revenue, employee):
    loan_limit = int(revenue * 0.25)
    if loan_limit > 10: loan_limit = 10
    hire_support = int(employee * 0.3 * 0.9)
    tax_save = int(revenue * 0.1 * 0.1)
    total = loan_limit + (hire_support/10) + (tax_save/10)
    return loan_limit, hire_support, tax_save, total

def analyze_dna(text):
    dna_type = "안정지향 일반형"
    risk = []
    opportunity = []
    
    if "돈" in text or "자금" in text:
        risk.append("현금 유동성 부족 (Cash-flow Warning)")
        dna_type = "기술 중심 흙수저형 (R&D-Rich, Cash-Poor)"
    if "담보" in text or "대출" in text:
        risk.append("보증 한도 초과 우려 (신보/기보 우회 필요)")
    
    if "특허" in text: opportunity.append("기술평가 우수기업 가점 대상")
    if "수출" in text: opportunity.append("글로벌 진출 지원사업 적합")
    
    if not risk: risk.append("특이 재무 리스크 미발견")
    if not opportunity: opportunity.append("보편적 사업 구조")
    
    return dna_type, risk, opportunity

def generate_real_psst(industry, item_name, target, strength):
    
    problem = f'''<h4>1-1. 개발 동기 및 필요성</h4>
<p><strong>□ {target} 시장의 구조적 비효율과 디지털 전환(DX)의 지체</strong><br>
◦ 현재 {industry} 시장은 노동 집약적이고 아날로그적인 프로세스에 의존하고 있어, 
데이터 누락 및 인적 오류(Human Error)로 인한 연간 손실액이 증가하는 추세임.<br>
◦ 특히, 기존 레거시(Legacy) 시스템은 도입 비용이 높고 유지보수가 어려워, 
자금력이 부족한 중소기업 및 소상공인의 접근이 원천적으로 차단되어 있음.</p>
<p><strong>□ '{item_name}' 도입을 통한 시장 패러다임 전환 시급</strong><br>
◦ 단순한 기능 개선이 아닌, 데이터 기반의 의사결정 구조를 확립하기 위해서는 
'{item_name}'과 같은 혁신적 솔루션 도입이 필수적임.</p>'''

    solution = f'''<h4>2-1. 기술적 차별성 및 독창성</h4>
<p><strong>□ 고도화된 알고리즘 적용을 통한 기술적 해자(Moat) 구축</strong><br>
◦ 경쟁사들이 단순 규칙(Rule-base) 기반의 매칭을 제공하는 것과 달리, 
당사는 비정형 데이터를 벡터화하여 분석하는 고도화된 알고리즘을 적용함.<br>
◦ 핵심 강점인 <strong>'{strength}'</strong> 기술을 통해 데이터 처리 속도를 200% 향상시켰으며, 
이를 통해 실시간 리스크 분석 및 최적화 제안이 가능함.</p>
<h4>2-2. 사업화 실현 방안</h4>
<p><strong>□ SaaS(서비스형 소프트웨어) 모델을 통한 초기 시장 진입</strong><br>
◦ 초기 도입 비용(Capex)을 0원으로 낮추고, 월 구독료(Opex) 모델을 채택하여 
가격 저항성을 최소화하고 <strong>{target}</strong> 고객군을 빠르게 확보함.<br>
◦ 웹/앱 하이브리드 아키텍처를 통해 별도의 설치 없이 즉시 사용 가능한 환경을 제공하여 
사용자 편의성(UX)을 극대화함.</p>'''

    scaleup = f'''<h4>3-1. 사업화 및 성장 전략</h4>
<p><strong>□ 1단계: 거점 확보 (Targeting)</strong><br>
- 수도권 내 {industry} 밀집 지역을 중심으로 테스트베드(Test-bed)를 구축하고, 
베타 서비스를 통해 실증 데이터(Log Data)를 확보하여 알고리즘을 고도화함.<br>
<strong>□ 2단계: 글로벌 진출 (Global)</strong><br>
- 3차년도부터 동남아/북미 시장의 특성을 반영한 현지화 버전을 출시하고, 
글로벌 클라우드 마켓플레이스(AWS, Azure)에 입점하여 해외 매출 비중을 30%까지 확대함.</p>'''

    team = f'''<h4>4-1. 대표자 및 핵심 인력 역량</h4>
<p><strong>□ 해당 분야 10년 이상의 업력과 노하우 보유</strong><br>
◦ 대표자는 {industry} 분야에서 실무 및 창업 경험을 보유하고 있으며, 
시장 니즈에 대한 명확한 이해를 바탕으로 비즈니스 모델을 설계함.<br>
◦ CTO는 AI 석사 학위 소지자로 대기업 프로젝트 리딩 경험을 보유하여 
안정적인 시스템 개발 및 유지보수가 가능함.</p>
<p><strong>□ 고용 창출 및 조직 관리 계획</strong><br>
◦ 본 과제 수행을 통해 청년 개발자 및 마케터 3명을 신규 채용하여 
정부의 일자리 창출 정책에 기여하고, 수평적 조직 문화를 확립할 계획임.</p>'''
    
    return {"problem": problem, "solution": solution, "scaleup": scaleup, "team": team}

def ghostwrite_bank_vc(text, mode):
    if mode == "Bank (은행 지점장용)":
        return """
        <h4>여신 심사 참고 자료</h4>
        <p><strong>1. 상환 능력 개요</strong><br>
        - 당사는 전년 대비 매출액 200% 성장을 기록하였으며, 영업이익률 15%를 달성하여 안정적인 현금 흐름을 보유하고 있습니다.<br>
        - 금번 운전 자금 대출 시, 생산 설비 확충을 통해 즉각적인 매출 증대가 확실시되어 1년 내 원금 상환이 가능합니다.</p>
        <p><strong>2. 담보 및 신용</strong><br>
        - 대표자 신용등급 1등급 유지 중이며, 공장 부지에 대한 추가 담보 여력이 존재합니다.</p>
        """
    elif mode == "VC (투자 심사역용)":
        return """
        <h4>Investment Highlight</h4>
        <p><strong>🚀 Next Climate Tech Unicorn</strong><br>
        우리는 연간 50조 원 규모의 글로벌 폐기물 시장을 AI로 혁신하고 있습니다.</p>
        <p><strong>📈 Traction & Scalability</strong><br>
        - MVP 테스트 완료: 처리 속도 3배 검증<br>
        - SOM (수익 시장): 국내 5,000억 원 -> 3년 내 점유율 10% 달성 목표</p>
        """
    return ""

# ==========================================
# [3. 사이드바: 컨트롤러]
# ==========================================
with st.sidebar:
    # API 상태등
    st.markdown('<div class="api-status">🟢 SYSTEM ONLINE</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 보안 경고
    st.markdown("""
    <div class="security-notice">
        ⚠️ AUTHORIZED PERSONNEL ONLY<br>
        CONFIDENTIAL BUSINESS INTELLIGENCE
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 TARGET MODULE")
    
    tab_basic, tab_memo = st.tabs(["DATA INPUT", "INTEL NOTES"])
    
    with tab_basic:
        c_name = st.text_input("COMPANY ID", "미래테크")
        c_type = st.selectbox("SECTOR", ["IT/소프트웨어", "제조업", "도소매/유통", "서비스/기타"])
        c_rev = st.number_input("REVENUE (억)", 1.0, 1000.0, 10.0)
        c_emp = st.number_input("HEADCOUNT", 1, 500, 5)
        
    with tab_memo:
        raw_text = st.text_area(
            "FIELD INTEL", 
            height=200,
            value="사장님이 기술 욕심은 많음. 특허도 하나 있음. 근데 당장 현금이 없어서 담보 대출은 꽉 찼다고 함. 수출도 하고 싶어 함.",
            help="Field intelligence for profile analysis"
        )
        
    st.markdown("---")
    if st.button("🚀 EXECUTE ANALYSIS"):
        st.session_state.run_analysis = True
    
    st.markdown("---")
    if st.button("🔴 EMERGENCY RESET"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# [4. 메인 대시보드]
# ==========================================

# 헤더: 워룸 스타일
st.markdown("""
<div class='war-room-header'>
    <div class='status-indicator'>🛡️ CLASSIFIED</div>
    <h1>ACTIVATED: BIZ-FINDER PROTOCOL</h1>
    <p>AI-POWERED BUSINESS INTELLIGENCE SYSTEM</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'run_analysis' not in st.session_state:
    st.session_state.run_analysis = False

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
        st.markdown(f"### 💰 {c_name} FUNDING ANALYSIS")
        st.markdown(f"#### 🎯 TOTAL PROJECTION: {total:.1f}억원")
        
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"""
            <div class='war-room-card'>
                <div style='text-align:center;'>
                    <div style='color:#6B7280; font-size:0.9rem; font-weight:600; margin-bottom:10px;'>POLICY LOAN</div>
                    <div class='kpi-value'>{loan}억원</div>
                    <div style='color:#9CA3AF; font-size:0.8rem; margin-top:5px;'>중진공/신보</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class='war-room-card'>
                <div style='text-align:center;'>
                    <div style='color:#6B7280; font-size:0.9rem; font-weight:600; margin-bottom:10px;'>EMPLOYMENT GRANT</div>
                    <div class='kpi-value'>{hire}천만원</div>
                    <div style='color:#9CA3AF; font-size:0.8rem; margin-top:5px;'>청년/특별고용</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class='war-room-card'>
                <div style='text-align:center;'>
                    <div style='color:#6B7280; font-size:0.9rem; font-weight:600; margin-bottom:10px;'>TAX SAVINGS</div>
                    <div class='kpi-value'>{tax}천만원</div>
                    <div style='color:#9CA3AF; font-size:0.8rem; margin-top:5px;'>법인세 감면</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown("#### 🏆 SUCCESS CASE REFERENCE")
        st.markdown(f"""
        <div class='war-room-card'>
            <strong>📋 {ref['case']} APPROVED CASE</strong><br>
            💰 Total Funding: <span style='color:#10B981; font-weight:bold; font-family:JetBrains Mono;'>{ref['fund']}</span><br>
            🔑 Success Factor: {ref['key']}
        </div>
        """, unsafe_allow_html=True)

    # --- 2. 기업 프로파일링 탭 ---
    with tab_dna:
        st.markdown("### 🧬 CORPORATE DNA ANALYSIS")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("#### 💾 PROFILE TYPE")
            st.markdown(f"""
            <div class='war-room-card' style='text-align:center;'>
                <h2 style='color:#10B981 !important; margin:0; font-family:JetBrains Mono;'>{dna_type}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col_d2:
            st.markdown("#### ⚠️ RISK & OPPORTUNITY MATRIX")
            st.markdown(f"""
            <div class='war-room-card'>
                <div style='color:#EF4444; margin-bottom:15px;'>🚨 <strong>RISK DETECTED</strong><br>{risks[0]}</div>
                <div style='color:#10B981;'>💡 <strong>OPPORTUNITY IDENTIFIED</strong><br>{opps[0]}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.caption(f"📊 Analysis Source: '{raw_text[:20]}...'")

    # --- 3. PSST 자동 작성 탭 ---
    with tab_doc:
        st.markdown("### ✍️ 사업계획서(PSST) 초안 생성")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            item_name = st.text_input("아이템명", "AI 기반 물류 시스템")
            in_industry = st.selectbox("산업 분야", ["IT/플랫폼", "제조/소부장", "바이오/헬스", "콘텐츠/교육"], key="psst_ind")
        with col_p2:
            target_cust = st.text_input("타겟 고객", "중소기업 경영지원팀")
            strength = st.text_input("핵심 강점", "특허 기술 보유")
            
        if st.button("🤖 정밀 사업계획서 생성 (High-Fidelity)"):
            with st.status("💾 ADVANCED AI PROCESSING...", expanded=True) as status:
                st.write("🔍 DATABASE SCANNING...")
                time.sleep(0.3)
                st.write("🧠 PATTERN ANALYSIS...")
                time.sleep(0.3)
                st.write("📊 FINANCIAL MODELING...")
                time.sleep(0.3)
                st.write("✅ DOCUMENT GENERATION COMPLETE")
                status.update(label="🛡️ CLASSIFIED DOCUMENT READY", state="complete", expanded=False)
            
            psst_data = generate_real_psst(in_industry, item_name, target_cust, strength)
            
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
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1: st.button("📋 텍스트 복사")
            with c2: st.button("💾 파일 다운로드")

else:
    # 대기 화면: 워룸 스타일
    st.markdown("""
    <div class='war-room-card' style='text-align:center; padding:60px;'>
        <h2 style='color:#6B7280; margin-bottom:20px;'>⏳ SYSTEM STANDBY</h2>
        <p style='color:#9CA3AF; font-size:1.2rem;'>Configure parameters in CONTROLLER panel</p>
        <p style='color:#6B7280; font-size:0.9rem; margin-top:30px;'>👈 Input data and execute analysis</p>
    </div>
    """, unsafe_allow_html=True)
