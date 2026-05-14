# Version 0.3: UI calls separate fake transcriber function.

import streamlit as st
from transcriber import transcribe_file


audio = ["mp3", "wav", "flac"]
video = ["mp4", "mov"]

def display_file_info(file):
    st.markdown(f":red[Name:] {file.name}")
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

st.title("TikTok-Transcriber")

#Debug
st.write("st_session_state.object")
st.session_state


st.markdown(":grey-background[:rainbow[**.mp3**]]:grey-background[:rainbow[**.mp4**]] :grey-background[:rainbow[**.flac**]] :grey-background[:rainbow[**.mov**]] :grey-background[:rainbow[**...**]]")
st.caption("All audio/video supported")
uploaded_file = st.file_uploader(label="Upload audio/video",accept_multiple_files=False, type=["mp3", "wav", "flac", "alac", "mp4", "m4a", "mov"], max_upload_size=500, help="Drag files or click Upload")


if uploaded_file is not None:
    if st.session_state['last_uploaded_file'] != uploaded_file.name:
        st.session_state['transcript'] = ""
        st.session_state['last_uploaded_file'] = uploaded_file.name
    display_file_info(uploaded_file)
    display_preview(uploaded_file)
    language = st.selectbox("Select Language", ["Auto-Detect", "ENG", "中文"])
    if st.button("Transcribe", type="primary"):
        st.session_state['transcript'] = transcribe_file(uploaded_file, language)
    
    #Debug
    st.session_state

    if st.session_state['transcript']:
        txt = st.text_area(
            "Transcript", 
            value=st.session_state['transcript'], 
            height="content")
        download_type = st.selectbox("Export as...", [".txt", ".vtt", ".srt"], index = None, placeholder = "Select File Type")
        if download_type is not None:
            st.download_button(label="Download", data=txt, file_name="transcript" + download_type, type="primary", icon=":material/download:")



else:
    st.write("No files uploaded yet")

