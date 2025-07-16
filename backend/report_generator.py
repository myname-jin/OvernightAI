"""from fpdf import FPDF
import pandas as pd
import os

def save_results(team, result):
    pdf_path = f"../results/{team}.pdf"
    excel_path = f"../results/{team}.xlsx"

    pdf = FPDF()
    pdf.add_page()
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../fonts/malgun.ttf"))
    pdf.add_font('malgun', '', font_path, uni=True)

    pdf.set_font('malgun', '', 14)
    pdf.cell(200, 10, f"{team} 발표 평가 결과", ln=True)

    for k, v in result['feedback'].items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)
    pdf.cell(200, 10, f"총점: {result['total_score']}점", ln=True)
    pdf.output(pdf_path)

    df = pd.DataFrame([{**result['feedback'], "총점": result['total_score']}])
    df.insert(0, "팀명", team)
    df.to_excel(excel_path, index=False)

    return pdf_path, excel_path
"""

import os
from fpdf import FPDF
import pandas as pd
import time

print(f"[DEBUG] report_generator.py 로드됨: {__file__}")

def create_pdf(team_name, criteria, grading_result):
    print("[DEBUG] create_pdf() 진입")

    pdf = FPDF()

    # 🔧 폴더 존재하지 않으면 자동 생성
    pdf_dir = os.path.join("results", "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    
    print("[DEBUG] 현재 실행 위치:", os.getcwd())
    # ✅ 절대 경로 + 존재 확인
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
    FONT_PATH = os.path.join(PROJECT_ROOT, "fonts", "malgun.ttf")   
    print("[DEBUG] FONT_PATH =", FONT_PATH)

    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"❌ 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")
    
    pdf.add_font('malgun', '', FONT_PATH, uni=True)
    pdf.add_font('malgun', 'B', FONT_PATH, uni=True)
    pdf.set_font('malgun', '', 12)
    pdf.set_font('malgun', 'B', 12)
    pdf.add_page()

    # 제목
    pdf.set_font('malgun', 'B', 20)
    pdf.multi_cell(0, 10, f"{team_name} 팀", align="C")
    pdf.ln(10)

    # 평가 기준
    pdf.set_font('malgun', 'B', 14)
    pdf.cell(0, 10, "평가 기준", ln=True)
    pdf.set_font('malgun', '', 12)
    total = 0
    for c in criteria:
        pdf.cell(0, 8, f"• {c['name']} : {c['weight']}점", ln=True)
        total += c["weight"]
    pdf.cell(0, 8, f"• 합계 : {total}점", ln=True)
    pdf.ln(5)

    # 채점 결과 표
    pdf.set_font('malgun', 'B', 14)
    pdf.cell(0, 10, "채점 결과", ln=True)
    pdf.ln(3)

    pdf.set_font("malgun", '', 12)
    total_score = 0

    for i, criterion in enumerate(criteria):
        name = criterion["name"]
        score = int(grading_result[i]["score"])
        feedback = grading_result[i]["feedback"]
        total_score += score

        pdf.set_font('malgun', 'B', 12)
        pdf.cell(0, 8, f"{name} : {score}점", ln=True)

        pdf.set_font('malgun', '', 12)
        pdf.multi_cell(0, 8, f"피드백 : {feedback}")

        pdf.ln(1)
        pdf.set_draw_color(150)
        pdf.set_line_width(0.3)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(3)

    pdf.ln(5)
    pdf.set_font('malgun', 'B', 12)
    pdf.cell(0, 10, f"총점 : {total_score}점", ln=True)

    # 🔥 PDF 파일 저장
    pdf_path = os.path.join(pdf_dir, f"{team_name}.pdf")  # ✅ 팀명 기준 저장
    pdf.output(pdf_path)


def save_summary_excel(team_name, presentation_topic, criteria, grading_result):
    # 📁 저장 경로 설정
    summary_dir = "results/excel/"
    os.makedirs(summary_dir, exist_ok=True)

    # 🧱 열 구조 생성 (기준 기준으로)
    new_columns = ["팀명"] + [c["name"] for c in criteria] + ["총점"]
    safe_topic = presentation_topic.replace(" ", "_")
    path = os.path.join(summary_dir, f"{safe_topic}.xlsx")

    # 📊 점수 계산
    total_score = sum(int(r["score"]) if str(r["score"]).isdigit() else 0 for r in grading_result)
    row = {
        "팀명": team_name,
        **{c["name"]: int(r["score"]) if str(r["score"]).isdigit() else 0 for c, r in zip(criteria, grading_result)},
        "총점": total_score
    }

    # 📄 기존 파일 존재 여부 및 열 비교
    if os.path.exists(path):
        existing = pd.read_excel(path)
        existing_columns = list(existing.columns)

        if existing_columns != new_columns:
            # 📁 기존 summary.xlsx 백업
            backup_path = os.path.join(summary_dir, f"summary_backup_{int(time.time())}.xlsx")
            os.rename(path, backup_path)
            print(f"📁 기준 변경 → 기존 summary.xlsx 백업됨: {backup_path}")
            df = pd.DataFrame([row])
        else:
            df = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    # 💾 저장
    df.to_excel(path, index=False)