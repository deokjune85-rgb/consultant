import streamlit as st
import plotly.graph_objects as go
import time
import random
import datetime

# ==========================================
# [1. 시스템 설정 및 디자인]
# ==========================================
st.set_page_config(
    page_title="Biz-Finder: 정책자금 AI 솔루션",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 금융/정부기관 느낌의 신뢰감 있는 CSS (블루 & 그레이)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 배경색 */
    .stApp { background-color: #f4f6f9; color: #333; }

    /* 텍스트 강제 검정 (가독성) */
    p, div, span, label, h1, h2, h3, h4, h5, h6, td, th, li {
        color: #1f2937 !important;
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* 헤더 스타일 */
    .dashboard-header {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #1e40af; /* 딥 블루 */
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* 카드 스타일 (진단 결과, 공고 리스트) */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    
    /* 상태 배지 */
    .status-badge-safe {
        background-color: #dcfce7; color: #166534 !important;
        padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;
    }
    .status-badge-danger {
        background-color: #fee2e2; color: #991b1b !important;
        padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background-color: #1e40af !important;
        color: white !important;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #1e3a8a !important;
    }
    
    /* 입력창 스타일 */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #fff !important;
        color: #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 로직 엔진 (Simulated)]
# ==========================================

def analyze_company(data):
    """기업 진단 로직"""
    # 부채비율에 따른 위험도
    debt_score = 100 - (data['debt'] / 10) 
    if debt_score < 0: debt_score = 10
    
    # 기술점수 (가산점)
    tech_score = 60
    if data['lab']: tech_score += 20
    if data['venture']: tech_score += 20
    
    # 종합 점수
    total_score = int((debt_score * 0.4) + (tech_score * 0.6))
    
    return {
        "score": total_score,
        "radar": [tech_score, debt_score, 70, 80, 60], # 기술, 재무, 시장성, 사업성, 팀
        "status": "양호" if total_score >= 70 else "주의 필요"
    }

def match_funds(data):
    """지원사업 매칭 로직 (RAG 시뮬레이션)"""
    funds = []
    
    # 1. 창업기 (~3년)
    if data['year'] <= 3:
        funds.append({
            "title": "2025년 초기창업패키지 (최대 1억)",
            "agency": "창업진흥원",
            "fit": 98,
            "d_day": "D-14",
            "type": "출연금(R&D)"
        })
    
    # 2. 기술 보유 기업
    if data['lab'] or data['venture']:
        funds.append({
            "title": "디딤돌 창업성장 기술개발사업 (1.2억)",
            "agency": "중소벤처기업부",
            "fit": 95,
            "d_day": "D-21",
            "type": "R&D"
        })
        
    # 3. 일반 융자 (부채비율 체크)
    if data['debt'] < 300:
        funds.append({
            "title": "혁신성장지원자금 (시설/운전)",
            "agency": "중소벤처기업진흥공단",
            "fit": 88,
            "d_day": "상시접수",
            "type": "정책융자(Low Interest)"
        })
    else:
        funds.append({
            "title": "⚠️ [경고] 부채비율 과다로 정책자금 융자 제한 예상",
            "agency": "System Alert",
            "fit": 0,
            "d_day": "-",
            "type": "Risk"
        })
        
    return funds

def generate_psst(item_name):
    """사업계획서 PSST 자동 생성"""
    return f"""
    <strong>1. 문제인식 (Problem)</strong><br>
    - 현재 시장의 기존 솔루션은 비효율적이며 비용이 높음.<br>
    - '{item_name}' 관련 데이터의 부재로 인한 소비자 불편 가중.<br><br>
    <strong>2. 실현가능성 (Solution)</strong><br>
    - AI 기반의 자동화 알고리즘을 통해 처리 속도 10배 향상.<br>
    - 독자적인 특허 기술 적용으로 경쟁사 대비 기술적 우위 확보.<br><br>
    <strong>3. 성장전략 (Scale-up)</strong><br>
    - 1차년도: 수도권 타겟 마케팅 및 베타 테스트 완료.<br>
    - 2차년도: 데이터 고도화 및 B2B 솔루션 확장.<br><br>
    <strong>4. 팀 구성 (Team)</strong><br>
    - 관련 분야 10년 이상 경력의 대표자 및 석/박사급 개발진 보유.
    """

# ==========================================
# [3. 사이드바: 클라이언트 관리]
# ==========================================
with st.sidebar:
    st.markdown("### 👥 클라이언트 프로파일링")
    
    c_name = st.text_input("기업명", "아이엠디테크")
    c_year = st.number_input("업력 (년)", 1, 30, 2)
    c_rev = st.number_input("작년 매출액 (억원)", 0.0, 1000.0, 5.0)
    c_debt = st.number_input("부채비율 (%)", 0, 1000, 200)
    
    st.markdown("---")
    st.markdown("**가점 요건 확인**")
    c_lab = st.checkbox("기업부설연구소 보유")
    c_venture = st.checkbox("벤처기업 인증")
    c_pat = st.checkbox("특허 보유 (출원 포함)")
    
    st.markdown("---")
    analyze_btn = st.button("🔍 기업 정밀 진단 실행", use_container_width=True)

# ==========================================
# [4. 메인 대시보드]
# ==========================================
if 'analyzed' not in st.session_state: st.session_state.analyzed = False
if analyze_btn: st.session_state.analyzed = True

st.markdown("""
<div class="dashboard-header">
    <h2 style="margin:0; color:#1e40af;">Biz-Finder Pro: 정책자금 솔루션</h2>
    <p style="margin:5px 0 0 0; color:#666;">AI 기반 기업 진단 및 맞춤형 공고 매칭 시스템</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.analyzed:
    # 데이터 패키징
    client_data = {
        "year": c_year, "debt": c_debt, 
        "lab": c_lab, "venture": c_venture
    }
    
    result = analyze_company(client_data)
    matched_list = match_funds(client_data)
    
    # --- [섹션 1] 기업 진단 결과 (레이더 차트) ---
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### 📊 기업 건강검진 결과")
        st.markdown(f"""
        <div class="info-card" style="text-align:center;">
            <h1 style="font-size:4rem; color:#1e40af; margin:0;">{result['score']}</h1>
            <p style="color:#666;">종합 지원 적합도</p>
            <div style="margin-top:10px;">
                <span class="{'status-badge-safe' if result['score']>=70 else 'status-badge-danger'}">{result['status']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 경고 메시지
        if c_debt > 400:
            st.error("⚠️ [Risk] 부채비율 400% 초과! 정책자금 융자 제한 대상입니다. R&D로 우회 전략이 필요합니다.")
        elif not (c_lab or c_venture):
            st.warning("💡 [Tip] 연구소나 벤처인증이 없습니다. 가점 요건 확보 컨설팅이 시급합니다.")
            
    with col2:
        # 레이더 차트
        categories = ['기술성', '재무건전성', '시장성', '사업성', '가점항목']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=result['radar'],
            theta=categories,
            fill='toself',
            fillcolor='rgba(30, 64, 175, 0.2)',
            line=dict(color='#1e40af'),
            name=c_name
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            margin=dict(t=20, b=20, l=40, r=40),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- [섹션 2] 매칭 공고 & 서류 생성 ---
    st.markdown("### 💰 AI 매칭 공고 및 서류 생성")
    
    for fund in matched_list:
        with st.container():
            # 공고 카드
            st.markdown(f"""
            <div class="info-card">
                <div style="display:flex; justify-content:space-between;">
                    <h4 style="margin:0; color:#1e40af;">{fund['title']}</h4>
                    <span style="color:#dc2626; font-weight:bold;">{fund['d_day']}</span>
                </div>
                <div style="margin:10px 0; font-size:0.9rem; color:#555;">
                    <span style="background:#f3f4f6; padding:3px 8px; border-radius:5px;">{fund['agency']}</span>
                    <span style="background:#f3f4f6; padding:3px 8px; border-radius:5px;">{fund['type']}</span>
                </div>
                <p style="margin:0;">🎯 AI 매칭 적합도: <strong>{fund['fit']}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # 작성기 (Expandable)
            with st.expander(f"📝 '{fund['title']}' 사업계획서 초안 생성하기"):
                item_input = st.text_input("핵심 아이템/기술명", key=f"item_{fund['title']}")
                if st.button("PSST 자동 생성", key=f"btn_{fund['title']}"):
                    if item_input:
                        with st.spinner("정부 표준 양식(PSST)에 맞춰 작성 중..."):
                            time.sleep(2)
                        draft = generate_psst(item_input)
                        st.markdown(f"""
                        <div style="background:#fff; border:1px solid #ccc; padding:15px; border-radius:5px; font-size:0.9rem;">
                            {draft}
                        </div>
                        """, unsafe_allow_html=True)
                        st.success("✅ 초안 생성 완료! 복사해서 한글(HWP) 파일에 붙여넣으세요.")
                    else:
                        st.warning("아이템명을 입력해주세요.")

else:
    st.info("👈 왼쪽 사이드바에서 고객 정보를 입력하고 '진단 실행' 버튼을 눌러주세요.")
