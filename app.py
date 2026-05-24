# Version 0.7.5: made vad and prediction based on previous text optional

import os
import tempfile

import streamlit as st
from transcriber import transcribe_file


audio = ["mp3", "wav", "flac"]
video = ["mp4", "mov"]

def display_file_info(file):
    st.markdown(f":red[Name:] {os.path.splitext(file.name)[0]}")
    st.markdown(f":red[Suffix:] {os.path.splitext(file.name)[1]}")
    st.markdown(f":red[Type:] {file.type}")
    st.markdown(f":red[Size:] :grey-background[{file.size / 1000000 : .2f}MB]")
def display_preview(file):
    if file.type.startswith("audio"):
        st.audio(file)
    elif file.type.startswith("video"):
        st.video(file)
    else:
        st.write("File type not supported")

if "transcript" not in st.session_state:
    st.session_state['transcript'] = ""
if "last_uploaded_file" not in st.session_state:
    st.session_state['last_uploaded_file'] = None

st.title("Media-Transcriber")

#Debug
#st.write("st_session_state.object")
#st.session_state


st.markdown(":grey-background[:rainbow[**.mp3**]]:grey-background[:rainbow[**.mp4**]] :grey-background[:rainbow[**.flac**]] :grey-background[:rainbow[**.mov**]] :grey-background[:rainbow[**...**]]")
st.caption("All audio/video supported")
uploaded_file = st.file_uploader(label="Upload audio/video",accept_multiple_files=False, type=["mp3", "wav", "flac", "alac", "mp4", "m4a", "mov"], max_upload_size=500, help="Drag files or click Upload")

#After file is uploaded
if uploaded_file is not None:

    if st.session_state['last_uploaded_file'] != uploaded_file.name:
        st.session_state['transcript'] = ""
        st.session_state['last_uploaded_file'] = uploaded_file.name
    display_file_info(uploaded_file)
    display_preview(uploaded_file)

    language = st.selectbox("Select Language", ["Auto-Detect", "ENG", "中文"])
    language_map = {
        "Auto-Detect" : None,
        "ENG" : "en",
        "中文" : "zh"
    }
    language_code = language_map[language]

    #checkboxes for toggling timestamps and line numbers
    show_time = st.checkbox(label="Timestamps", value=True)
    show_line = st.checkbox(label="Line numbers", value=False)
    activate_vad = st.checkbox(label="Voice Activity Detection Filter", value=False)
    activate_guess = st.checkbox(label="Use Prediction", value=True)

    #Transcribe button
    if st.button("Transcribe", type="primary"):
        #1. get suffix from uploaded_file (.mp4, .flac ...)
        #2. create named temp file with that suffix
        #3. write uploaded_file's data into temp file
        #4  close temp file without deleting so other libraries can read it
        #5. transcribe
        #6. delete temp file
        uploaded_file_suffix = os.path.splitext(uploaded_file.name)[1]
        uploaded_file_bytes = uploaded_file.getvalue()
        with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file_suffix) as temp_file:
            temp_file.write(uploaded_file_bytes)
            temp_file_path = temp_file.name
        st.session_state['transcript'] = transcribe_file(temp_file_path, uploaded_file.name,language_code, show_line, show_time, activate_vad, activate_guess)
        os.remove(temp_file_path)
    
    #Debug
    #st.session_state

    if st.session_state['transcript']:
        txt = st.text_area(
            "Transcript", 
            value=st.session_state['transcript'], 
            height="content")
        download_type = st.selectbox("Export as...", [".txt"], index = None, placeholder = "Select File Type")
        if download_type is not None:
            st.download_button(label="Download", data=txt, file_name="transcript" + download_type, type="primary", icon=":material/download:")



else:
    st.write("No files uploaded yet")

