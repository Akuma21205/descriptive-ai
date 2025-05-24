import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av

# App config
st.set_page_config(
    page_title="Descriptive AI",
    page_icon="🤖",
    layout="wide",
)

st.title("Descriptive AI 🤖")
st.write(
    "This web app uses your webcam and OpenAI models to generate descriptive content based on visual input."
)

# WebRTC config (optional but useful for NAT traversal)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Convert incoming frames to ndarray (basic passthrough for now)
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Initialize session state
if "camera_started" not in st.session_state:
    st.session_state.camera_started = False

# Camera Controls
st.markdown("### Camera Controls")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Launch Camera", use_container_width=True):
        st.session_state.camera_started = True

with col2:
    if st.button("🛑 Stop Camera", use_container_width=True):
        st.session_state.camera_started = False

# Show camera stream if started
if st.session_state.camera_started:
    st.success("📷 Camera is active.")
    webrtc_streamer(
        key="cam",
        video_frame_callback=video_frame_callback,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        async_processing=True,
    )
else:
    st.info("Camera is off. Click 'Launch Camera' to start.")
