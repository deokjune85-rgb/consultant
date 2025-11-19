# =====================================================
# 💰 IMD BIZ-FINDER v1.0 — 정책자금 진단 엔진 (Cash Radar)
# =====================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (금융 터미널 스타일)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BIZ-FINDER PRO",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 돈 냄새 나는 '에메랄드 그린' & '다크' 테마
custom_css = """
<style>
    /* 기본 설정 */
    header, footer {visibility: hidden;}
    .stApp {
        background-color: #000000; /* 완전 블랙 */
        color: #E5E7EB;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 사이드바 (입력부) */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #10B981; /* 녹색 라인 강조 */
    }
    
    /* 메트릭 박스 (점수판) */
    [data-testid="stMetricValue"] {
        color: #10B981 !important; /* 돈 색깔 */
        font-family: 'Consolas', monospace;
        font-weight: bold;
    }

    /* 버튼 스타일 */
    button[kind="primary"] {
        background-color: #10B981 !important; /* 녹색 버튼 */
        color: black !important;
        font-weight: 900 !important;
        border: none;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1F2937;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10B981;
        color: black;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. [사이드바] 기업 정보 입력 (현장용)
# ---------------------------------------
with st.sidebar:
    st.title("💰 BIZ-FINDER")
    st.caption("정책자금/R&D 진단 시스템 v1.0")
    st.markdown("---")

    st.subheader("📋 기업 현황 입력")
    
    col1, col2 = st.columns(2)
    with col1:
        biz_type = st.selectbox("업종", ["제조업", "IT/SW", "서비스", "건설", "기타"])
    with col2:
        biz_year = st.number_input("설립연차", 0, 50, 3)
        
    sales = st.number_input("작년 매출액 (억원)", 0.0, 1000.0, 10.0, step=0.5)
    profit = st.number_input("영업이익 (억원)", -50.0, 500.0, 1.0, step=0.1)
    debt_ratio = st.slider("부채비율 (%)", 0, 1000, 250)
    
    st.markdown("---")
    st.subheader("✨ 가점 요소 (Tech)")
    has_lab = st.checkbox("기업부설연구소 보유")
    has_patent = st.checkbox("특허 보유 (등록)")
    is_venture = st.checkbox("벤처기업 인증")
    
    st.markdown("---")
    analyze_btn = st.button("🚀 AI 진단 실행", type="primary", use_container_width=True)

# ---------------------------------------
# 2. [로직] 가짜(Mockup) 진단 엔진
#    (실제로는 여기서 RAG와 연산이 돌아간다)
# ---------------------------------------
def run_simulation(sales, profit, debt, tech_score):
    # 간단한 점수 계산 로직 (Show용)
    base_score = 50
    if sales > 10: base_score += 10
    if profit > 0: base_score += 10
    if debt < 300: base_score += 10
    score = base_score + (tech_score * 5)
    return min(score, 99)

# ---------------------------------------
# 3. [메인] 진단 결과 대시보드
# ---------------------------------------
st.title("🛡️ 기업 정책자금 진단 리포트")
st.markdown(f"**진단 대상:** {biz_type} | **매출:** {sales}억 | **Update:** 2025.05.20")
st.markdown("---")

if analyze_btn:
    with st.spinner("🏢 기업 재무 데이터 분석 중..."):
        time.sleep(1)
    with st.spinner("📜 2025년 정책자금 공고 매칭 중..."):
        time.sleep(1.5)
        
    # 결과 계산 (가라 데이터)
    tech_points = sum([has_lab, has_patent, is_venture])
    final_score = run_simulation(sales, profit, debt_ratio, tech_points)
    max_fund = int(sales * 0.4 * 10000) # 매출의 40%
    
    # --- [섹션 A] 스코어보드 ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("종합 등급", "A-" if final_score > 80 else "B+", "우수")
    c2.metric("AI 추천 점수", f"{final_score}점", f"{final_score - 60}점 상승")
    c3.metric("수령 가능 한도", f"{max_fund:,} 만원", "예상치")
    c4.metric("합격 확률", f"{min(final_score + 10, 95)}%", "긍정적")
    
    st.markdown("---")

    # --- [섹션 B] 시각화 (레이더 차트) ---
    col_chart, col_detail = st.columns([1, 1.5])
    
    with col_chart:
        # Plotly 레이더 차트 (있어 보이는 핵심)
        categories = ['매출성장성', '수익성', '기술성', '안정성(부채)', '정책부합도']
        
        # 입력값에 따른 동적 차트 데이터
        r_values = [
            min(sales * 5, 90), 
            min(profit * 20 + 50, 90), 
            50 + (tech_points * 15), 
            max(100 - (debt_ratio / 5), 40), 
            70 + (tech_points * 5)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=categories,
            fill='toself',
            name='우리 기업',
            line_color='#10B981'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[60, 60, 50, 60, 50],
            theta=categories,
            name='업계 평균',
            line_color='#4B5563',
            line_dash='dot'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_detail:
        st.subheader("💡 AI 컨설턴트 소견")
        st.info(f"""
        **[총평]**: {biz_type} 업종 내에서 **기술성**이 돋보이는 기업입니다. 
        특히 {'부채비율이 안정적' if debt_ratio < 200 else '부채비율이 다소 높으나'}, **매출 규모({sales}억)**를 고려할 때 
        운전자금보다는 **시설자금**이나 **R&D 과제**로 접근하는 것이 승산이 높습니다.
        """)
        
        st.write("**✅ 승리 전략 (Winning Move):**")
        st.markdown(f"""
        1. **연구소 활용:** {'기업부설연구소 가점 활용' if has_lab else '기업부설연구소 즉시 설립 요망 (+5점)'}
        2. **재무 보정:** 가지급금 정리 후 부채비율 {debt_ratio}% -> {max(debt_ratio-50, 100)}%로 조정 시 금리 1.5% 인하 가능.
        3. **타겟 공고:** 중진공 '혁신성장지원자금' + 기보 '벤처인증 보증' 동시 공략.
        """)

    # --- [섹션 C] 매칭 공고 리스트 (RAG 결과 시뮬레이션) ---
    st.markdown("### 📂 2025년도 맞춤형 추천 자금 (Top 3)")
    
    # 탭으로 구분해서 보여줌 (운전 / 시설 / R&D)
    tab1, tab2, tab3 = st.tabs(["💸 운전자금", "🏭 시설자금", "🧪 R&D 과제"])
    
    with tab1:
        st.markdown("""
        | 공고명 | 주관기관 | 한도 | 금리 | 마감일 | 적합도 |
        | :--- | :--- | :--- | :--- | :--- | :--- |
        | **혁신성장지원자금** | 중소벤처기업진흥공단 | 100억 | 2.5%~ | 2025.02.20 | ⭐⭐⭐⭐⭐ |
        | **창업기반지원자금** | 중소벤처기업진흥공단 | 5억 | 2.9%~ | 예산 소진시 | ⭐⭐⭐⭐ |
        """)
        if st.button("📄 '혁신성장' 사업계획서 초안 생성", key="btn1"):
            st.success("사업계획서 초안이 생성되었습니다. (Demo)")
            
    with tab2:
        st.warning("시설 구매 계획서(견적서)가 추가로 필요합니다.")
        st.markdown("""
        | 공고명 | 주관기관 | 한도 | 비고 |
        | :--- | :--- | :--- | :--- |
        | **스마트공장 구축지원** | 스마트제조혁신추진단 | 2억 | 자부담 50% |
        """)
        
    with tab3:
        st.markdown("""
        * **디딤돌 R&D 과제 (첫걸음)**: 최대 1.2억 지원 (경쟁률 15:1)
        * **팁스(TIPS) 연계형**: 투자 유치 선행 필수.
        """)

else:
    # 대기 화면 (유혹 멘트)
    st.info("👈 왼쪽 사이드바에 기업 정보를 입력하고 **'진단 실행'**을 눌러주세요.")
    st.markdown("""
    #### 🔍 무엇을 진단하나요?
    * **중진공/기보/신보** 3대 정책자금 합격 확률
    * **기업 신용등급** 예상 시뮬레이션
    * **R&D 과제** (디딤돌, 팁스 등) 매칭 적합도
    """)
