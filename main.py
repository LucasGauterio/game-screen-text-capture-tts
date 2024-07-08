import subprocess
import keyboard
import sys
import logging

logging.basicConfig(level = logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ])

print("type Ctrl+C to close the program")
print("type Shift+Print Screen to take a screenshot and select the area to be read")

# Path to the cropper script
cropper_script = 'cropper.py'

# Function to run the cropper script
def run_cropper():
    logging.info(f"run cropper.py")
    subprocess.run(['python', cropper_script])
    logging.info(f"exit cropper.py")

# Function to monitor key press
def monitor_key_press():
    while True:
        if keyboard.is_pressed('shift+print screen'):
            run_cropper()

# Start the reader script in a separate thread
def start_screenshot_reader():
    logging.info(f"python reader.py")
    subprocess.run(['python', 'reader.py'])
    logging.info(f"exit reader.py")

def exit_program():
    logging.info("Exiting the program...")
    sys.exit(0)

keyboard.add_hotkey("shift+print screen", lambda: run_cropper())

try:
    # Start the screenshot reader
    start_screenshot_reader()
except KeyboardInterrupt:
  logging.info("Ctrl-C pressed!")
  exit_program()