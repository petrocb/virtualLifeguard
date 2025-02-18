import cv2
from ultralytics.models.yolo.model import YOLO
import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk

class SwimmerDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swimmer Detection")

        # Main frame to hold video and other widgets
        self.main_frame = Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Video frame inside the main frame
        self.video_frame = Frame(self.main_frame, width=640, height=480, bd=2, relief=tk.SUNKEN)
        self.video_frame.grid(row=0, column=0, padx=5, pady=5)

        self.label = Label(self.video_frame)
        self.label.pack()

        # Placeholder for extra widgets (e.g., buttons, info labels)
        self.streamOptionsFrame = Frame(self.main_frame)
        self.streamOptionsFrame.grid(row=1, column=0)

        tk.Label(self.streamOptionsFrame, text="brightness").grid(row=0, column=0)
        tk.Scale(self.streamOptionsFrame, from_=0, to=100, orient="horizontal").grid(row=0, column=1)

        # Load model and start video capture
        self.model = self.load_model()
        self.cap = cv2.VideoCapture(0)
        self.running = True
        # self.tracker = tracker()
        self.update_frame()


    def load_model(self):
        return YOLO('yolo11n.pt')

    def update_frame(self):
        _, frame = self.cap.read()
        results = self.model.track(source=frame, conf=0.01, persist=True)
        # results[0].plot(labels=True)
        for r in results:
            r.plot(labels=True)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        # print("Updating frame")
        self.root.after(10, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()




#
# cap.release()
# cv2.destroyAllWindows()
if __name__ == "__main__":
    root = tk.Tk()
    app = SwimmerDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
