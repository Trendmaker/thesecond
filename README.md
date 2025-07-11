# Eye Tracking with Ebook Launch

This repository contains a Python script `eye_reader.py` that opens an ebook file using your system's default viewer and starts real-time face and eye tracking with OpenCV. It can optionally record the camera feed to a video file while you are reading.

## Requirements

- Python 3
- OpenCV (`opencv-python` package)
- Haar cascade XML files (`haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`) placed in the same directory as the script.

## Usage

1. Place your ebook (e.g., `your_ebook.pdf`) in this directory and adjust the `ebook_path` variable in `eye_reader.py`.
2. Run the script:
   ```bash
   python eye_reader.py
   ```
3. A window will display the eye tracking feed. Press `q` to stop recording and close the window.

If `output_video` is provided, the script saves a recording of the camera feed to an AVI file with a timestamped name.
