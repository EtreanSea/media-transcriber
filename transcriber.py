import streamlit as st
from faster_whisper import WhisperModel

# 1. Load a Whisper model
# 2. Ask the model to transcribe file_path
# 3. Collect the text from each segment
# 4. Return the transcript as one string

TF_display = {
    True : "On",
    False : "Off"
}

model_size = "base"
device = "cpu"
compute_type = "int8"

@st.cache_resource
def load_model():
    #Debug
    #st.write("Loading WhisperModel...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    return model


#formats each line of the transcript
def format_seconds(seconds):
    hours = f"{int(seconds//3600):02d}"
    mins = f"{int(seconds//60%60):02d}"
    secs = f"{seconds%60:05.2f}"
    return f"{hours}:{mins}:{secs}"

def format_seconds_srt(seconds):
    hours = f"{int(seconds//3600):02d}"
    mins = f"{int(seconds//60%60):02d}"
    secs = f"{seconds%60:06.3f}"
    return f"{hours}:{mins}:{secs}".replace(".", ",");

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

def format_segment_srt(segment, line_num):
    prefix_parts = []
    prefix_parts.append(f"{line_num}")
    time = f"{format_seconds_srt(segment.start)} --> {format_seconds_srt(segment.end)}"
    prefix_parts.append(time)
    prefix_parts.append(segment.text.strip())
    return "\n".join(prefix_parts)


def transcribe_file(file_path, language_code, show_line, show_time, vad, predict):
    model = load_model()
    segments, info = model.transcribe(file_path, beam_size=2, language=language_code, vad_filter=vad, condition_on_previous_text=predict)
    transcript_display = []
    transcript_srt = []
    for line_num, segment in enumerate(segments, start=1):
        segment_line = format_segment(segment, line_num, show_line, show_time)
        transcript_display.append(segment_line)
        segment_srt = format_segment_srt(segment, line_num)
        transcript_srt.append(segment_srt)

    transcript_info = f"""
Transcription model: {model_size} (faster whisper)
Processing device: {device}
Compute mode: {compute_type}
Selected language: {language_code}
Detected Language: {info.language}
Voice activity filter: {TF_display[vad]}
Prediction: {TF_display[predict]}
Accuracy confidence: {info.language_probability}
"""
    
    return [f"""{"\n".join(transcript_display)}""", f"""{"\n\n".join(transcript_srt)}""", transcript_info]


#only run if directly executing transcriber.py, wont run when app.py imports transcriber.py
if __name__ == "__main__":
    result = transcribe_file(
        "samples/test.mp3",
        None,
        False,
        True,
        False,
        False
    )
    print(result)