import streamlit as st
import os

from utils.data_loader import get_excel_files, load_team_scores, get_team_names
from utils.fonts import set_korean_font
from utils.score_visualizer import draw_bar, draw_radar, draw_donut, draw_line, draw_heatmap, draw_scorecard

# ✅ 한글 폰트 설정
font_prop = set_korean_font()

st.set_page_config(page_title="점수 시각화", layout="wide")

# 💡 배경 스타일 적용
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #14132a, #2a244d, #7a6b96);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .stSelectbox label, .stMarkdown, .stText {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI 채점 결과 시각화")

# 📁 엑셀 파일 로드
excel_dir = os.path.abspath("../../presentation_grader/backend/results/excel")
excel_files = get_excel_files(excel_dir)

if not excel_files:
    st.warning("❌ 결과 엑셀 파일이 존재하지 않습니다.")
    st.stop()

selected_file = st.selectbox("📑 발표 주제 선택:", excel_files)
file_path = os.path.join(excel_dir, selected_file)

try:
    df, _ = load_team_scores(file_path, team_name=None)  # team list만 추출용
except Exception as e:
    st.error(f"❌ 엑셀 파일 읽기 오류: {e}")
    st.stop()

team_names = get_team_names(df)
team_name = st.selectbox("👥 팀 이름 선택:", team_names)

if not team_name:
    st.warning("팀을 선택해주세요.")
    st.stop()

_, score_dict = load_team_scores(file_path, team_name)
if score_dict is None:
    st.error(f"{team_name}에 대한 데이터가 없습니다.")
    st.stop()

# 📌 시각화 방식 선택
chart_type = st.selectbox("📊 시각화 방식 선택", [
    "막대 그래프", "방사형 그래프", "도넛 차트", "꺾은선 그래프",
    "히트맵", "점수 카드"
])

# 📊 시각화 렌더링
col1, col2, col3 = st.columns([1, 3, 1])  # 좌우 여백 확보

with col2:
    if chart_type == "막대 그래프":
        st.pyplot(draw_bar(score_dict, team_name, font_prop))
    elif chart_type == "방사형 그래프":
        st.pyplot(draw_radar(score_dict, team_name, font_prop))
    elif chart_type == "도넛 차트":
        st.pyplot(draw_donut(score_dict, team_name, font_prop))
    elif chart_type == "꺾은선 그래프":
        st.pyplot(draw_line(score_dict, team_name, font_prop))
    elif chart_type == "히트맵":
        st.pyplot(draw_heatmap(score_dict, team_name, font_prop))
    elif chart_type == "점수 카드":
        st.pyplot(draw_scorecard(score_dict, team_name, font_prop))

