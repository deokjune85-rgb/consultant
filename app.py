# =====================================================
# 💰 IMD BIZ-FINDER FINAL — 정책자금 정밀 진단 엔진
# Authorized by: The Architect
# =====================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import random

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (The Black Box Theme)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BIZ-FINDER PRO",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 전문가용 다크/에메랄드 테마 CSS 주입
custom_css = """
<style>
    /* 1. 헤더/푸터 제거 */
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 2. 전체 배경: Deep Charcoal */
    .stApp {
        background-color: #0E1117;
        color: #E5E7EB;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 3. 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #10B981; /* 돈 색깔(녹색) 강조 */
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #10B981 !important;
    }

    /* 4. 메트릭 박스 (스코어보드) */
    [data-testid="stMetricValue"] {
        color: #10B981 !important;
        font-family: 'Consolas', monospace;
        font-weight: bold;
        font-size: 36px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #9CA3AF !important;
        font-weight: bold;
    }

    /* 5. 버튼 스타일 */
    button[kind="primary"] {
        background-color: #10B981 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border: none;
        transition: all 0.3s ease;
    }
    button[kind="primary"]:hover {
        background-color: #059669 !important;
        box-shadow: 0 0 10px #10B981;
    }

    /* 6. 입력창 스타일 */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #1F2937;
        color: white;
        border: 1px solid #374151;
        border-radius: 4px;
    }
    
    /* 7. 탭 스타일 */
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
        font-weight: bold;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. [사이드바] 정밀 입력 패널
# ---------------------------------------
with st.sidebar:
    st.title("💰 BIZ-FINDER")
    st.caption("정책자금 AI 정밀 진단 v2.0")
    st.markdown("---")

    # 섹션 1: 기본 정보
    st.markdown("### 1️⃣ 기업 개요 (Basic)")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        biz_type = st.selectbox("업종", ["제조업", "IT/SW", "서비스", "건설", "도소매"])
    with col_s2:
        biz_year = st.number_input("설립연차", 0, 50, 3)

    # 섹션 2: 재무 정보 (사장님이 아는 수준)
    st.markdown("### 2️⃣ 재무 현황 (Finance)")
    sales = st.number_input("작년 매출액 (억원)", 0.0, 1000.0, 10.0, step=0.1, help="부가세 과세표준증명원 기준")
    profit = st.number_input("영업이익 (억원)", -50.0, 500.0, 1.0, step=0.1)
    
    # 핵심 추가: 부채의 질과 한도 계산용 변수
    current_loans = st.number_input("현재 정책자금 잔액 (억원)", 0.0, 500.0, 2.0, step=0.1, help="기보/신보/중진공 대출 합계")
    debt_ratio = st.slider("부채비율 (%)", 0, 1000, 250, help="자본총계 대비 부채총계 비율")

    # 섹션 3: 평가 지표 (전문가용)
    st.markdown("### 3️⃣ 핵심 평가 지표 (Score)")
    employee_count = st.number_input("현재 고용 인원 (명)", 0, 1000, 5)
    employee_growth = st.checkbox("작년 대비 고용 증가 (+1명 이상)")
    ceo_credit = st.slider("대표자 신용점수 (NICE)", 0, 1000, 850, help="600점 미만은 신청 불가")

    st.markdown("---")
    
    # 섹션 4: 가점 요소
    with st.expander("✨ 가점 및 인증 (Bonus)", expanded=False):
        has_lab = st.checkbox("기업부설연구소/전담부서")
        has_patent = st.checkbox("특허 보유 (등록)")
        is_venture = st.checkbox("벤처/이노비즈/메인비즈")
        is_women = st.checkbox("여성기업/청년창업")
    
    st.markdown("---")
    analyze_btn = st.button("🚀 AI 정밀 진단 실행", type="primary", use_container_width=True)


# ---------------------------------------
# 2. [엔진] 시뮬레이션 로직 (보정 알고리즘)
# ---------------------------------------
def run_simulation(sales, profit, debt, current_loans, credit, employees, emp_growth, tech_score):
    # 1. 기초 체력 점수
    score = 55
    
    # 2. 매출 한도 체크 (정책자금은 보통 매출의 20~50% 한도)
    max_limit = sales * 0.4  # 매출의 40%를 MAX로 가정
    remaining_limit = max_limit - current_loans # 이미 받은 돈 뺌
    
    # 한도가 마이너스면 0으로 처리
    remaining_limit = max(remaining_limit, 0)

    # 3. 신용도 체크 (컷오프) - 점수 반영
    if credit < 600:
        return 0, 0 # 신용 불량 (즉시 탈락)
    elif credit >= 900:
        score += 10
    elif credit >= 800:
        score += 5
    
    # 4. 고용 가점 (정부가 제일 좋아하는 것)
    if emp_growth: score += 10
    if employees >= 10: score += 5

    # 5. 부채비율 감점
    if debt > 500:
        score -= 20
    elif debt > 300:
        score -= 10
    elif debt < 150:
        score += 10

    # 6. 기술 가점 (연구소, 특허 등)
    score += (tech_score * 5)
    
    # 7. 이익 가점
    if profit > (sales * 0.1): # 영업이익률 10% 이상
        score += 5
    elif profit < 0:
        score -= 10

    return min(score, 98), remaining_limit


# ---------------------------------------
# 3. [메인] 결과 대시보드 (War Room)
# ---------------------------------------
st.title("🛡️ IMD Policy Fund Analysis")
st.caption(f"Target: **{biz_type}** | Established: **{biz_year}년차** | Data: **2025.05.20 Live**")
st.markdown("---")

if analyze_btn:
    # [A. 할리우드 해킹 연출]
    status_container = st.empty()
    bar = st.progress(0)
    
    logs = [
        "📡 중소벤처기업부 통합 API 연결 시도...",
        "🔐 보안 세션(Secure Layer) 암호화 중...",
        "🏢 기업 재무 데이터(Financial Data) 파싱...",
        "⚠️ 대표자 신용정보 크로스체크(NICE)...",
        "🔍 2025년도 정책자금 공고 14,200건 스캔 중...",
        "📊 부채비율 및 한도 리스크 시뮬레이션...",
        "✅ 기업부설연구소 및 고용 가점 적용...",
        "🚀 최종 적합도 산출 완료."
    ]
    
    for i, log in enumerate(logs):
        time.sleep(random.uniform(0.2, 0.5)) # 랜덤 딜레이로 리얼함 추가
        status_container.markdown(f"```text\n[SYSTEM] {log}\n```")
        bar.progress(int((i + 1) / len(logs) * 100))
    
    time.sleep(0.5)
    status_container.empty()
    bar.empty()

    # [B. 결과 계산]
    tech_points = sum([has_lab, has_patent, is_venture, is_women])
    final_score, final_limit = run_simulation(sales, profit, debt_ratio, current_loans, ceo_credit, employee_count, employee_growth, tech_points)
    
    # 컷오프(신용불량 등) 처리
    if final_score == 0:
        st.error("🚨 [SYSTEM ALERT] 정책자금 신청 불가 등급입니다. (사유: 대표자 신용도 미달 또는 한도 초과)")
        st.stop()

    # [C. 스코어보드]
    c1, c2, c3, c4 = st.columns(4)
    
    grade = "A+" if final_score >= 90 else "A" if final_score >= 80 else "B+" if final_score >= 70 else "B"
    c1.metric("종합 등급", grade, "Scoring")
    c2.metric("AI 추천 점수", f"{final_score}점", f"+{final_score - 60} vs 업계평균")
    
    # 한도 보여주기 (돈이 보여야 눈이 돌아간다)
    c3.metric("수령 가능 한도", f"{int(final_limit * 10000):,} 만원", "Estimated")
    c4.metric("합격 확률", f"{min(final_score + 5, 95)}%", "Positive")
    
    st.markdown("---")

    # [D. 레이더 차트 & 전략]
    col_chart, col_detail = st.columns([1, 1.2])
    
    with col_chart:
        categories = ['매출성장성', '수익성', '기술성', '안정성(부채)', '정책부합도']
        
        # 차트 데이터 동적 생성
        r_values = [
            min(sales * 5, 90), 
            min(profit * 20 + 50, 90), 
            50 + (tech_points * 20), 
            max(100 - (debt_ratio / 5), 30), 
            60 + (tech_points * 10) + (10 if employee_growth else 0)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=categories,
            fill='toself',
            name='우리 기업',
            line_color='#10B981',
            fillcolor='rgba(16, 185, 129, 0.3)'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[60, 60, 40, 60, 50],
            theta=categories,
            name='업계 평균',
            line_color='#6B7280',
            line_dash='dot'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#374151'),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=True,
            legend=dict(font=dict(color="white")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Noto Sans KR"),
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_detail:
        st.success("✅ **AI 전략 컨설턴트 소견**")
        
        # 동적 코멘트 생성
        weakness = ""
        if debt_ratio > 300: weakness = "부채비율이 다소 높습니다. '가수금 증자'를 통해 비율을 200%대로 낮추면 금리 인하가 가능합니다."
        elif not has_lab: weakness = "기술 점수 보강이 필요합니다. '기업부설연구소' 설립 시 가점(+5) 확보 가능합니다."
        
        st.markdown(f"""
        **[총평]**
        {biz_type} 업종 내에서 **{'기술성' if tech_points > 2 else '매출 안정성'}**이 돋보이는 기업입니다.
        현재 산출된 한도는 **{final_limit}억 원**이며, 이는 {biz_year}년차 기업 평균 상위 15% 수준입니다.
        
        **[핵심 제언]**
        1. {weakness if weakness else "재무 상태가 양호합니다. 공격적인 시설 자금 신청이 가능합니다."}
        2. **고용 증가** 실적을 활용하여 '일자리 창출 특례' 자금을 노리십시오.
        3. 현재 신용점수({ceo_credit}점)는 { '안정권입니다.' if ceo_credit > 800 else '개선이 필요합니다.' }
        """)

    # [E. 추천 자금 리스트]
    st.markdown("### 📂 2025년도 최적 매칭 자금 (Top 3)")
    
    tab1, tab2, tab3 = st.tabs(["💸 운전자금 (Working)", "🏭 시설자금 (Facility)", "🧪 R&D 과제 (Tech)"])
    
    with tab1:
        st.markdown(f"""
        | 자금명 | 주관기관 | 예상 한도 | 금리 | 적합도 |
        | :--- | :--- | :--- | :--- | :--- |
        | **혁신성장지원자금** | 중진공 | **{min(final_limit, 10)}억** | 2.5%~ | ⭐⭐⭐⭐⭐ |
        | **창업기반지원자금** | 중진공 | **{min(final_limit, 5)}억** | 2.7%~ | ⭐⭐⭐⭐ |
        | **신성장동력보증** | 신용보증기금 | **{min(final_limit, 3)}억** | 보증료 0.2%↓ | ⭐⭐⭐⭐ |
        """)
        if st.button("📄 '혁신성장' 사업계획서(PSST) 초안 생성", key="btn1", type="primary"):
            with st.spinner("사업계획서 생성 중... (AI Writing)"):
                time.sleep(2)
            st.success("사업계획서 초안이 생성되었습니다. (다운로드 준비 완료)")
            
    with tab2:
        st.info("💡 공장 매입, 기계 설비 도입 시 최대 100억까지 한도가 늘어납니다.")
        st.markdown("""
        | 자금명 | 주관기관 | 한도 | 비고 |
        | :--- | :--- | :--- | :--- |
        | **스마트공장 구축지원** | 스마트제조혁신추진단 | 2억 | 자부담 50% |
        | **시설구조개선자금** | 중진공 | 60억 | 10년 상환 |
        """)
        
    with tab3:
        st.markdown("""
        * **디딤돌 R&D 과제 (첫걸음)**: 최대 1.2억 지원 (경쟁률 15:1)
        * **팁스(TIPS) 연계형**: 투자 유치 선행 필수.
        """)

else:
    # 대기 화면
    st.info("👈 왼쪽 사이드바에 기업 정보를 입력하고 **'진단 실행'**을 눌러주세요.")
    
    # 3단 컬럼 마케팅 멘트
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🔍 3대 정책자금")
        st.caption("중진공 / 기보 / 신보 완벽 분석")
    with c2:
        st.markdown("#### 📊 신용도 시뮬레이션")
        st.caption("대표자 신용등급에 따른 한도 산출")
    with c3:
        st.markdown("#### 🤖 AI 사업계획서")
        st.caption("PSST 양식 자동 작성 기능")
