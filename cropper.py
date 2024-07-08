import pyautogui
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import os
import logging
import datetime
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')

logging.basicConfig(level = logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("cropper.log"),
        logging.StreamHandler()
    ])

# Global variables
mouse_start = None

# Save the cropped image to the monitored folder
folder_to_monitor = config.get("configuration","folder_to_monitor")

# Function to capture the screenshot
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

# Function to handle mouse events
def on_mouse_down(event):
    try:
        logging.info(f"record mouse start {event}")
        global mouse_start
        mouse_start = (event.x, event.y)
    except Exception:
        logging.error("Aborting")
        root.destroy()

def on_mouse_release(event):
    try:
        logging.info(f"record mouse release {event}")
        global mouse_start, screenshot_img

        mouse_end = (event.x, event.y)

        # Calculate rectangle coordinates
        x1, y1 = mouse_start
        x2, y2 = mouse_end
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)

        logging.info(f"crop screenshot ({left}, {top}, {right}, {bottom})")
        # Crop the screenshot
        cropped_img = screenshot_img.crop((left, top, right, bottom))

        if not os.path.exists(folder_to_monitor):
            os.makedirs(folder_to_monitor)
        filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        cropped_img.save(os.path.join(folder_to_monitor, f"{filename}.png"))
        logging.info(f"saved screenshot {filename}.png")
    except Exception:
        logging.error("Aborting")

    # Close the window
    root.destroy()

if __name__ == "__main__":
    try:
        logging.info("taking screenshot")
        global screenshot_img
        # Capture the screenshot
        screenshot_img = capture_screenshot()

        # Display the screenshot using tkinter
        root = tk.Tk()
        root.overrideredirect(True)  # Create a borderless window
        root.lift()
        root.wm_attributes("-topmost", True)
        
        root.geometry(f"{screenshot_img.width}x{screenshot_img.height}")

        # Convert screenshot to PhotoImage format
        screenshot_tk = ImageTk.PhotoImage(screenshot_img)

        # Create a canvas
        canvas = tk.Canvas(root, width=screenshot_img.width, height=screenshot_img.height)
        canvas.pack()

        # Draw the screenshot on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=screenshot_tk)

        # Bind mouse events
        canvas.bind("<ButtonPress-1>", on_mouse_down)
        canvas.bind("<ButtonRelease-1>", on_mouse_release)

        root.mainloop()
    except KeyboardInterrupt:
        print("Ctrl-C pressed!")
        sys.exit(0)