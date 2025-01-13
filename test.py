import cv2



cameras = []

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(i)
        cameras.append(i)
        cap.release()

if cameras:
    print(f"Connected cameras: {cameras}")
else:
    print("No cameras detected.")
