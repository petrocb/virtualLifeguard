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

        # Tools frame on the left of the screen
        self.tools_frame = Frame(self.main_frame)
        self.video_label = Label(self.video_frame)
        self.video_label.grid(row=0, column=0, sticky="nsew")
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        # Add tools to the tools_frame
        tool_buttons = [
            ("⚙\nSettings"), ("🛠\nThresholds"), ("🖼\nVideo\nOptions"), ("✖", "Close")
        ]
        for i, (symbol) in enumerate(tool_buttons):
            btn = tk.Button(self.tools_frame, text=symbol, font=("Arial", 8), bg="#f0f0f0", relief="raised")
            btn.grid(row=i, column=0, padx=2, pady=5, sticky="ew")

        # The information dashboard
        self.info_dash_frame = Frame(self.main_frame, height=200)
        self.info_dash_frame.grid_rowconfigure(0, weight=0)
        self.info_dash_label = Label(self.info_dash_frame, text="Information dashboard", font=("Arial", 12, "bold"))

        # Layout config
        self.tools_frame.grid(row=0, column=0, columnspan=1, rowspan = 2, sticky="nsew")
        self.video_frame.grid(row=0, column=1, columnspan=1, sticky="nsew", padx=5, pady=5)
        self.info_dash_frame.grid(row=1, column=0, columnspan=2, rowspan = 1, sticky="nsew")
        self.info_dash_label.grid(row=0, column=0, sticky="w")

        # Load model and start video capture
        self.model = self.loadModel()
        # self.upScaleModel = RealESRGAN(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.running = True
        self.sound = pygame.mixer.Sound(r"C:\Users\petro\Downloads\file_example_MP3_700KB.mp3")
        self.soundPlaying = False
        self.tracker = tracker()
        # the list of active alert classes
        # alert classes analyse tracker data and return alerts
        # Toogle self.labels on/off to show YOLOv11 labels on screen
        self.labels = True
        self.alerts = [Disappearing()]
        self.activeAlerts = []
        self.dismissedAlerts = []
        self.updateFrame()


    def loadModel(self):
        # use this for a larger model
        # return YOLO('yolo11n.pt')
        return YOLO('yolo11n.pt')

    def updateFrame(self):
        _, frame = self.cap.read()
        for i in self.alerts:
            tempAlerts = i.step(self.tracker.getLocations())
            if tempAlerts:
                self.alertManager(tempAlerts)
        results = self.model.track(source=frame, conf=0.01, persist=True)
        # results = self.model.predict(frame, conf=0.1)
        frame = results[0].plot(labels=self.labels)


        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = self.drawBoxes(img, self.activeAlerts)
        #
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        # print("Updating frame")
        self.tracker.track(results)
        self.tracker.saveLocations2File(False)
        self.root.after(10, self.updateFrame)
        # self.annotator = Annotator(frame, line_width=2)


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
                # self.displayAlert(i)
                self.updateInfoDash()

    def drawBoxes(self, img, alerts):
        for i in alerts:
            if i['showLastLocation'] == True:
                cords = {'x1' : int(i['x'] - (i['w']/2)),
                         'x2' : int(i['x'] + (i['w']/2)),
                         'y1' : int(i['y'] - (i['h']/2)),
                         'y2' : int(i['y'] + (i['h']/2))}
                # cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 0), 2)
                cv2.rectangle(img, (cords['x1'], cords['y1']), (cords['x2'], cords['y2']), (255, 0, 0), 2)
                cv2.putText(img, f"Org ID: {i['objectID']} Scr ID: {i['yoloIDs'][-1]}", (cords['x1'], cords['y1']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2 )
        return img


    def dismissButton(self, alert):
        self.activeAlerts.remove(alert)
        alert['dismissedTime'] = datetime.utcnow()
        self.dismissedAlerts.append(alert)
        self.updateInfoDash()


    def displayAlert(self, alert):
        # window = tk.Tk()
        # window.title("Notification")

        message_label = tk.Label(self.info_dash_frame, text=str(alert['type'] + " " + str(alert['objectID'])), font=("Arial", 14), fg="red")
        message_label.pack(pady=20)

        track_button = tk.Button(self.info_dash_frame, text="Track")
        track_button.pack(side=tk.LEFT, padx=20, pady=10)

        dismiss_button = tk.Button(self.info_dash_frame, text="Dismiss", command=lambda : self.dismissButton(alert, self.info_dash_frame))
        dismiss_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def showLastLocationOnScreen(self, alert):
        alert['showLastLocation'] = not alert['showLastLocation']
        self.updateInfoDash()

    def updateInfoDash(self):
        # First, clear the existing widgets in the info dashboard frame.
        for widget in self.info_dash_frame.winfo_children():
            widget.destroy()

        if self.activeAlerts:
            self.playSound()
            for alert in self.activeAlerts:
                # Create a frame for each alert.
                alert_frame = tk.Frame(self.info_dash_frame, borderwidth=1, relief="solid", padx=5, pady=5)
                alert_frame.pack(fill="x", padx=5, pady=2)

                # Display the alert information.
                if self.labels == True and alert['objectID'] != max(alert['yoloIDs']):
                    alert_text = f"Alert: {alert['type']} - Original ID: {alert['objectID']} with on screen ID of {alert['yoloIDs'][-1]}"
                else:
                    alert_text = f"Alert: {alert['type']} - ID: {alert['objectID']}"
                label = tk.Label(alert_frame, text=alert_text, font=("Arial", 12))
                label.pack(side="left", padx=10)
                if alert['showLastLocation'] == True:
                    text = "Remove Last Location"
                else:
                    text = "Show Last Location"
                # Add a Track button for future functionality.
                track_button = tk.Button(alert_frame, text=text,
                                         command=lambda a=alert: self.showLastLocationOnScreen(a))
                track_button.pack(side="left", padx=10)

                # Add a Dismiss button that calls a custom method.
                dismiss_button = tk.Button(alert_frame, text="Dismiss",
                                           command=lambda a=alert: self.dismissButton(a))
                dismiss_button.pack(side="left", padx=10)
        else:
            # If there are no active alerts, show a default message.
            no_alert_label = tk.Label(self.info_dash_frame, text="No active alerts", font=("Arial", 12))
            no_alert_label.pack(padx=10, pady=10)
            self.sound.stop()
            self.soundPlaying = False


if __name__ == "__main__":
    root = tk.Tk()
    pygame.mixer.init()
    app = SwimmerDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.onClosing)
    root.mainloop()
