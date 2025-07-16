# 🌓 OvernightAI – AI 발표 자동 채점 시스템

AI를 활용하여 **발표를 녹음하고**, 기준에 따라 **자동 채점 및 피드백을 생성**하는 발표 평가 시스템입니다.  
이 저장소는 팀 프로젝트를 바탕으로 **개인 포트폴리오용으로 정리**되었습니다.

---

## 🚀 주요 기능

- 🎙 발표 녹음 (웹 UI)
- 🔁 Whisper 기반 음성 → 텍스트 변환
- 🧠 GPT API 기반 채점 및 피드백 생성
- 📄 채점 결과 PDF, Excel 저장
- 📊 점수 시각화 페이지 제공

---

## 🛠 기술 스택

| 분류       | 기술 스택                                |
|------------|-------------------------------------------|
| 백엔드     | Python, Flask, Whisper, OpenAI GPT       |
| 프론트엔드 | Streamlit                                 |
| 기타       | ReportLab (PDF), OpenPyXL (Excel), Matplotlib (시각화)

---

## 📁 프로젝트 구조

presentation_grader/
├── backend/
│ ├── app.py # Flask 서버 (STT, 채점 처리)
│ ├── analyzer.py # Whisper 음성 텍스트 변환
│ ├── openai_grader.py # GPT API 채점 로직
│ ├── report_generator.py # PDF 및 Excel 저장기
├── frontend/
│ ├── OvernightAI.py # Streamlit UI 메인 페이지
│ └── pages/ # 점수 시각화 서브 페이지
├── frontend/utils/ # 시각화용 유틸리티
├── fonts/ # 말랑한 한글 폰트
├── replace.txt # 필터링에 사용된 문자열 정의 (옵션)
└── README.md
