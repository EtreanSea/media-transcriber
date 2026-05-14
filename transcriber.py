import streamlit as st
from faster_whisper import WhisperModel

# 1. Load a Whisper model
# 2. Ask the model to transcribe file_path
# 3. Collect the text from each segment
# 4. Return the transcript as one string

@st.cache_resource
def load_model():
    #Debug
    #st.write("Loading WhisperModel...")
    model_size = "tiny"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return model

def transcribe_file(file_path, original_filename, language_code):
    model = load_model()
    segments, info = model.transcribe(file_path, beam_size=2, language=language_code)
    transcript_lines = []
    for segment in segments:
        segment_line = f"line {segment.id}: {segment.text}"
        transcript_lines.append(segment_line)


    return f"""
    Transcript: {"\n".join(transcript_lines)}
    
    Original filename: {original_filename}
    Temp file path: {file_path}
    Language code: {language_code}
    Detected Language: {info.language}
    Accuracy confidence: {info.language_probability}

"""

#only run if directly executing transcriber.py, wont run when app.py imports transcriber.py
if __name__ == "__main__":
    result = transcribe_file("samples/test.mp3", "test.mp3", None)
    print(result)