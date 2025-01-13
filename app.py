import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile

# Title of the app
st.title("Swimmer Detection")

# Load YOLOv11 model
@st.cache_resource
def load_model():
    return YOLO('yolo11n.pt')


model = load_model()

cap = cv2.VideoCapture(2)
stframe = st.empty()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.write("Webcam feed not available.")
        break

    # Perform prediction
    results = model.predict(source=frame, conf=0.01)

    # Show results on each frame
    for r in results:
        annotated_frame = r.plot()

    # Display in Streamlit
    stframe.image(annotated_frame, channels="BGR")

cap.release()


