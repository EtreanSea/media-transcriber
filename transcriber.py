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


#formats each line of the transcript
def format_seconds(seconds):
    hours = f"{int(seconds//3600):02d}"
    mins = f"{int(seconds//60%60):02d}"
    secs = f"{seconds%60:05.2f}"

    return f"{hours}:{mins}:{secs}"
def format_segment(segment, line_num, show_line, show_time):
    prefix_parts = []
    if show_line:
        line = f"line {line_num}:"
        prefix_parts.append(line)
    if show_time:
        time = f"[{format_seconds(segment.start)} -> {format_seconds(segment.end)}]"
        prefix_parts.append(time)

    prefix_parts.append(segment.text.strip())
    return " ".join(prefix_parts)


def transcribe_file(file_path, original_filename, language_code, show_line, show_time):
    model = load_model()
    segments, info = model.transcribe(file_path, beam_size=2, language=language_code)
    transcript_lines = []
    for line_num, segment in enumerate(segments, start=1):
        segment_line = format_segment(segment, line_num, show_line, show_time)
        transcript_lines.append(segment_line)


    return f"""{"\n".join(transcript_lines)}

Original filename: {original_filename}
Language code: {language_code}
Detected Language: {info.language}
Accuracy confidence: {info.language_probability}
"""

#only run if directly executing transcriber.py, wont run when app.py imports transcriber.py
if __name__ == "__main__":
    result = transcribe_file("samples/test.mp3", "test.mp3", None)
    print(result)