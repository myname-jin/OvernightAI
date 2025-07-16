import os
import json
import re
import whisper
import subprocess
from flask import Flask, request, jsonify, render_template, send_from_directory
from openai_grader import evaluate_presentation, polish_transcript
# [임태종] 채점 결과 PDF 및 Excel 요약 저장 메서드 import
from report_generator import create_pdf, save_summary_excel
print("현재 실행 위치:", os.getcwd())

app = Flask(__name__, static_folder='static', template_folder='templates')
audio_dir = "audio"
criteria_dir = "criteria"

os.makedirs(audio_dir, exist_ok=True)
os.makedirs(criteria_dir, exist_ok=True)

#@app.route("/")
#def home():
#    return render_template("index.html")

@app.route("/save_criteria", methods=["POST"])
def save_criteria():
    data = request.get_json()

    print("[DEBUG] /save_criteria 호출됨")
    print("[DEBUG] 받은 데이터:", data)

    team_name = data.get("team", "default_team")
    presentation_topic = data.get("presentation_topic") or data.get("topic", "")
    presentation_topic = presentation_topic.strip()
    criteria = data.get("criteria", [])

    print("[DEBUG] 팀명:", team_name)
    print("[DEBUG] 주제명:", presentation_topic)
    print("[DEBUG] 평가 기준:", criteria)

    if not presentation_topic:
        return jsonify({"error": "❗ 발표 주제가 없습니다."}), 400

    safe_topic = re.sub(r'[\\/:*?"<>|]', "_", presentation_topic)
    criteria_path = os.path.join(criteria_dir, f"{safe_topic}.json")
    print("[DEBUG] 저장 경로:", criteria_path)

    try:
        with open(criteria_path, "w", encoding="utf-8") as f:
            json.dump(criteria, f, ensure_ascii=False, indent=2)
        print("[DEBUG] 기준 저장 성공")
        return jsonify({"status": "success"})
    except Exception as e:
        print("[ERROR] 기준 저장 실패:", str(e))
        return jsonify({"error": f"❌ 기준 저장 실패: {str(e)}"}), 500
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        team_name = request.form["teamName"]
        presentation_topic = request.form["presentationTopic"] 
        audio_file = request.files["audio"]
    except Exception as e:
        return jsonify({"error": f"요청 데이터 부족: {str(e)}"}), 400

    base_filename = os.path.splitext(audio_file.filename)[0]
    audio_ext = os.path.splitext(audio_file.filename)[1].lower()
    audio_path = os.path.join(audio_dir, f"{base_filename}{audio_ext}")

    # ✅ 발표 주제명을 기준으로 안전한 파일명 생성
    safe_topic = re.sub(r'[\\/:*?"<>|]', "_", presentation_topic)
    criteria_path = os.path.join(criteria_dir, f"{safe_topic}.json")

    # 1. 오디오 저장
    audio_file.save(audio_path)

    # 2. 기준 파일 확인
    if not os.path.exists(criteria_path):
        return jsonify({"error": "❗ 기준 파일이 존재하지 않습니다. 먼저 기준을 저장해주세요."}), 400

    # 3. Whisper STT 처리
    try:
        model = whisper.load_model("base")

        if audio_ext == ".webm":
            wav_path = os.path.join(audio_dir, f"{base_filename}.wav")
            subprocess.run(["ffmpeg", "-y", "-i", audio_path, wav_path], check=True)
            result = model.transcribe(wav_path)
        else:
            result = model.transcribe(audio_path)

        transcript = result["text"]
    except Exception as e:
        return jsonify({"error": f"🗣️ 음성 인식 실패: {str(e)}"}), 500

    # 4. 데이터 전처리
    transcript = polish_transcript(transcript)

    # 5. 기준 읽기
    try:
        with open(criteria_path, "r", encoding="utf-8") as f:
            criteria = json.load(f)
    except Exception as e:
        return jsonify({"error": f"📄 기준 파일 읽기 실패: {str(e)}"}), 500

    # 6. GPT 채점
    try:
        grading_result = evaluate_presentation(transcript, criteria)
        create_pdf(team_name, criteria, grading_result)
        save_summary_excel(team_name, presentation_topic, criteria, grading_result)
        return jsonify({
            "transcript": transcript,
            "grading": grading_result
        })
    except Exception as e:
        return jsonify({"error": f"🤖 AI 평가 실패: {str(e)}"}), 500

# 정적 리소스(js/css) 제공용 (선택)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)
