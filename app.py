# =====================================================
# 💰 IMD BIZ-FINDER FINAL (Document UI) — 서류 시뮬레이션 탑재
# =====================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import random

# ---------------------------------------
# 0. [UI/UX] 시스템 설정
# ---------------------------------------
st.set_page_config(
    page_title="IMD BIZ-FINDER PRO",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    /* 기본 블랙 테마 */
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp {
        background-color: #0E1117;
        color: #E5E7EB;
        font-family: 'Noto Sans KR', sans-serif;
    }
    /* 사이드바 */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #10B981;
    }
    /* 메트릭 */
    [data-testid="stMetricValue"] {
        color: #10B981 !important;
        font-family: 'Consolas', monospace;
        font-weight: bold;
        font-size: 36px !important;
    }
    /* 버튼 */
    button[kind="primary"] {
        background-color: #10B981 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border: none;
        transition: all 0.3s ease;
    }
    /* 탭 */
    .stTabs [data-baseweb="tab"] {
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
    
    /* ★★★ [핵심] A4 용지 시뮬레이션 CSS ★★★ */
    .a4-paper {
        background-color: white;
        color: black;
        padding: 40px;
        margin-top: 20px;
        border-radius: 2px;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
        position: relative;
    }
    .doc-header {
        text-align: center;
        border-bottom: 2px solid black;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .doc-title {
        font-size: 24px;
        font-weight: bold;
        margin: 0;
    }
    .doc-sub {
        font-size: 12px;
        color: #555;
    }
    .doc-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        font-size: 14px;
    }
    .doc-table th, .doc-table td {
        border: 1px solid #000;
        padding: 8px;
        text-align: left;
    }
    .doc-table th {
        background-color: #f0f0f0;
        text-align: center;
        font-weight: bold;
    }
    /* 블러 처리 (유료 유도) */
    .blur-content {
        filter: blur(4px);
        user-select: none;
        opacity: 0.6;
    }
    .paywall-overlay {
        position: absolute;
        bottom: 100px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0,0,0,0.8);
        color: white;
        padding: 15px 30px;
        border-radius: 30px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 10;
        text-align: center;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 상태 초기화
# ---------------------------------------
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'psst_generated' not in st.session_state:
    st.session_state.psst_generated = False

# ---------------------------------------
# 1. [사이드바] 입력 패널
# ---------------------------------------
with st.sidebar:
    st.title("💰 BIZ-FINDER")
    st.caption("정책자금 AI 정밀 진단 v2.1")
    st.markdown("---")

    st.markdown("### 1️⃣ 기업 개요 (Basic)")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        biz_type = st.selectbox("업종", ["제조업", "IT/SW", "서비스", "건설", "도소매"])
    with col_s2:
        biz_year = st.number_input("설립연차", 0, 50, 3)

    st.markdown("### 2️⃣ 재무 현황 (Finance)")
    sales = st.number_input("작년 매출액 (억원)", 0.0, 1000.0, 10.0, step=0.1)
    profit = st.number_input("영업이익 (억원)", -50.0, 500.0, 1.0, step=0.1)
    current_loans = st.number_input("현재 정책자금 잔액 (억원)", 0.0, 500.0, 2.0, step=0.1)
    debt_ratio = st.slider("부채비율 (%)", 0, 1000, 250)

    st.markdown("### 3️⃣ 핵심 평가 지표 (Score)")
    employee_count = st.number_input("현재 고용 인원 (명)", 0, 1000, 5)
    employee_growth = st.checkbox("작년 대비 고용 증가 (+1명 이상)")
    ceo_credit = st.slider("대표자 신용점수 (NICE)", 0, 1000, 850)

    st.markdown("---")
    with st.expander("✨ 가점 및 인증 (Bonus)", expanded=False):
        has_lab = st.checkbox("기업부설연구소/전담부서")
        has_patent = st.checkbox("특허 보유 (등록)")
        is_venture = st.checkbox("벤처/이노비즈/메인비즈")
        is_women = st.checkbox("여성기업/청년창업")
    
    st.markdown("---")
    
    if st.button("🚀 AI 정밀 진단 실행", type="primary", use_container_width=True):
        st.session_state.analysis_done = True
        st.session_state.show_spinner = True
        st.session_state.psst_generated = False # 진단 다시 하면 문서도 리셋
    
    if st.button("🔄 초기화 (Reset)"):
        st.session_state.analysis_done = False
        st.session_state.psst_generated = False
        st.experimental_rerun()

# ---------------------------------------
# 2. [엔진] 로직
# ---------------------------------------
def run_simulation(sales, profit, debt, current_loans, credit, employees, emp_growth, tech_score):
    score = 55
    max_limit = sales * 0.4 
    remaining_limit = max(max_limit - current_loans, 0)

    if credit < 600: return 0, 0
    elif credit >= 900: score += 10
    elif credit >= 800: score += 5
    
    if emp_growth: score += 10
    if employees >= 10: score += 5

    if debt > 500: score -= 20
    elif debt > 300: score -= 10
    elif debt < 150: score += 10

    score += (tech_score * 5)
    
    if profit > (sales * 0.1): score += 5
    elif profit < 0: score -= 10

    return min(score, 98), remaining_limit

# ---------------------------------------
# 3. [메인] 결과 대시보드
# ---------------------------------------
st.title("🛡️ IMD Policy Fund Analysis")
st.caption(f"Target: **{biz_type}** | Established: **{biz_year}년차** | Data: **2025.05.20 Live**")
st.markdown("---")

if st.session_state.analysis_done:
    
    # [A. 할리우드 연출]
    if st.session_state.get('show_spinner'):
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
            time.sleep(random.uniform(0.1, 0.2)) 
            status_container.markdown(f"```text\n[SYSTEM] {log}\n```")
            bar.progress(int((i + 1) / len(logs) * 100))
        
        time.sleep(0.3)
        status_container.empty()
        bar.empty()
        st.session_state.show_spinner = False

    # [B. 결과 계산]
    tech_points = sum([has_lab, has_patent, is_venture, is_women])
    final_score, final_limit = run_simulation(sales, profit, debt_ratio, current_loans, ceo_credit, employee_count, employee_growth, tech_points)
    
    if final_score == 0:
        st.error("🚨 [SYSTEM ALERT] 정책자금 신청 불가 등급입니다. (사유: 대표자 신용도 미달 또는 한도 초과)")
        st.stop()

    # [C. 스코어보드]
    c1, c2, c3, c4 = st.columns(4)
    grade = "A+" if final_score >= 90 else "A" if final_score >= 80 else "B+" if final_score >= 70 else "B"
    c1.metric("종합 등급", grade, "Scoring")
    c2.metric("AI 추천 점수", f"{final_score}점", f"+{final_score - 60} vs 업계평균")
    c3.metric("수령 가능 한도", f"{int(final_limit * 10000):,} 만원", "Estimated")
    c4.metric("합격 확률", f"{min(final_score + 5, 95)}%", "Positive")
    
    st.markdown("---")

    # [D. 레이더 차트 & 전략]
    col_chart, col_detail = st.columns([1, 1.2])
    
    with col_chart:
        categories = ['매출성장성', '수익성', '기술성', '안정성(부채)', '정책부합도']
        r_values = [
            min(sales * 5, 90), 
            min(profit * 20 + 50, 90), 
            50 + (tech_points * 20), 
            max(100 - (debt_ratio / 5), 30), 
            60 + (tech_points * 10) + (10 if employee_growth else 0)
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=r_values, theta=categories, fill='toself', name='우리 기업', line_color='#10B981', fillcolor='rgba(16, 185, 129, 0.3)'))
        fig.add_trace(go.Scatterpolar(r=[60, 60, 40, 60, 50], theta=categories, name='업계 평균', line_color='#6B7280', line_dash='dot'))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='#374151'), bgcolor='rgba(0,0,0,0)'),
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
    
    tab1, tab2, tab3 = st.tabs(["💸 운전자금", "🏭 시설자금", "🧪 R&D 과제"])
    
    with tab1:
        st.markdown(f"""
        | 자금명 | 주관기관 | 예상 한도 | 금리 | 적합도 |
        | :--- | :--- | :--- | :--- | :--- |
        | **혁신성장지원자금** | 중진공 | **{min(final_limit, 10)}억** | 2.5%~ | ⭐⭐⭐⭐⭐ |
        | **창업기반지원자금** | 중진공 | **{min(final_limit, 5)}억** | 2.7%~ | ⭐⭐⭐⭐ |
        | **신성장동력보증** | 신용보증기금 | **{min(final_limit, 3)}억** | 보증료 0.2%↓ | ⭐⭐⭐⭐ |
        """)
        
        # 버튼 클릭 시 상태 변경
        if st.button("📄 '혁신성장' 사업계획서(PSST) 초안 생성", key="btn1", type="primary"):
            with st.spinner("사업계획서 구조화 및 AI 작문 중..."):
                time.sleep(2)
            st.session_state.psst_generated = True
    
    # [F. ★★★ 가짜 서류 시뮬레이션 (HTML Injection) ★★★]
    if st.session_state.psst_generated:
        st.markdown("---")
        st.markdown("### 🖨️ 생성된 사업계획서 (미리보기)")
        
        # A4 용지 느낌의 HTML
        # 여기는 '하얀 종이'다.
        a4_html = f"""
        <div class="a4-paper">
            <div class="doc-header">
                <h1 class="doc-title">2025년 중소기업 정책자금 융자신청서</h1>
                <span class="doc-sub">Form ID: 2025-KOSME-LN-01 (혁신성장지원자금)</span>
            </div>
            
            <p><strong>1. 신청 기업 개요</strong></p>
            <table class="doc-table">
                <tr>
                    <th>업체명</th> <td>(주)IMD솔루션</td> <th>대표자</th> <td>김준</td>
                </tr>
                <tr>
                    <th>설립일</th> <td>{2025-biz_year}.01.01</td> <th>업종</th> <td>{biz_type}</td>
                </tr>
                <tr>
                    <th>매출액</th> <td>{sales}억 원</td> <th>상시근로자</th> <td>{employee_count}명</td>
                </tr>
            </table>
            
            <p><strong>2. 자금 소요 계획</strong></p>
            <table class="doc-table">
                <tr>
                    <th>소요 자금</th> <td>운전자금 300,000,000원</td> <th>자금 용도</th> <td>원부자재 구입 및 R&D 인건비</td>
                </tr>
            </table>

            <p><strong>3. 사업 내용 및 기대 효과 (PSST 핵심)</strong></p>
            <p style="font-size:13px; line-height:1.6;">
                <strong>[기술성]</strong> 당사는 AI 기반 빅데이터 분석 엔진을 보유하고 있으며, 특허 {1 if has_patent else 0}건을 등록 완료하였습니다. 
                특히 기업부설연구소를 통해 매년 매출액의 10% 이상을 R&D에 재투자하고 있습니다.<br><br>
                <strong>[사업성]</strong> 현재 시장 규모는 연평균 15% 성장 중이며, 당사는 독자적인 알고리즘을 통해 경쟁사 대비 30% 높은 효율을 달성했습니다. 
                본 자금을 통해 마케팅을 강화할 경우 내년 매출 {sales * 1.5}억 원 달성이 확실시됩니다.
            </p>
            
            <br>
            <p><strong>4. 세부 추진 일정</strong></p>
            <div class="blur-content">
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
                <table class="doc-table">
                    <tr><th>구분</th><th>1분기</th><th>2분기</th><th>3분기</th></tr>
                    <tr><td>R&D</td><td>완료</td><td>테스트</td><td>출시</td></tr>
                </table>
                <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                <p>※ 본 내용은 유료 결제 시 전체 열람이 가능합니다. 전문가의 검토를 거쳐 제출하시기 바랍니다.</p>
            </div>

            <div class="paywall-overlay">
                🔒 PREMIUM REPORT<br>
                <span style="font-size:12px; font-weight:normal;">(유료 버전에서 전체 다운로드 가능)</span>
            </div>
        </div>
        """
        st.markdown(a4_html, unsafe_allow_html=True)

else:
    # 대기 화면
    st.info("👈 왼쪽 사이드바에 기업 정보를 입력하고 **'진단 실행'**을 눌러주세요.")
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
