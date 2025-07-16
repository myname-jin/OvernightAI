# 🌓 OvernightAI – AI 발표 자동 채점 시스템

AI를 활용하여 **발표를 녹음하고**, 기준에 따라 **자동 채점 및 피드백을 생성**하는 발표 평가 시스템입니다.  
이 저장소는 팀 프로젝트를 바탕으로 **개인 포트폴리오용으로 정리**되었습니다.

---
## 🌐 시스템 개요

**AI 발표 채점 시스템**은 다음과 같은 흐름으로 작동합니다:

> 발표자 → 🎙 녹음 → 🧠 AI 분석 → 📄 점수 및 피드백 제공

Streamlit 기반 웹 UI에서 사용자가 녹음을 시작하면, Whisper AI가 음성을 텍스트로 변환하고, 변환된 텍스트는 ChatGPT API를 통해 분석되어 각 항목별 점수와 피드백이 생성됩니다. 결과는 PDF 및 Excel로 저장되고, Streamlit을 통해 시각화됩니다.

---

## 🧭 시스템 흐름 및 기술 아키텍처

📌 아래 이미지는 **전체 시스템 흐름**과 동시에 사용된 주요 기술들을 한눈에 보여줍니다:

<p align="center">
  <img src="readmeimg/systempage.png" alt="시스템 아키텍처" width="700"/>
</p>

---

## ⚙️ 사용 기술 스택

| 항목         | 내용 |
|--------------|------|
| 언어         | Python |
| 웹 프레임워크 | Flask (서버), Streamlit (클라이언트) |
| 음성 인식    | Whisper AI (OpenAI) |
| 채점 모델    | ChatGPT (OpenAI API) |
| 프론트엔드   | Streamlit + HTML/CSS/JS |
| 결과 저장    | ReportLab (PDF), OpenPyXL (Excel) |
| 시각화       | Matplotlib (Streamlit 내부 차트 출력) |

---

## 💡 주요 기능 요약

- 🎙 웹 기반 발표 녹음
- 🧠 Whisper를 이용한 음성 → 텍스트 변환
- 🤖 GPT-4 기반 자동 채점 및 피드백
- 📄 PDF 및 Excel로 결과 저장
- 📊 점수 시각화 (Streamlit UI)

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

