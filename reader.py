import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.cloud import vision
import pyttsx3
import time
import logging
import configparser

def exit_program():
    logging.info("Exiting the program...")
    sys.exit(0)

config = configparser.RawConfigParser()
config.read('config.ini')

logging.basicConfig(level = logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("reader.log"),
        logging.StreamHandler()
    ])

# Set up Google Vision API client
credentials_path = config.get("configuration","google_vision_credential_path")

if credentials_path and os.path.exists(credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
else:
    logging.error(f"a valid file for google_vision_credential_path property must be set at config.ini")
    logging.error(f"current google_vision_credential_path: {credentials_path}")
    exit_program()

client = vision.ImageAnnotatorClient()

# Folder to monitor
folder_to_monitor = config.get("configuration","folder_to_monitor")
if folder_to_monitor and not os.path.exists(folder_to_monitor):
    logging.error(f"a valid path for folder_to_monitor property must be set at config.ini")
    logging.error(f"current folder_to_monitor: {folder_to_monitor}")
    exit_program()

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory or not event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            logging.info(f"New screenshot detected: {event.src_path}")
            try:
                self.process_screenshot(event.src_path)
            except Exception as e: 
                logging.info(f"process_screenshot error: {event.src_path}")
                logging.info(e)

    def process_screenshot(self, file_path):
        time.sleep(0.2)
        with open(file_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            extracted_text = texts[0].description.replace('\n', ' ')
            logging.info(f"Extracted text: {extracted_text}")
            self.read_text(extracted_text)
        else:
            logging.info("No text detected.")

    def read_text(self, text):
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate',160) #default is 200
        tts_engine.say(text)
        tts_engine.runAndWait()

if __name__ == "__main__":
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ctrl-C pressed!")
        observer.stop()
    observer.join()