import streamlit as st
import base64

# 페이지 설정
st.set_page_config(page_title="Overnight.AI - 발표 자동 채점기", layout="wide")

# 배경 이미지 Base64 인코딩 함수
def get_base64_image(path):
    with open(path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"

bg_url = get_base64_image("image//hackathon.jpg")

# 스타일 추가
st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to bottom right, #14132a, #2a244d, #7a6b96);
        color: white;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 0;
    }}
    .hero-banner {{
        position: relative;
        width: 100%;
        height: 600px;
        background-image: url('{bg_url}');
        background-size: cover;
        background-position: center;
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 3rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
    }}
    .hero-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* 더 투명하게 조정 */
        backdrop-filter: blur(6px); /* ✅ 블러 효과 추가 */
        -webkit-backdrop-filter: blur(6px); /* ✅ 사파리 호환 */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 0 2rem;
    }}
    .hero-overlay h1 {{
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        white-space: nowrap;
    }}
    .hero-overlay p {{
        font-size: 1.2rem;
        max-width: 720px;
        color: #e0e0e0;
        line-height: 1.6;
    }}
    .feature-section {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 0;
        margin: 1rem 0;
    }}
    .feature-card {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        transition: 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        min-height: 320px;
        height: 360px;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.3);
    }}
    .feature-icon img {{
        width: 100px;
        margin-bottom: 1rem;
    }}
    .feature-title {{
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }}
    .feature-desc {{
        font-size: clamp(0.85rem, 1.2vw, 1rem);
        line-height: 1.6;
        color: #f0f0f0;
    }}
    .timeline-step {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        color: white;
    }}
    .timeline-bullet {{
        background: #ff6b81;
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }}
    
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 탭 전체 배경 제거 및 정렬 */
    [data-testid="stTabs"] {
        background-color: transparent;
        color: white;
    }

    /* 선택된 탭 */
    .stTabs [aria-selected="true"] {
        color: white;
        font-weight: bold;
    }

    /* 선택되지 않은 탭 */
    .stTabs [aria-selected="false"] {
        color: #808080;
    }
    </style>
""", unsafe_allow_html=True)

moon_icon = get_base64_image("image//moonnight.png")
evaluation_icon = get_base64_image("image//evaluation.png")    
fast_icon = get_base64_image("image//timefast.png")     
growth_icon = get_base64_image("image//growth.png") 

# 히어로 배너
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-overlay">
            <h1 style="display:flex; align-items:center; justify-content:center; gap:12px;">
                <img src="{moon_icon}" alt="moon" style="width:48px; height:auto; vertical-align:middle;" />
                Overnight.AI
            </h1>
            <p>밤새 준비한 당신의 발표, AI가 정성껏 채점해드립니다.<br>발표 녹음부터 점수 확인까지, 지금 바로 시작하세요.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 탭 UI
tab1, tab2, tab3 = st.tabs(["💡 소개", "⚙️ 기능", "📝 사용 방법"])

with tab1:
    st.subheader("💡 Overnight.AI란?")
    st.markdown(f"""
            <p style="font-size: 1.05rem; line-height: 1.7; color: #e0e0e0;">
                Overnight.AI는 AI 기반 발표 자동 채점 시스템입니다.<br>
                발표 내용을 녹음하고, 사전 설정된 기준에 따라 AI가 자동 평가와 점수를 제공합니다.
            </p></br>
            
            <div style="margin-bottom: 1.2rem; display: flex; align-items: center; gap: 12px;">
                <img src="{evaluation_icon}" alt="moon" style="width: 48px; height: auto; vertical-align: middle;" />
                <div>
                    <b style="color: #FFD8A8;">공정하고 일관된 평가</b><br>
                    <span style="font-size: 0.9rem;">
                        사전 기준에 따라 AI가 누구에게나 동일하게 채점해요.<br>
                        평가자의 주관 없이 신뢰도 높은 결과를 제공합니다.
                    </span>
                </div>
            </div></br>

            <div style="margin-bottom: 1.2rem; display: flex; align-items: center; gap: 12px;">
                <img src="{fast_icon}" alt="moon" style="width: 48px; height: auto; vertical-align: middle;" />
                <div>
                    <b style="color: #a3d5ff;">평가 시간 절약</b><br>
                    <span style="font-size: 0.9rem;">
                        반복되는 발표 평가를 자동화해<br>
                        교사와 학생 모두 시간을 아낄 수 있어요.
                    </span>
                </div>
            </div></br>

            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{growth_icon}" alt="moon" style="width: 48px; height: auto; vertical-align: middle;" />
                <div>
                    <b style="color: #b5e7a0;">발표력 향상</b><br>
                    <span style="font-size: 0.9rem;">
                        발표 전 AI로 미리 점검하고,<br>
                        점수를 기반으로 개선 방향을 확인할 수 있어요.
                    </span>
                </div>
            </div></br>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("⚙️ 주요 기능")
    st.markdown("<div class='feature-section'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">
                <img src="{get_base64_image("image//adjust.png")}" />
            </div>
            <div class="feature-title">평가 기준 설정</div>
            <div class="feature-desc">
                발표 평가 기준을 미리 정해둘 수 있어요.<br>
                예: “목소리 또렷함”, “시간 준수” 같은 항목을<br>
                만들고 중요도를 설정할 수 있어요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">
                <img src="{get_base64_image("image///mike.png")}" />
            </div>
            <div class="feature-title">발표 녹음</div>
            <div class="feature-desc">
                발표 내용을 실시간으로 녹음하고,<br>
                말한 내용을 자동으로 글자로 바꿔줘요.<br>
                복잡한 도구 없이 클릭 몇 번이면 끝나요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">
                <img src="{get_base64_image("image//link.png")}" />
            </div>
            <div class="feature-title">결과 리포트 및 시각화  제공</div>
            <div class="feature-desc">
                AI가 발표 내용을 자동으로 채점해줘요.<br>
                결과는 PDF나 엑셀 파일로 저장하고,<br>
                막대 · 도넛 · 히트맵 등 다양한 그래프로 직관적으로 분석할 수 있어요.
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("📝 사용 방법")
    steps = [
        "좌측 사이드바에서 \"발표자동채점\" 메뉴를 클릭합니다.",
        "팀명, 평가 항목, 항목별 비중을 입력합니다.",
        "녹음 시작 후 발표를 진행하고, 완료 후 \"AI 채점 시작\"을 클릭합니다.",
        "AI 채점 결과를 확인하고 PDF/Excel로 저장합니다.",
        "점수 시각화 메뉴에서 발표 주제를 선택하고, 다양한 그래프 방식으로 팀별 점수를 확인합니다."
    ]

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div class="timeline-step">
            <div class="timeline-bullet">{i}</div>
            <div class="timeline-text">{step}</div>
        </div>
        """, unsafe_allow_html=True)
