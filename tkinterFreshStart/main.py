import cv2
from ultralytics.models.yolo.model import YOLO
import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk
import pygame
from tracker import tracker
from alerts.always import Always
from alerts.moving import Moving
from alerts.velocity import velocity
from alerts.disappearing import Disappearing
# from realesrgan import RealESRGAN
import torch
from datetime import datetime

class SwimmerDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swimmer Detection")

        # Main frame to hold video and other widgets
        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Video frame inside the main frame
        self.video_frame = Frame(self.main_frame, width = 640, height = 480, relief=tk.SUNKEN)
        # width = 640, height = 480, bd=2
        # Tools frame on the left of the screen
        self.tools_frame = Frame(self.main_frame)
        self.video_label = Label(self.video_frame)
        self.video_label.grid(row=0, column=0, sticky="nsew")
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        # Layout config
        self.tools_frame.grid(row=0, column=0, columnspan=1, rowspan = 1, sticky="nsew")
        self.video_frame.grid(row=0, column=1, columnspan=9, sticky="nsew", padx=5, pady=5)

        # Add tools to the tools_frame
        tool_buttons = [
            ("⚙\nSettings", "Settings"), ("🔑", "Thresholds"), ("⚙", "Settings"), ("✖", "Close"),
            ("📁", "Open File"), ("💾", "Save"), ("⏳", "Loading"), ("🔄", "Refresh"),
            ("🖼\nVideo\nOptions", "Image")
        ]
        for i, (symbol, tooltip) in enumerate(tool_buttons):
            btn = tk.Button(self.tools_frame, text=symbol, font=("Arial", 8), bg="#f0f0f0", relief="raised")
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

            # ("📤", "Upload"), ("📥", "Download"), ("🔑", "Key"),
            # ("🛠", "Tools"), ("📊", "Stats"),

        # Placeholder for extra widgets (e.g., buttons, info labels)
        # self.streamOptionsFrame = Frame(self.main_frame)
        # self.streamOptionsFrame.grid(row=1, column=0)

        # tk.Label(self.streamOptionsFrame, text="brightness").grid(row=0, column=0)
        # tk.Scale(self.streamOptionsFrame, from_=0, to=100, orient="horizontal").grid(row=0, column=1)

        # Load model and start video capture
        self.model = self.loadModel()
        # self.upScaleModel = RealESRGAN(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        self.cap = cv2.VideoCapture(1)
        self.running = True
        self.sound = pygame.mixer.Sound(r"C:\Users\petro\Downloads\file_example_MP3_700KB.mp3")
        self.soundPlaying = False
        self.tracker = tracker()
        self.alerts = [Disappearing()]
        self.activeAlerts = []
        self.dismissedAlerts = []
        self.updateFrame()


    def loadModel(self):
        return YOLO('yolo11n.pt')

    def updateFrame(self):
        _, frame = self.cap.read()
        for i in self.alerts:
            tempAlerts = i.step(self.tracker.getLocations())
            if tempAlerts:
                self.alertManager(tempAlerts)
        # self.alertManager(self.activeAlerts)
                # self.playSound()
        # frame = self.upScaleModel.predict(frame)
        results = self.model.track(source=frame, conf=0.01, persist=True)
        # results = self.model.predict(frame, conf=0.1)
        frame = results[0].plot(labels=True)


        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        # print("Updating frame")
        self.tracker.track(results)
        self.tracker.saveLocations2File(True)
        self.root.after(10, self.updateFrame)


    def onClosing(self):
        self.cap.release()
        self.root.destroy()

    def playSound(self):
        if not self.soundPlaying:
            self.sound.play(-1)
            self.soundPlaying = True

    # dismissedAlertExists checks if there are any dismissed alerts in self.dismissedAlerts of a particular
    # objectId, type and that were dismissed with a number of seconds (timeThreshold)
    def dismissedAlertExists(self, objectID, type, timeThreshold):
        return any(disAlrt['objectID'] == objectID and
                   disAlrt['type'] == type and
                   (datetime.utcnow() - disAlrt['dismissedTime']).total_seconds() < timeThreshold for
                   disAlrt in self.dismissedAlerts)

    def alertManager(self, alerts):
        if not self.activeAlerts:
            for i in alerts:
                if not self.dismissedAlertExists(i['objectID'], i['type'] , 60):
                    self.activeAlerts = alerts

        else:
            for i in alerts:
                if not any(alrt['objectID'] == i['objectID'] and
                           alrt['type'] == i['type']
                           for alrt in self.activeAlerts):
                    if not self.dismissedAlertExists(i['objectID'], i['type'] , 60):
                        self.activeAlerts.append(i)

        for i in self.activeAlerts:
            if not i['displayed']:
                i['displayed'] = True
                i['active'] = True
                self.displayAlert(i)

    def dismissButton(self, alert, window):
        self.activeAlerts.remove(alert)
        alert['dismissedTime'] = datetime.utcnow()
        self.dismissedAlerts.append(alert)
        window.destroy()


    def displayAlert(self, alert):
        window = tk.Tk()
        window.title("Notification")

        message_label = tk.Label(window, text=str(alert['type'] + " " + str(alert['objectID'])), font=("Arial", 14), fg="red")
        message_label.pack(pady=20)

        track_button = tk.Button(window, text="Track")
        track_button.pack(side=tk.LEFT, padx=20, pady=10)

        dismiss_button = tk.Button(window, text="Dismiss", command=lambda : self.dismissButton(alert, window))
        dismiss_button.pack(side=tk.RIGHT, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    pygame.mixer.init()
    app = SwimmerDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.onClosing)
    root.mainloop()
