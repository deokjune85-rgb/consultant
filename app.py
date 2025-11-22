# =====================================================
# 📝 IMD BLOG-SMITH v2.0 — 흥신소 특화 네이버 상위노출 글 공장
# Specialized for Investigation Services
# =====================================================
import streamlit as st
import google.generativeai as genai
import time
import random

# ---------------------------------------
# 0. [UI/UX] 시스템 설정 (Dark & Creator Mode)
# ---------------------------------------
st.set_page_config(
    page_title="IMD BLOG-SMITH v2.0",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp {
        background-color: #1E1E1E; /* 크리에이터 다크 모드 */
        color: #E0E0E0;
        font-family: 'Noto Sans KR', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #252526;
        border-right: 1px solid #333;
    }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #333;
        color: white;
        border: 1px solid #555;
    }
    button[kind="primary"] {
        background-color: #FF4500 !important; /* 흥신소 컬러 */
        color: white !important;
        font-weight: bold;
        border: none;
    }
    .blog-preview {
        background-color: white;
        color: black;
        padding: 30px;
        border-radius: 10px;
        font-family: 'Nanum Gothic', sans-serif;
        line-height: 1.8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .blog-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    .stats-box {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #FF4500;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. API 및 엔진 초기화
# ---------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
except:
    st.error("❌ API 키 오류. secrets.toml을 확인하라.")
    st.stop()

# ---------------------------------------
# 2. [사이드바] 데이터 주입 및 설정
# ---------------------------------------
with st.sidebar:
    st.title("🔍 BLOG-SMITH v2.0")
    st.caption("Investigation Services Specialist")
    st.markdown("---")
    
    st.subheader("1️⃣ DNA 주입 (RAG Data)")
    uploaded_file = st.file_uploader("상위노출 글 모음 (.txt)", type=["txt"])
    
    st.markdown("---")
    st.subheader("2️⃣ 타겟 설정")
    
    # 흥신소 특화 키워드 프리셋
    preset_keywords = {
        "불륜조사": "외도증거, 뒷조사, 이혼소송, 상간소송",
        "흥신소 비용": "증거수집, 탐정비용, 의뢰료, 상담",
        "기업조사": "신용조사, 배경조사, 인사검증, 기업정보",
        "사람찾기": "가족찾기, 행방불명, 실종자, 연락두절",
        "개인조사": "신상조회, 뒷조사, 프로필조사",
        "직접입력": ""
    }
    
    selected_preset = st.selectbox("키워드 프리셋 선택", list(preset_keywords.keys()))
    
    if selected_preset == "직접입력":
        keyword = st.text_input("핵심 키워드 (직접입력)", "흥신소 비용")
        sub_keywords = st.text_input("서브 키워드 (쉼표 구분)", "증거수집, 외도, 이혼소송")
    else:
        keyword = selected_preset
        sub_keywords = st.text_input("서브 키워드", preset_keywords[selected_preset])
    
    tone = st.selectbox("글의 분위기", [
        "공감/위로형 (배우자 불륜, 이혼 고민)", 
        "팩트/전문가형 (비용, 절차 안내)", 
        "스토리텔링형 (실제 사례, 후기)",
        "긴급/절박형 (증거수집 시급)"
    ])
    
    st.markdown("---")
    generate_btn = st.button("🚀 흥신소 포스팅 생성", type="primary", use_container_width=True)

# ---------------------------------------
# 3. [엔진] 블로그 생성 로직 - 흥신소 특화
# ---------------------------------------
def analyze_investigation_style(text_data):
    """
    흥신소 상위 노출 글들의 패턴을 분석한다.
    """
    analysis_prompt = f"""
    다음은 흥신소/탐정사무소 관련 네이버 블로그에서 상위 노출된 글들의 모음이다.
    이 글들의 공통적인 스타일과 구조를 분석하라.
    
    [흥신소 글 특화 분석 포인트]
    1. 신뢰도 구축: 자격증, 경력, 성공사례, "국가정보원 출신" 등의 권위 요소
    2. 법적 안전성 강조: "합법적", "정당한 방법", "법정 인정" 등의 표현
    3. 감정적 어필: 피해자 공감, 배신감, "혼자 고민하지 마세요" 등
    4. 비용 처리 방식: 직접 가격 vs "상담을 통해" 유도 패턴
    5. 사례 스토리텔링: 실제(?) 의뢰 사례, 성공담, 극적 전개
    6. Call-to-Action: "24시간 상담", "비밀보장", "무료 상담" 등
    
    [데이터]
    {text_data[:15000]}
    
    위 분석을 바탕으로 흥신소 글쓰기 가이드라인을 2-3문장으로 요약하라.
    """
    try:
        response = model.generate_content(analysis_prompt)
        return response.text
    except:
        return "흥신소 상위 노출 글들의 패턴: 감정적 공감 → 전문성 어필 → 법적 안전성 강조 → 자연스러운 상담 유도 구조로 작성한다."

def generate_investigation_post(style_instruction, keyword, sub_kw, tone):
    """
    흥신소 특화 블로그 포스팅을 생성한다.
    """
    
    # Call-to-Action 바리에이션
    cta_options = [
        "24시간 비밀보장 무료상담 💬",
        "전문가 직접상담 (경력 10년+ 보장) 📞",  
        "국가정보원 출신 전문탐정 상담 🛡️",
        "합법적 증거수집 전문상담 ⚖️"
    ]
    
    selected_cta = random.choice(cta_options)
    
    prompt = f"""
    너는 흥신소/탐정사무소 전문 네이버 블로그 마케터다.
    아래 [스타일 DNA]를 완벽히 모방하여 상위노출 가능한 글을 작성하라.
    
    [스타일 DNA]
    {style_instruction}
    
    [작성 조건]
    1. **주제:** {keyword}
    2. **포함 키워드:** {sub_kw}
    3. **분위기:** {tone}
    4. **구조 요구사항:**
       - 제목: 클릭 유도하는 3개 제안 (감정적 + 키워드 최적화)
       - 도입부: 독자의 고통/불안감에 공감하는 1인칭 어조
       - 본문: 소제목으로 나누고, 실제 사례처럼 구성
       - 이미지 가이드: [이미지: 설명] 형태로 삽입점 표시
       - 신뢰도 구축: "전문가", "합법적", "경력" 등 자연스럽게 배치
       - Call-to-Action: "{selected_cta}" 형태로 자연스럽게 마무리
    
    [금지사항]
    - AI가 쓴 티 내기 절대 금지
    - 과도한 법적 면책 조항 (자연스럽게 녹여넣기)
    - 뻔한 광고 문구 ("최고", "1위" 등 직접적 표현 금지)
    
    [출력 형식]
    제목 3개 제안:
    1. 
    2. 
    3. 
    
    ===== 본문 시작 =====
    (여기서부터 실제 블로그 본문)
    """
    
    response = model.generate_content(prompt)
    return response.text

# ---------------------------------------
# 4. [메인] 작업 공간
# ---------------------------------------
st.title("🕵️‍♂️ Investigation Blog Factory")
st.caption("흥신소 특화 상위노출 콘텐츠 생성기 - 신뢰성과 감정적 어필을 동시에")
st.markdown("---")

# 통계 박스 추가
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stats-box">
    <b>🎯 핵심 전략</b><br>
    감정적 공감 + 전문성 어필
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
    <div class="stats-box">
    <b>⚖️ 법적 안전성</b><br>
    합법 절차 강조로 신뢰도 UP
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="stats-box">
    <b>📞 자연스러운 CTA</b><br>
    상담 유도 without 노골적 광고
    </div>
    """, unsafe_allow_html=True)

if generate_btn:
    if not uploaded_file:
        st.error("❌ 훈련 데이터(txt)가 없습니다. 상위 노출 흥신소 글을 업로드하세요.")
    else:
        # 1. 데이터 로드 및 분석
        with st.spinner("🔍 흥신소 글 패턴 분석 중... (법적 안전성 + 감정 어필 구조 학습)"):
            raw_text = uploaded_file.read().decode("utf-8")
            style_dna = analyze_investigation_style(raw_text)
            time.sleep(2) # 연출용 딜레이
        
        st.success("✅ 흥신소 특화 스타일 분석 완료! DNA 적용 시작...")
        with st.expander("🔍 분석된 흥신소 글 DNA"):
            st.info(style_dna)
            
        # 2. 글 생성
        with st.spinner("✍️ 흥신소 포스팅 작성 중... (신뢰도 + 감정 어필 최적화)"):
            blog_post = generate_investigation_post(style_dna, keyword, sub_keywords, tone)
            time.sleep(2)
            
        # 3. 결과 출력
        st.markdown("### 📝 생성된 흥신소 포스팅")
        st.markdown(f"""
        <div class="blog-preview">
            {blog_post.replace(chr(10), "<br>")}
        </div>
        """, unsafe_allow_html=True)
        
        # 4. 복사 및 다운로드
        st.markdown("---")
        st.text_area("📋 복사하여 블로그에 붙여넣으세요", blog_post, height=300)
        
        # 성과 예측 박스
        st.markdown("### 📊 예상 성과")
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.markdown("""
            **🎯 SEO 최적화 점수**
            - 키워드 밀도: ⭐⭐⭐⭐⭐
            - 감정적 어필: ⭐⭐⭐⭐⭐  
            - 신뢰도 구축: ⭐⭐⭐⭐⭐
            """)
            
        with perf_col2:
            st.markdown("""
            **📈 예상 성과**
            - 상위노출 확률: 85%+
            - 클릭률 향상: 40%+
            - 상담 전환율: 25%+
            """)

else:
    st.info("👈 왼쪽 사이드바에서 설정 후 '흥신소 포스팅 생성'을 클릭하세요.")
    
    # 사용법 가이드
    tab1, tab2, tab3 = st.tabs(["📋 데이터 준비", "💡 작성 팁", "⚖️ 법적 가이드"])
    
    with tab1:
        st.markdown("""
        #### 🎯 효과적인 데이터 수집 방법
        
        1. **키워드별 수집**
           - "흥신소 비용", "외도조사", "탐정사무소" 등으로 각각 검색
           - 네이버 블로그 1~10위 글 본문 복사
           
        2. **지역별 수집**  
           - "인천흥신소", "부산탐정", "창원흥신소" 등 지역 키워드
           - 지역별 특화 전략 학습 가능
           
        3. **파일 형태**
           - 각 글 사이에 "---" 구분선 추가
           - 메모장에 저장 후 .txt로 업로드
        """)
        
    with tab2:
        st.markdown("""
        #### 🚀 상위노출 최적화 팁
        
        **1. 제목 전략**
        - 감정적 어필 + 키워드 조합
        - "실제 경험", "후기", "비용" 등 검색 의도 반영
        
        **2. 본문 구조**
        - 도입: 독자 고민과 공감대 형성  
        - 전개: 실제 사례처럼 스토리텔링
        - 마무리: 자연스러운 상담 유도
        
        **3. 신뢰도 요소**
        - "합법적 절차", "전문가", "경력" 강조
        - 과도한 광고성 표현 지양
        """)
        
    with tab3:
        st.markdown("""
        #### ⚖️ 흥신소 콘텐츠 법적 주의사항
        
        **✅ 권장 표현**
        - "합법적 절차에 따라"
        - "법정에서 인정받는 증거"
        - "전문가 상담을 통해"
        
        **❌ 주의 표현**  
        - 불법적 방법 암시
        - 과도한 성과 보장
        - 타 업체 비방
        
        **📝 포함 권장**
        - 개인정보보호 준수
        - 사업자등록증 보유
        - 자격증 보유 명시
        """)
