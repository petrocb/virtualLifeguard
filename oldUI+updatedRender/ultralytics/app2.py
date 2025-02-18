import tkinter as tk
from tkinter import Label, Frame
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk
from tracker import tracker


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
        self.cap = cv2.VideoCapture(1)
        self.running = True
        self.tracker = tracker()
        self.update_frame()

    def load_model(self):
        return YOLO('yolo11n.pt')

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret and self.running:
            # results = self.model.predict(source=frame, conf=0.01)
            results = self.model.track(source=frame, conf=0.01, persist=True)


            results2 = []
            for r in results:
                # print(r.boxes.xywh, r.boxes.cls, r.boxes.id, r.boxes.conf)
                # for i in range(len(r.boxes.xywh)):  # Iterate over all detected boxes
                    # results2.append({
                    #     "xywh": r.boxes.xywh[i].tolist(),  # Convert tensor to list
                        # "cls": int(r.boxes.cls[i].item()),  # Convert single-value tensor to int
                        # "id": int(r.boxes.id[i].item())  # Convert single-value tensor to int
                        # "conf": float(r.boxes.conf[i].item())  # Convert single-value tensor to float
                    # })
                # print(r.boxes.xywh[0], r.boxes.cls[0], r.boxes.id[0], r.boxes.conf[0])
                # for res in results2[:5]:  # Print only the first 5 to check
                #     print(res)
                frame = r.plot(labels=True)
            self.tracker.track(results2)
            # try:
            #     locations = tracking(results2, locations)
            # except NameError:
            #     locations = tracking(results2, None)
            #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # tracking(results2, )
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

    # def tracking(self, results):
    #     if self.locations == []:
    #         self.locations = results
    #     else:
    #         print(self.locations)




if __name__ == "__main__":
    root = tk.Tk()
    app = SwimmerDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
