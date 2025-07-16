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
<img width="435" height="355" alt="image" src="https://github.com/user-attachments/assets/9ef12d7b-0d6a-49d3-8e87-9f55fe03ba9c" />

---

## 🛠 기술 스택

| 분류       | 기술 스택                                |
|------------|-------------------------------------------|
| 백엔드     | Python, Flask, Whisper, OpenAI GPT       |
| 프론트엔드 | Streamlit                                 |
| 기타       | ReportLab (PDF), OpenPyXL (Excel), Matplotlib (시각화)

---

## 📁 프로젝트 구조

<pre>

presentation_grader/
├── backend/                            # 🎯 백엔드 서버 및 처리 로직
│   ├── app.py                          # Flask 서버 실행 및 라우팅
│   ├── analyzer.py                     # Whisper 음성 → 텍스트 변환
│   ├── openai_grader.py                # GPT API를 통한 채점 로직
│   ├── report_generator.py             # PDF, Excel 결과 저장 처리
│   ├── audio/                          # 🔊 업로드된 녹음 파일 저장 폴더
│   │   └── 예시.wav                      # 예시 오디오 파일
│   ├── results/                        # 📁 채점 결과 저장 폴더
│   │   ├── pdf/                        # 생성된 PDF 결과 저장
│   │   │   └── 예시.pdf                  # 예시 결과 PDF
│   │   └── excel/                      # 생성된 Excel 결과 저장
│   │       └── 예시.xlsx                # 예시 결과 엑셀
│   └── criteria/                       # 📋 채점 기준 JSON 저장 폴더
│       └── 예시_기준.json                # 예시 기준 JSON 파일
│
├── frontend/                           # 🎨 Streamlit 프론트엔드 앱
│   ├── OvernightAI.py                  # 메인 페이지 (팀명 입력, 녹음, 채점)
│   ├── pages/                          # 📄 추가 페이지 모음
│   │   ├── 02_점수_시각화.py             # 점수 시각화 메인 페이지
│   │   └── 점수_세부_페이지.py           # 점수 항목별 세부 시각화
│   └── utils/                          # 🛠️ 시각화 관련 유틸리티 모음
│       ├── data_loader.py              # 엑셀 데이터 로드 함수
│       ├── fonts.py                    # 한글 폰트 설정
│       └── score_visualizer.py         # 시각화 차트 생성 함수
│
├── fonts/                              # 🔤 한글 폰트 폴더
│   └── malgun.ttf                      # 맑은 고딕 폰트 파일
│
├── replace.txt                         # 🧼 개인정보 키 제거용 치환 텍스트 파일 (옵션)
└── README.md                           # 📘 프로젝트 설명 문서

</pre>

