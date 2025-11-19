import streamlit as st
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

    /* 페르소나 문서 박스 (A4 용지 느낌) */
    .doc-paper {
        background-color: #fff;
        border: 1px solid #ddd;
        padding: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 400px;
        font-family: 'Noto Serif KR', serif; /* 명조체 느낌 */
        line-height: 1.8;
        font-size: 1rem;
        border-radius: 2px;
    }
    /* 문서 내부 텍스트 강제 검정 */
    .doc-paper strong, .doc-paper p, .doc-paper div, .doc-paper h3, .doc-paper h4 {
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

def generate_dynamic_psst(industry, item_name, target, strength):
    """PSST 동적 생성 엔진 (문서 스타일 HTML 반환)"""
    
    # 1. Problem (문제인식)
    p_templates = [
        f"현재 {target} 시장은 아날로그 방식의 운영으로 인해 비효율이 발생하고 있음.",
        f"기존 {industry} 분야의 솔루션은 도입 비용이 높아 중소기업 접근이 어려움.",
        f"{target}의 니즈가 세분화되고 있으나, 기존 기술로는 맞춤형 대응이 불가능함."
    ]
    p_detail = f"- 특히 '{item_name}' 관련 데이터의 부재로 인해 {target}의 불만족이 심화됨.<br>- 기존 방식 대비 시간과 비용이 과다하게 소요되어 생산성 저하 야기."

    # 2. Solution (실현가능성)
    s_templates = [
        f"빅데이터 및 AI 알고리즘을 적용한 '{item_name}' 개발을 통해 문제 해결.",
        f"독자적인 특허 기술을 적용하여 기존 대비 성능을 획기적으로 개선한 '{item_name}' 출시.",
        f"SaaS(서비스형 소프트웨어) 기반의 '{item_name}' 구축으로 접근성 및 확장성 확보."
    ]
    s_detail = f"- 경쟁사 대비 차별점: {strength} 기술 적용으로 처리 속도 200% 향상.<br>- MVP 테스트를 통해 {target}의 긍정적 피드백 및 초기 데이터 확보 완료."

    # 3. Scale-up (성장전략)
    sc_plan = f"""
    - <strong>(1차년도: 기반 구축)</strong> {item_name} 시제품 개발 및 핵심 특허 2건 출원.
    - <strong>(2차년도: 시장 진입)</strong> 국내 {industry} 주요 거점 대상 시범 서비스 및 레퍼런스 확보.
    - <strong>(3차년도: 글로벌 확장)</strong> 안정화된 솔루션을 바탕으로 동남아/북미 등 해외 시장 판로 개척.
    """

    # 4. Team (팀 구성)
    t_plan = f"""
    - <strong>대표자:</strong> {industry} 분야 10년 이상 경력 및 관련 특허 보유자.
    - <strong>연구소:</strong> AI/SW 개발 전문 인력 3인 및 마케팅 전담 인력 구성 완료.
    - <strong>네트워크:</strong> {target} 관련 협회 및 유관 기관과의 MOU 체결로 판로 사전 확보.
    """

    # HTML 문서 서식
    psst_html = f"""
    <div style='line-height: 1.8; color: #000000;'>
        <h4 style='color: #1e40af !important; border-bottom: 2px solid #1e40af; padding-bottom: 5px; margin-bottom:10px;'>1. 문제인식 (Problem)</h4>
        <p><strong>□ {target} 시장의 기술적/사회적 애로사항</strong><br>
        ◦ {random.choice(p_templates)}<br>
        {p_detail}</p>
        
        <h4 style='color: #1e40af !important; border-bottom: 2px solid #1e40af; padding-bottom: 5px; margin-top: 25px; margin-bottom:10px;'>2. 실현가능성 (Solution)</h4>
        <p><strong>□ '{item_name}' 개발을 통한 해결 방안</strong><br>
        ◦ {random.choice(s_templates)}<br>
        {s_detail}</p>
        
        <h4 style='color: #1e40af !important; border-bottom: 2px solid #1e40af; padding-bottom: 5px; margin-top: 25px; margin-bottom:10px;'>3. 성장전략 (Scale-up)</h4>
        <p><strong>□ 단계별 사업화 로드맵</strong><br>
        {sc_plan}</p>
        
        <h4 style='color: #1e40af !important; border-bottom: 2px solid #1e40af; padding-bottom: 5px; margin-top: 25px; margin-bottom:10px;'>4. 팀 구성 (Team)</h4>
        <p><strong>□ 과제 수행 역량</strong><br>
        {t_plan}</p>
    </div>
    """
    return psst_html

# ==========================================
# [3. 사이드바: 간편 조회 폼]
# ==========================================
with st.sidebar:
    st.markdown("### 🏢 기업 간편 진단")
    st.markdown("<p style='font-size:0.9rem; color:#555 !important;'>사업자번호만 있으면 1분 안에 한도 조회가 가능합니다.</p>", unsafe_allow_html=True)
    
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
    st.info("**[전문가 Tip]**\n서류 제출 없이 사업자 번호만으로 1차 가한도 확인이 가능합니다.")

# ==========================================
# [4. 메인 대시보드]
# ==========================================

# 헤더
st.markdown("""
<div class='header-box'>
    <h1 style='margin:0; font-size:2.2rem;'>Biz-Finder Enterprise</h1>
    <p style='margin:5px 0 0 0; font-size:1.1rem; color:#555;'>대한민국 1등 정책자금 조달 솔루션</p>
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
        status.update(label="분석 완료!", state="complete", expanded=False)

    # 결과 계산
    result = calculate_consulting(c_type, c_rev, c_emp)
    ref_case = success_db.get(c_type, success_db["서비스/기타"])

    # --- [섹션 1] 핵심 KPI (3-in-1 패키지) ---
    st.markdown("### 💰 예상 자금 조달 및 혜택 규모")
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>총 조달 가능액</div><div class='kpi-value'>{result['total']}</div><div class='kpi-sub'>+ 추가 금리 인하</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>정책자금(융자)</div><div class='kpi-value' style='color:#191f28 !important;'>{result['loan']}</div><div class='kpi-sub'>중진공/신보/기보</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>고용지원금(무상)</div><div class='kpi-value' style='color:#191f28 !important;'>{result['hire']}</div><div class='kpi-sub'>청년/특별고용 장려금</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='info-card kpi-metric'><div class='kpi-title'>예상 세금 절세</div><div class='kpi-value' style='color:#191f28 !important;'>{result['tax']}</div><div class='kpi-sub'>법인세/소득세 감면</div></div>""", unsafe_allow_html=True)

    # --- [섹션 2] 성공 사례 매칭 (Reference) ---
    st.markdown("### 🏆 동종 업계 성공 사례 (Reference)")
    
    st.markdown(f"""
    <div class='success-case'>
        <h3 style='color:#3c1e1e !important; margin-top:0;'>❝ 사장님과 유사한 {ref_case['case']} 승인 사례 ❞</h3>
        <p style='font-size:1.1rem; font-weight:bold; color:#333 !important;'>💰 총 조달 금액: <span style='color:#d97706; font-size:1.3rem;'>{ref_case['fund']}</span> 승인</p>
        <hr style='border-color:#e6d35f;'>
        <ul style='line-height:1.8; color:#333 !important;'>
            <li><strong>[자금 구성]</strong> {ref_case['detail']}</li>
            <li><strong>[성공 키워드]</strong> {ref_case['key']}</li>
        </ul>
        <p style='font-size:0.9rem; color:#555 !important; margin-top:15px;'>※ 매출액 {c_rev}억 규모 기업의 표준 승인 데이터입니다. 컨설팅 시 98.7% 확률로 승인 가능합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [섹션 3] 솔루션 제안 & 서류 생성 (가로 2단 분할) ---
    st.markdown("---")
    col_L, col_R = st.columns([1, 1.2])
    
    with col_L:
        st.markdown("### 📋 기업 성장 솔루션 제안")
        st.markdown(f"""
        <div class='info-card' style='height:500px;'>
            <p style='color:#191919 !important;'><strong>1. 정책자금 (운전/시설)</strong></p>
            <ul style='color:#333 !important;'>
                <li>한국은행 기준금리 연동 저금리 대출 (2~3%대)</li>
                <li>{c_year}년차 기업 특화자금 (창업기반/도약지원) 매칭</li>
            </ul>
            <br>
            <p style='color:#191919 !important;'><strong>2. 기업 인증 (스펙업)</strong></p>
            <ul style='color:#333 !important;'>
                <li>{'벤처기업 인증 진행 (법인세 50% 감면 타겟)' if c_type == 'IT/소프트웨어' or c_type == '제조업' else '이노비즈/메인비즈 인증을 통한 신뢰도 확보'}</li>
                <li>기업부설연구소 설립으로 인건비 세액 공제 (25%)</li>
            </ul>
            <br>
            <p style='color:#191919 !important;'><strong>3. 리스크 관리</strong></p>
            <ul style='color:#333 !important;'>
                <li>부채비율 관리 및 가지급금 정리 솔루션 제공</li>
                <li>대표자 신용등급 관리 (NICE/KCB) 가이드</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_R:
        st.markdown("### 📝 PSST 사업계획서 자동 생성")
        
        with st.container():
            st.markdown("""<div class='info-card'>""", unsafe_allow_html=True)
            
            # 입력 필드 세분화
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                in_industry = st.selectbox("산업 분야", ["IT/플랫폼", "제조/소부장", "바이오/헬스", "콘텐츠/교육"], key="psst_ind")
                in_target = st.text_input("타겟 고객", "중소기업 경영지원팀", key="psst_target")
            with col_in2:
                in_item = st.text_input("아이템 명칭", "AI 기반 정책자금 매칭 솔루션", key="psst_item")
                in_strength = st.text_input("핵심 강점", "RAG 벡터 검색 기술", key="psst_str")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🤖 AI 초안 작성 시작 (PSST)", use_container_width=True):
                # 진짜 생성하는 척 연출
                placeholder = st.empty()
                
                with st.spinner("정부 표준 양식 학습 중..."):
                    time.sleep(1)
                with st.spinner(f"'{in_industry}' 분야 합격 사례 분석 중..."):
                    time.sleep(1)
                with st.spinner("문장 생성 및 윤문 작업 중..."):
                    time.sleep(1)
                
                # 결과 생성
                result_html = generate_dynamic_psst(in_industry, in_item, in_target, in_strength)
                
                # 문서 프리뷰 보여주기 (A4 스타일)
                placeholder.markdown(f"""
                <div class='doc-paper'>
                    <div style='text-align:center; margin-bottom:20px;'>
                        <span style='border:1px solid #333; padding:5px 15px; border-radius:20px; font-size:0.8rem; color:#333 !important;'>2025년도 창업성장기술개발사업</span>
                        <h3 style='margin-top:10px;'>[사업계획서 요약본]</h3>
                    </div>
                    {result_html}
                    <div style='margin-top:30px; text-align:center; color:#999 !important; font-size:0.8rem;'>
                        Powered by IMD Ghostwriter Engine
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ 작성이 완료되었습니다. 아래 버튼을 눌러 복사하세요.")
                
                d1, d2 = st.columns(2)
                with d1: st.button("📄 한글(HWP) 다운로드")
                with d2: st.button("📑 PDF 다운로드")

            st.markdown("</div>", unsafe_allow_html=True)

else:
    # 초기 대기 화면
    st.info("👈 왼쪽 사이드바에 기업 정보를 입력하고 '무료 한도 조회'를 눌러주세요.")
    st.markdown("""
    <div style='text-align:center; margin-top:50px;'>
        <h1 style='color:#ccc !important;'>Ready for Analysis</h1>
        <p style='color:#999 !important;'>데이터를 입력하면 AI가 3,400개 공고를 스캔합니다.</p>
    </div>
    """, unsafe_allow_html=True)
