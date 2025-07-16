import whisper
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path, language='ko')
    return result.get("text", "")
