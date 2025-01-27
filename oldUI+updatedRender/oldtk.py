import tkinter as tk
from PIL import Image, ImageTk
import cv2


def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_image = ImageTk.PhotoImage(resized_image)
    video_label.config(image=new_image)
    video_label.image = new_image


def show_alert(message):
    output_label.config(text=message, fg="red")


def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (video_frame.winfo_width(), video_frame.winfo_height()))
        img = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=img)
        video_label.image = img
    video_label.after(10, update_video)


# Create the root window
root = tk.Tk()
root.title("Wireframe")
root.geometry("960x540")
root.configure(bg="#000000")

# Define Frames
tools_frame = tk.Frame(root, bg="#FFFFFF", highlightthickness=2, highlightbackground="#4b4b4b")
video_frame = tk.Frame(root, bg="#FFFFFF", highlightthickness=2, highlightbackground="#4b4b4b")
video_options_frame = tk.Frame(root, bg="#FFFFFF", highlightthickness=2, highlightbackground="#4b4b4b")
output_frame = tk.Frame(root, bg="#FFFFFF", highlightthickness=2, highlightbackground="#4b4b4b")

# Layout Configuration
tools_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
video_frame.grid(row=0, column=1, sticky="nsew")
video_options_frame.grid(row=1, column=1, sticky="nsew")
output_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

root.grid_rowconfigure(0, weight=10)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=25)

# Add tools to the tools_frame
tool_buttons = [
    ("🖉", "Edit"), ("🔍", "Search"), ("⚙", "Settings"), ("✖", "Close"),
    ("📁", "Open File"), ("💾", "Save"), ("⏳", "Loading"), ("🔄", "Refresh"),
    ("🖼", "Image"), ("📤", "Upload"), ("📥", "Download"), ("🔑", "Key"),
    ("🛠", "Tools"), ("📊", "Stats"),
]

for i, (symbol, tooltip) in enumerate(tool_buttons):
    btn = tk.Button(tools_frame, text=symbol, font=("Arial", 14), bg="#f0f0f0", relief="raised")
    btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

# Initialize video capture
cap = cv2.VideoCapture("/home/user/Downloads/midBondi_20241204_033001.mp4")  # Use 0 for webcam, or provide a file path

video_label = tk.Label(video_frame, bg="#FFFFFF")
video_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Start video update loop
update_video()

# Add sliders to video_options_frame
video_options = [
    ("Brightness", 0, 100),
    ("Contrast", 0, 100),
    ("Saturation", 0, 100),
    ("Sharpness", 0, 100),
]

for i, (label, min_val, max_val) in enumerate(video_options):
    tk.Label(video_options_frame, text=label, bg="#FFFFFF", font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=5, pady=5)
    tk.Scale(
        video_options_frame,
        from_=min_val,
        to=max_val,
        orient="horizontal",
        bg="#f0f0f0",
        highlightthickness=0
    ).grid(row=i, column=1, sticky="ew", padx=10)

camera_label = tk.Label(video_options_frame, text="Select Camera:", bg="#FFFFFF", font=("Arial", 10))
camera_label.grid(row=0, column=2, sticky="w", padx=10)

camera_selection = tk.StringVar(value="South Camera")

cameras = ["North Camera", "South Camera", "Mid Camera", "Ramp Camera"]
for i, camera in enumerate(cameras):
    tk.Radiobutton(
        video_options_frame,
        text=camera,
        variable=camera_selection,
        value=camera,
        bg="#FFFFFF",
        font=("Arial", 10),
        anchor="w"
    ).grid(row=1 + i, column=2, sticky="w", padx=10)

video_options_frame.grid_columnconfigure(1, weight=1)
video_options_frame.grid_columnconfigure(2, weight=0)

output_label = tk.Label(output_frame, text="", bg="#FFFFFF", font=("Arial", 14))
output_label.pack(expand=True, fill="both")

root.after(2000, lambda: show_alert("Alert: Person beyond limit!"))

root.mainloop()

cap.release()
cv2.destroyAllWindows()