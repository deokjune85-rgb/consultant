import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd

# ==========================================
# [1. 시스템 설정 & 하이엔드 디자인]
# ==========================================
st.set_page_config(
    page_title="Biz-Finder Enterprise",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 고급 CSS (그림자, 카드, 타이포그래피 강화)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f0f2f5;
        color: #191f28;
    }
    
    /* 사이드바 강제 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e8eb;
    }
    [data-testid="stSidebar"] * {
        color: #333333 !important;
    }

    /* 텍스트 컬러 강제 고정 */
    h1, h2, h3, h4, h5, p, span, div, label {
        color: #191f28 !important;
    }
    
    /* 카드 UI (박스 디자인) */
    .card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e8eb;
        margin-bottom: 20px;
    }
    
    /* KPI 박스 */
    .kpi-metric {
        text-align: center;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #8b95a1 !important;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #3182f6 !important; /* 토스 블루 */
    }
    
    /* 공고 리스트 스타일 */
    .grant-item {
        border-bottom: 1px solid #f1f3f5;
        padding: 16px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .grant-item:last-child { border-bottom: none; }
    
    .badge-dday {
        background-color: #fff1f1;
        color: #e93d3d !important;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* 문서 프리뷰 스타일 (A4 용지 느낌) */
    .document-preview {
        background-color: #ffffff;
        border: 1px solid #d1d6db;
        padding: 40px;
        min-height: 400px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-family: 'Pretendard', serif; /* 명조 느낌 */
        line-height: 1.8;
        font-size: 0.95rem;
    }
    
    /* 버튼 커스텀 */
    .stButton > button {
        background-color: #3182f6 !important;
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1b64da !important;
    }
    
    /* 입력 필드 개선 */
    .stTextInput input, .stNumberInput input {
        background-color: #f9fafb !important;
        border: 1px solid #d1d6db;
        border-radius: 8px;
        color: #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 사이드바: 고객 데이터 입력]
# ==========================================
with st.sidebar:
    st.markdown("### 🏢 클라이언트 정보 입력")
    
    with st.expander("기본 재무 정보", expanded=True):
        c_name = st.text_input("기업명", "아이엠디테크")
        c_sector = st.selectbox("업종", ["IT/소프트웨어", "제조업", "바이오/헬스케어", "서비스/기타"])
        c_year = st.number_input("업력 (년)", 1, 50, 2)
        c_rev = st.number_input("매출액 (억원)", 0.0, 1000.0, 5.0)
    
    with st.expander("재무 건전성 지표", expanded=True):
        c_debt = st.slider("부채비율 (%)", 0, 1000, 200, help="400% 초과 시 융자 제한 가능성 높음")
        c_profit = st.radio("영업이익 상태", ["흑자", "적자 (자본잠식 없음)", "완전 자본잠식"])
        
    with st.expander("가점 및 인증 현황"):
        c_lab = st.checkbox("기업부설연구소 보유")
        c_venture = st.checkbox("벤처/이노비즈 인증")
        c_pat = st.number_input("등록 특허 수", 0, 100, 0)

    st.markdown("---")
    analyze_btn = st.button("🚀 AI 정밀 진단 실행", use_container_width=True)

# ==========================================
# [3. 메인 대시보드 로직]
# ==========================================

# 헤더 영역
st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;'>
    <div>
        <h1 style='margin:0; font-size:2rem; color:#191f28;'>Biz-Finder Pro</h1>
        <p style='margin:5px 0 0 0; color:#6b7684;'>정책자금 컨설턴트 전용 AI 솔루션 v2.1</p>
    </div>
    <div style='text-align:right;'>
        <span style='background:#e5f4ff; color:#3182f6; padding:6px 12px; border-radius:20px; font-weight:bold;'>Professional License</span>
    </div>
</div>
""", unsafe_allow_html=True)

if analyze_btn:
    # 로딩 시뮬레이션 (있어 보이게)
    with st.status("🔍 기업 데이터를 분석 중입니다...", expanded=True) as status:
        st.write("📊 재무제표 및 부채비율 리스크 스캐닝...")
        time.sleep(0.5)
        st.write("📡 3,400개 정부 공고 데이터베이스 대조 중...")
        time.sleep(0.7)
        st.write("⚖️ 업종별 가점 항목 및 지원 적합도 산출 중...")
        time.sleep(0.5)
        status.update(label="분석 완료!", state="complete", expanded=False)
    
    # --- 데이터 처리 (시뮬레이션) ---
    # 점수 계산
    base_score = 60
    if c_year < 3: base_score += 10 # 창업 초기 가점
    if c_lab: base_score += 10
    if c_venture: base_score += 10
    if c_pat > 0: base_score += (c_pat * 5)
    if c_debt > 400: base_score -= 30 # 부채비율 페널티
    
    final_score = min(max(base_score, 0), 100) # 0~100 제한
    
    # 지원 가능 금액 추정
    max_fund = 0.5 if c_rev < 1 else (1 if c_rev < 10 else 3) # 매출액 기반 한도
    if final_score > 80: max_fund *= 1.5

    # --- [대시보드: 상단 KPI] ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""<div class='card kpi-metric'><div class='kpi-label'>종합 진단 점수</div><div class='kpi-value'>{final_score}점</div></div>""", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""<div class='card kpi-metric'><div class='kpi-label'>지원 가능 등급</div><div class='kpi-value'>{'A' if final_score>=80 else ('B' if final_score>=60 else 'C')}등급</div></div>""", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""<div class='card kpi-metric'><div class='kpi-label'>예상 확보 자금</div><div class='kpi-value'>{max_fund}억</div></div>""", unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""<div class='card kpi-metric'><div class='kpi-label'>매칭된 공고</div><div class='kpi-value'>4건</div></div>""", unsafe_allow_html=True)

    # --- [대시보드: 중단 - 레이더 차트 & 리스크 리포트] ---
    col_chart, col_risk = st.columns([1, 1])
    
    with col_chart:
        st.markdown("### 📐 기업 역량 5각 분석")
        with st.container():
            # 레이더 차트
            categories = ['기술성', '시장성', '사업성', '재무건전성', '정책부합도']
            
            # 점수 세분화
            tech = 80 if c_lab or c_pat > 0 else 40
            market = 70
            biz = 75
            finance = 90 if c_debt < 200 else (40 if c_debt > 400 else 60)
            policy = 85 if c_sector == "IT/소프트웨어" or c_sector == "바이오/헬스케어" else 60
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[tech, market, biz, finance, policy],
                theta=categories,
                fill='toself',
                fillcolor='rgba(49, 130, 246, 0.2)',
                line=dict(color='#3182f6', width=2),
                name=c_name
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='#aaa')),
                margin=dict(t=10, b=10, l=40, r=40),
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_risk:
        st.markdown("### 📋 AI 진단 소견서")
        st.markdown(f"""
        <div class='card' style='height: 300px; overflow-y: auto;'>
            <p style='font-weight:bold; color:#1e40af !important;'>[종합 의견]</p>
            <p>{c_name}의 경우, <strong>{c_sector}</strong> 분야의 정책적 가점이 높으나 
            <strong>{'재무건전성' if c_debt > 300 else '기술 인증'}</strong> 보완이 시급합니다.</p>
            <hr style='border-color:#f1f3f5;'>
            
            <p style='font-weight:bold; color:#d97706 !important;'>[⚠️ 발견된 리스크]</p>
            <ul>
                <li>부채비율 <strong>{c_debt}%</strong>: {'위험 수준 (300% 초과). 자본금 증자 필요.' if c_debt > 300 else '안정권입니다.'}</li>
                <li>연구소 보유 여부: {'✅ 보유 (가점 +2점)' if c_lab else '❌ 미보유 (R&D 지원 시 불리)'}</li>
            </ul>
            <hr style='border-color:#f1f3f5;'>
            
            <p style='font-weight:bold; color:#166534 !important;'>[💡 컨설턴트 Action Plan]</p>
            <p>1. {'부채비율 관리 및 가수금 출자전환 유도' if c_debt > 300 else '기업부설연구소 설립 선행 (소요기간 1개월)'}<br>
            2. {'창업패키지보다는 R&D 과제 위주 공략' if c_year > 3 else '초기창업패키지(1억) 최우선 공략'}</p>
        </div>
        """, unsafe_allow_html=True)

    # --- [대시보드: 하단 - 공고 매칭 & 서류 생성] ---
    st.markdown("---")
    st.markdown("### 💰 AI 매칭 공고 및 서류 자동 생성")
    
    col_list, col_gen = st.columns([1, 1.2])
    
    with col_list:
        st.markdown("**📌 추천 공고 리스트 (적합도 순)**")
        
        # 공고 리스트 (HTML로 커스텀)
        matched_funds = [
            {"title": "2025 초기창업패키지", "amt": "최대 1억", "dday": "D-12", "fit": 98, "tag": "출연금"},
            {"title": "창업성장기술개발 디딤돌", "amt": "1.2억", "dday": "D-24", "fit": 92, "tag": "R&D"},
            {"title": "혁신성장지원자금 (운전)", "amt": "대한도", "dday": "상시", "fit": 85, "tag": "융자"},
            {"title": "데이터바우처 지원사업", "amt": "4,500만", "dday": "예정", "fit": 81, "tag": "바우처"}
        ]
        
        for fund in matched_funds:
            st.markdown(f"""
            <div class='card' style='padding: 15px; margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:5px;'>
                    <span style='font-weight:bold; font-size:1.05rem;'>{fund['title']}</span>
                    <span class='badge-dday'>{fund['dday']}</span>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='color:#555; font-size:0.9rem;'>{fund['tag']} | {fund['amt']}</span>
                    <strong style='color:#3182f6;'>적합도 {fund['fit']}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_gen:
        st.markdown("**📝 PSST 사업계획서 초안 생성**")
        
        with st.container():
            st.markdown("""<div class='card'>""", unsafe_allow_html=True)
            
            target_fund = st.selectbox("작성할 공고 선택", [f['title'] for f in matched_funds])
            item_keyword = st.text_input("핵심 아이템 키워드 (예: AI 기반 물류 최적화)", "AI 기반 속옷 사이즈 추천 플랫폼")
            
            if st.button("🤖 AI 초안 작성 시작 (30초 소요)"):
                # 스트리밍 효과 (타이핑 치는 느낌)
                placeholder = st.empty()
                full_text = ""
                
                # 시뮬레이션 텍스트 (PSST 구조)
                simulated_response = f"""
                <strong>[1. 문제인식 (Problem)]</strong><br>
                - 기존 온라인 패션 시장의 반품률은 30% 이상으로, 물류비 손실이 심각함.<br>
                - 소비자들은 각기 다른 브랜드 사이즈 표기법으로 인해 구매 결정에 어려움을 겪음.<br>
                - 이를 해결할 정밀한 비대면 신체 계측 솔루션의 부재.<br><br>
                
                <strong>[2. 실현가능성 (Solution)]</strong><br>
                - 본 과제는 '{item_keyword}' 기술을 적용하여 오차범위 1cm 이내의 계측을 목표로 함.<br>
                - 15만 건의 체형 빅데이터를 RAG(검색증강생성) 기술과 결합하여 환각 없는 추천 구현.<br>
                - 기존 앱 설치 방식이 아닌, 쇼핑몰 웹 임베드(Embed) 방식으로 접근성 100% 확보.<br><br>
                
                <strong>[3. 성장전략 (Scale-up)]</strong><br>
                - (1차년도) 국내 상위 50개 자사몰 대상 SaaS 모델 공급 및 데이터 확보.<br>
                - (2차년도) 확보된 신체 데이터를 기반으로 패션 제조사(Brand)와 데이터 제휴.<br>
                - (3차년도) 글로벌 플랫폼(Shopify 등) 플러그인 출시로 해외 진출.<br><br>
                
                <strong>[4. 팀 구성 (Team)]</strong><br>
                - 대표자: 동종 업계 15년 경력, 000 브랜드 창업 및 매각 경험 보유.<br>
                - 개발팀: AI 석/박사 출신 엔지니어 3인 보유.
                """
                
                # 타이핑 효과 구현
                st.markdown(f"""
                <div class='document-preview'>
                    <h3 style='text-align:center; text-decoration:underline; margin-bottom:20px;'>사업계획서 (PSST) 요약본</h3>
                    <div style='font-family: "Pretendard", sans-serif;'>
                        {simulated_response}
                    </div>
                    <div style='margin-top:30px; text-align:center; color:#888; font-size:0.8rem;'>
                        * 위 내용은 AI가 생성한 초안입니다. 전문가의 검토 후 제출하십시오.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ 생성이 완료되었습니다. 복사하여 사용하십시오.")

            st.markdown("</div>", unsafe_allow_html=True)

else:
    # 초기 화면 (아무것도 안 눌렀을 때)
    st.info("👈 왼쪽 사이드바에 클라이언트 정보를 입력하고 '진단 실행'을 눌러주세요.")
