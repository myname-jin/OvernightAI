import openai

openai.api_key = "REMOVED_API_KEYvWurSzkLapvIuBMB694f5pl--9arqgFGJvs6RASDZ5049Mx1qIUxBld-s4aK4GDbDCb_5-d1JRT3BlbkFJ2kRGS8CYMGILEOPc0xs72rXFdmNE-7_zcJSb87rC8xB-RYlW352yF96dUUnXFJtZvlLjpZjBcA"

def evaluate_presentation(script: str, criteria: list):
    system_prompt = (
        "너는 AI 발표 채점 도우미야. 발표 내용을 보고, 각 항목별 기준에 따라 점수와 피드백을 줘.\n"
        "점수는 0부터 항목의 최대 점수 사이 정수여야 해.\n"
        "출력 형식은 반드시 다음을 따르도록 해:\n"
        "점수: <숫자>\n"
        "피드백: <한 줄 설명>"
    )

    outputs = []

    for i, criterion in enumerate(criteria):
        user_prompt = (
            f"발표 내용:\n{script}\n\n"
            f"[항목 {i+1}] 이름: {criterion['name']}\n"
            f"설명: {criterion['description']}\n"
            f"배점: {criterion['weight']}점\n"
            f"이 항목을 채점해줘."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )

        reply = response.choices[0].message["content"]
        lines = reply.strip().split("\n")
        score_line = next((line for line in lines if line.startswith("점수:")), "")
        feedback_line = next((line for line in lines if line.startswith("피드백:")), "")

        outputs.append({
            "score": score_line.replace("점수:", "").strip(),
            "feedback": feedback_line.replace("피드백:", "").strip()
        })

    return outputs


def polish_transcript(transcript: str) -> str:
    system_prompt = (
        "다음은 발표 내용을 음성인식으로 추출한 텍스트입니다. "
        "오탈자, 잘못 인식된 단어, 문맥상 어색한 부분을 자연스럽게 수정해 주세요. "
        "발표의 말투나 흐름은 유지하고 너무 과하게 고치지 마세요. "
        "수정하는 과정에서 기존에 없는 단어를 추가하지 마세요."
        "텍스트만 출력해 주세요."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ],
        temperature=0.3,
    )

    return response['choices'][0]['message']['content'].strip()