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

# 디자인: 카카오 비즈니스 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #ffffff;
    }

    /* 배경 및 텍스트 강제 설정 */
    [data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
    [data-testid="stHeader"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #f7f7f7 !important; border-right: 1px solid #ececec; }
    
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {
        color: #191919 !important;
    }
    
    /* 입력창 스타일 */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border-color: #dcdcdc !important;
    }
    
    /* 입력창 라벨 */
    .stTextInput label p, .stNumberInput label p, .stSelectbox label p, .stTextArea label p {
        color: #191919 !important;
        font-weight: 600 !important;
    }

    /* 카드 UI */
    .info-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #eee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background-color: #fee500 !important;
        color: #191919 !important;
        font-weight: 800 !important;
        border: none;
        padding: 15px;
        border-radius: 6px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #fdd835 !important;
    }

    /* 탭 스타일 */
    .stTabs [aria-selected="true"] {
        border-bottom-color: #fee500 !important;
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

# 재무 계산 로직 (인자 수정됨: biz_type 제거)
def calculate_consulting(revenue, employee):
    loan_limit = int(revenue * 0.25)
    if loan_limit > 10: loan_limit = 10
    hire_support = int(employee * 0.3 * 0.9)
    tax_save = int(revenue * 0.1 * 0.1)
    total = loan_limit + (hire_support/10) + (tax_save/10)
    return loan_limit, hire_support, tax_save, total

# DNA 프로파일링 로직
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

# PSST 생성기
def get_psst_data(industry, item_name, target, strength):
    return {
        "problem": [
            f"현재 {target} 시장은 아날로그 방식으로 비효율이 발생하고 있음.",
            f"특히 '{item_name}' 관련 데이터 부재로 소비자 불만족 심화.",
            "기존 방식 대비 시간과 비용이 과다하게 소요됨."
        ],
        "solution": [
            f"빅데이터 및 AI 알고리즘을 적용한 '{item_name}' 개발.",
            f"경쟁사 대비 차별점: {strength} 기술 적용으로 속도 200% 향상.",
            f"SaaS 기반 구축으로 {target}의 접근성 확보."
        ],
        "scaleup": [
            "(1차년도) 시제품 개발 및 핵심 특허 출원.",
            f"(2차년도) {industry} 주요 거점 대상 시범 서비스.",
            "(3차년도) 글로벌(동남아/북미) 시장 판로 개척."
        ],
        "team": [
            f"대표자: {industry} 분야 10년 이상 경력.",
            "연구소: AI/SW 개발 전문 인력 구성 완료.",
            f"네트워크: {target} 관련 협회 MOU 체결."
        ]
    }

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

# 세션 상태 초기화
if 'run_analysis' not in st.session_state:
    st.session_state.run_analysis = False

# 헤더
st.markdown("""
<div style='padding:20px; background:#fff; border-bottom:3px solid #fee500; margin-bottom:20px;'>
    <h1 style='margin:0; font-size:2.2rem;'>Biz-Finder Enterprise</h1>
    <p style='margin:5px 0 0 0; font-size:1.1rem; color:#555;'>AI 기반 정책자금/프로파일링 통합 솔루션</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.run_analysis:
    # 1. 재무 계산 (인자 2개로 수정 완료)
    loan, hire, tax, total = calculate_consulting(c_rev, c_emp)
    ref = success_db.get(c_type, success_db["서비스/기타"])
    
    # 2. DNA 분석
    dna_type, risks, opps = analyze_dna(raw_text)

    # --- [Tab 구성] 기능별로 화면 분리 ---
    tab_finance, tab_dna, tab_doc = st.tabs(["💰 자금/재무 진단", "🧬 기업 프로파일링", "📝 PSST 자동 작성"])

    # --- 1. 자금/재무 진단 탭 ---
    with tab_finance:
        st.markdown(f"### 📊 {c_name} 예상 조달 규모: 총 {total:.1f}억원")
        
        k1, k2, k3 = st.columns(3)
        with k1:
            st.info(f"**정책자금(융자)**\n\n# {loan}억원\n(중진공/신보)")
        with k2:
            st.success(f"**고용지원금**\n\n# {hire}천만원\n(청년/특별고용)")
        with k3:
            st.warning(f"**세금 절세**\n\n# {tax}천만원\n(법인세 감면)")
            
        st.markdown("---")
        st.markdown("#### 🏆 동종 업계 성공 사례")
        st.markdown(f"""
        <div class='info-card' style='background-color:#fffae0; border-color:#fee500;'>
            <strong>{ref['case']} 승인 내역</strong><br>
            💰 총 조달: {ref['fund']}<br>
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
            <div class='info-card' style='text-align:center;'>
                <h2 style='color:#3c1e1e !important;'>{dna_type}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col_d2:
            st.markdown("#### ⚠️ 발견된 리스크 & 기회")
            st.error(f"**[RISK]** {risks[0]}")
            st.success(f"**[OPPORTUNITY]** {opps[0]}")
            
        st.markdown("---")
        st.caption(f"분석 근거: 입력하신 상담 메모 '{raw_text[:20]}...'")

    # --- 3. PSST 자동 작성 탭 ---
    with tab_doc:
        st.markdown("### ✍️ 사업계획서(PSST) 초안 생성")
        
        # 추가 입력
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            item_name = st.text_input("아이템명", "AI 기반 물류 시스템")
        with col_p2:
            strength = st.text_input("핵심 강점", "특허 기술 보유")
            
        if st.button("🤖 문서 생성 시작"):
            with st.spinner("정부 표준 양식으로 작성 중..."):
                time.sleep(1.5)
            
            # 데이터 생성
            psst_data = get_psst_data(c_type, item_name, "중소기업", strength)
            
            st.markdown("---")
            st.subheader("1. 문제인식 (Problem)")
            for line in psst_data['problem']:
                st.write(f"- {line}")
                
            st.subheader("2. 실현가능성 (Solution)")
            for line in psst_data['solution']:
                st.write(f"- {line}")
                
            st.subheader("3. 성장전략 (Scale-up)")
            for line in psst_data['scaleup']:
                st.write(f"- {line}")
                
            st.subheader("4. 팀 구성 (Team)")
            for line in psst_data['team']:
                st.write(f"- {line}")
            
            st.markdown("---")
            st.success("✅ 생성이 완료되었습니다. 내용을 복사해서 사용하세요.")

else:
    # 대기 화면
    st.info("👈 왼쪽 사이드바에 정보를 입력하고 [진단 실행] 버튼을 눌러주세요.")
    st.markdown("<div style='text-align:center; margin-top:50px; color:#999;'>Waiting for Data...</div>", unsafe_allow_html=True)
