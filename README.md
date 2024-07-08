# game-screen-text-capture-tts

## Project Description

The `game-screen-text-capture-tts` project captures screenshots, extracts text from the screenshots using Google Cloud Vision, and reads the extracted text aloud using a Text-to-Speech (TTS) engine. This can be particularly useful for gamers who want to quickly capture and hear on-screen text without having to read it manually.

## Features

- Capture screenshots using a specified hotkey.
- Crop and save screenshots to a monitored folder.
- Automatically detect new screenshots in the monitored folder.
- Extract text from the screenshots using Google Cloud Vision API.
- Read the extracted text aloud using a TTS engine.

## Installation

### Requirements

Make sure you have the following dependencies installed:

- Python 3.x
- Pillow
- pyautogui
- tkinter
- watchdog
- google-cloud-vision
- pyttsx3
- keyboard
- configparser

You can install these dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Configuration

1. **Google Cloud Vision**:
   - Set up Google Cloud Vision API and download your credentials file (`credentials.json`).
   - Place the `credentials.json` file in the project directory.

2. **Configuration File**:
   - Update the `config.ini` file with the appropriate paths:
     ```ini
     [configuration]
     folder_to_monitor=G:/Pictures/Screenshots
     google_vision_credential_path=credentials.json
     ```

## Usage

### Running the Application

1. **Start the Main Application**:
   - Run the `main.py` script to monitor the folder for new screenshots and process them:
     ```bash
     python main.py
     ```

### Keyboard Shortcuts

- **Capture Screenshot**: Press `Shift+Print Screen`, `click and hold left mouse button` to select the area of the screen to capture.
- **Exit Application**: Press `Ctrl+C` on terminal/console

### How It Works

1. **Capture Screenshot**:
   - The `cropper.py` script captures a screenshot and allows you to select a region to crop. The cropped image is then saved in the monitored folder specified in the `config.ini`.

2. **Monitor Folder**:
   - The `reader.py` script monitors the specified folder for new screenshots. When a new screenshot is detected, it uses the Google Cloud Vision API to extract text from the image.

3. **Text-to-Speech**:
   - The extracted text is read aloud using the `pyttsx3` TTS engine.

## File Descriptions

- **config.ini**: Configuration file specifying the folder to monitor and the path to Google Cloud Vision credentials.
- **cropper.py**: Script to capture and crop screenshots.
- **main.py**: Manages the execution of `reader.py` and `cropper.py` scripts
- **reader.py**: script to monitor the folder, process screenshots, and perform text-to-speech.
- **requirements.txt**: List of required Python packages.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.
