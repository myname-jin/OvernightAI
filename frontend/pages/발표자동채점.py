import streamlit as st
import os
import time
from audiorecorder import audiorecorder
import io
import requests
import re
# 페이지 설정
st.set_page_config(page_title="AI 발표 채점기", layout="wide")

# --------------------------
# 🌙 전체 스타일: 배경 + 폰트 + 텍스트 색상 + UI 요소
# --------------------------
st.markdown("""
    <style>
            
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #14132a, #2a244d, #7a6b96);
        font-family: 'Pretendard', sans-serif;
        color: white;
        margin: 0;
        padding: 0;
    }

    h1, h2, h3, h4, h5, h6, label, .subtitle {
        color: white !important;
    }

    input::placeholder, textarea::placeholder {
        color: #CCCCCC !important;
    }
    #team-save-button button {
        background-color: #4c6ef5 !important;
        color: white !important;
        font-weight: bold;
        padding: 0.6rem 1.4rem !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        border: none !important;
        transition: background-color 0.3s ease;
    }
    #team-save-button button:hover {
        background-color: #3b5bdb !important;
    }
    .glass-box {
        background: rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.15);
    }

    .big-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #cccccc;
        font-style: italic;
    }

    button[kind="primary"] {
        background-color: #ff4b4b !important;
        color: white !important;
        margin-right: 1rem;
    }

    button[kind="secondary"] {
        background-color: #4c6ef5 !important;
        color: white !important;
    }

    textarea {
        border-radius: 10px !important;
        border: none !important;
        padding: 1rem !important;
        background-color: #f9f9f9 !important;
        color: black !important;
        font-size: 0.95rem !important;
    }

    .result-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        color: white;
        font-size: 0.95rem;
    }
    div.st-audiorecorder {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

           
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 🌙 헤더 (브랜드 이름)
# --------------------------
from PIL import Image
import base64

# 이미지 Base64로 인코딩
def image_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

image_path = os.path.join(os.path.dirname(__file__), "..", "image", "moonnight.png")
moon_icon_base64 = image_to_base64(image_path)


# 기존 헤더 교체
st.markdown(f"""
<div class="glass-box">
    <div class="big-title" style="display: flex; align-items: center; gap: 20px;">
        <img src="data:image/png;base64,{moon_icon_base64}" style="width: 40px; height: auto; vertical-align: middle;" />
        Overnight.AI
    </div>
    <div class="subtitle">밤새 준비한 발표, AI가 대신 채점해드립니다.</div>
</div>
""", unsafe_allow_html=True)


# --------------------------
# 세션 상태 초기화 (항목 수)
# --------------------------
if "num_criteria" not in st.session_state:
    st.session_state.num_criteria = 1

# --------------------------
# 1. 팀명 + 발표 주제 입력
# --------------------------

st.header("👥 팀 정보 입력")
team_name = st.text_input("팀명을 입력하세요", placeholder="예: 4조, AI팀")

st.header("📝 발표 주제 입력")
presentation_topic = st.text_input("발표 주제를 입력하세요", placeholder="해커톤 대회")

# --------------------------
# ✅ 팀명 + 주제 통합 저장 버튼
# --------------------------
with st.container():
    st.markdown('<div id="team-save-button">', unsafe_allow_html=True)
    save_all_clicked = st.button("✅ 팀 정보 저장")  # 버튼명 변경
    st.markdown("</div>", unsafe_allow_html=True)

# 클릭 시 유효성 검사 + 세션 저장
if save_all_clicked:
    if not team_name.strip():
        st.warning("⚠️ 팀명을 입력해주세요.")
    elif not presentation_topic.strip():
        st.warning("⚠️ 발표 주제를 입력해주세요.")
    else:
        # 세션에 저장 (다른 페이지나 기능에서 재사용 가능)
        st.session_state.team_name = team_name
        st.session_state.presentation_topic = presentation_topic

        st.success(f"✅ 현재 [{team_name}] 팀의 발표 [{presentation_topic}] 를 평가 중입니다.")

#---------------------------
# 2. 채점 기준 설정
# --------------------------
st.markdown("---")
st.header("📋 채점 기준 및 비중 설정")

# ➕➖ 항목 조절 버튼
col_add, col_remove = st.columns([1, 1])
with col_add:
    if st.button("➕ 채점 항목 추가"):
        st.session_state.num_criteria += 1
with col_remove:
    if st.button("➖ 채점 항목 삭제"):
        if st.session_state.num_criteria > 1:
            st.session_state.num_criteria -= 1
        else:
            st.warning("항목은 최소 1개 이상이어야 합니다.")

criteria = []
for i in range(1, st.session_state.num_criteria + 1):
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        criterion = st.text_input(f"항목 {i} 이름", key=f"criterion_{i}", placeholder="예: 창의력")
    with col2:
        description = st.text_input(f"설명 {i}", key=f"description_{i}", placeholder="예: 새로운 관점에서 주제를 해석했는가?")
    with col3:
        weight = st.number_input(f"점수비중 {i}", step=1, key=f"weight_{i}" )

    if criterion and description:
        criteria.append({
            "name": criterion,
            "description": description,
            "weight": weight
        })

# ✅ 기준 저장 버튼
if st.button("💾 기준 저장하기"):
    if not team_name:
        st.warning("⚠️ 팀명을 입력해주세요.")
    elif len(criteria) == 0:
        st.warning("⚠️ 모든 항목을 입력해야 저장할 수 있습니다.")
    else:
        try:
            res = requests.post("http://localhost:5000/save_criteria", json={
                "team": team_name,
                "topic": presentation_topic,  # 이 줄 추가하면 주제도 저장 가능
                "criteria": criteria
            })
            if res.ok:
                st.success(f"✅ [{team_name}] 팀의 기준이 성공적으로 저장되었습니다!")
            else:
                st.error("❌ 저장 실패: 서버에서 에러가 발생했습니다.")
        except Exception as e:
            st.error(f"❗ 서버 연결 실패: {e}")

# --------------------------
# 3. 발표 녹음 (직접 버튼)
# --------------------------
st.markdown("---")
st.header("🎙️ 발표 녹음")

audio = audiorecorder("🔴 녹음 시작", "⏹ 녹음 중지")

# --------------------------
# 분석 결과 관련 세션 변수 초기화
# --------------------------
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "grading_result" not in st.session_state:
    st.session_state.grading_result = []

# --------------------------
# 녹음 완료 후 처리
# --------------------------
if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")
    st.success("✅ 녹음 완료됨! 아래 버튼으로 AI 채점을 시작하세요.")

    if st.button("✅ AI 채점 시작"):
        with st.spinner("AI가 발표 내용을 분석하고 채점 중입니다..."):
            try:
                audio_bytes = audio.export(format="wav").read()
                files = {
                    "audio": (f"{team_name}.wav", io.BytesIO(audio_bytes), "audio/wav")
                }
                data = {
                    "teamName": team_name,
                    "presentationTopic": st.session_state.get("presentation_topic", "")
                }
                res = requests.post("http://localhost:5000/analyze", files=files, data=data)

                if not res.ok:
                    try:
                        error_detail = res.json().get("error", "서버 내부 오류")
                    except Exception:
                        error_detail = res.text
                    st.error(f"❌ 서버 응답 오류: {error_detail}")
                    st.stop()

                result = res.json()
                st.session_state.transcript = result.get("transcript", "")
                st.session_state.grading_result = result.get("grading", [])
                st.success("✅ 채점 완료!")

            except Exception as e:
                st.error(f"❌ 요청 자체 실패: {e}")

else:
    st.info("🎤 먼저 발표 내용을 녹음해주세요.")

# --------------------------
# 4. 분석 결과 출력 (하나만 남김)
# --------------------------
if st.session_state.transcript or st.session_state.grading_result:
    st.markdown("---")
    st.header("📑 분석 결과")

    st.subheader("🗣️ 텍스트:")
    st.text_area("발표 내용(STT 결과)", value=st.session_state.transcript, height=120, disabled=False)


    st.subheader("📈 결과:")
    if st.session_state.grading_result:
        for i, item in enumerate(st.session_state.grading_result, 1):
            st.markdown(f"""
<div class="result-card">
<b>항목 {i}</b>: {item['score']}점  
📝 {item['feedback']}
</div>
""", unsafe_allow_html=True)
    else:
        st.info("❗ 채점 결과가 없습니다.")


# --------------------------
# 5. 결과 파일 다운로드
# --------------------------
st.markdown("---")
st.header("📂 채점 결과 파일 다운로드")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RESULTPDF_DIR = os.path.join(PROJECT_ROOT, "backend", "results", "pdf")
RESULTEXCEL_DIR = os.path.join(PROJECT_ROOT, "backend", "results", "excel")

teamprefix = team_name if team_name else "예시팀"

pdf_path = os.path.join(RESULTPDF_DIR, f"{teamprefix}.pdf")
safe_topic = st.session_state.get("presentation_topic", "default_topic").replace(" ", "_")
safe_topic = re.sub(r'[\\/*?:"<>|]', "", safe_topic)  # 파일 이름으로 안 되는 문자 제거
xlsx_path = os.path.join(RESULTEXCEL_DIR, f"{safe_topic}.xlsx")

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        st.download_button("📄" + team_name+" 팀 PDF 파일 다운로드", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")
else:
    st.info("❗ PDF 파일이 아직 없습니다.")

if os.path.exists(xlsx_path):
    with open(xlsx_path, "rb") as f:
        st.download_button("📊 엑셀 파일 다운로드", data=f, file_name=os.path.basename(xlsx_path), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("❗ 엑셀 파일이 아직 없습니다.")
