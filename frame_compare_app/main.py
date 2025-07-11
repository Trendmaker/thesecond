"""Entry point for the frame comparison application."""

import sys

from PyQt5 import QtWidgets, QtGui
import cv2

from modules.video_manager import VideoManager
from modules.gui import FrameCompareWindow

from modules.media_manager import MediaSource


def frame_to_qimage(frame) -> QtGui.QImage:
    """Convert an OpenCV frame (BGR) to QImage."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    bytes_per_line = ch * w
    return QtGui.QImage(rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, video_a: MediaSource, video_b: MediaSource) -> None:
        super().__init__()
        self.video_a = video_a
        self.video_b = video_b
        self._init_ui()
        self.show_first_frames()

    def _init_ui(self) -> None:
        self.setWindowTitle("Frame Compare")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
        self.label_a = QtWidgets.QLabel("Video A")
        self.label_b = QtWidgets.QLabel("Video B")
        layout.addWidget(self.label_a)
        layout.addWidget(self.label_b)

    def show_first_frames(self) -> None:
        frame_a = self.video_a.get_frame(0)
        frame_b = self.video_b.get_frame(0)
        if frame_a:
            img_a = frame_to_qimage(frame_a[1])
            self.label_a.setPixmap(QtGui.QPixmap.fromImage(img_a))
        if frame_b:
            img_b = frame_to_qimage(frame_b[1])
            self.label_b.setPixmap(QtGui.QPixmap.fromImage(img_b))

def main(path_a: str, path_b: str) -> None:
    video_a = MediaSource(path_a)
    video_b = MediaSource(path_b)
    app = QtWidgets.QApplication(sys.argv)
    win = FrameCompareWindow(video_a, video_b)
    win.show()
    app.exec_()
    video_a.release()
    video_b.release()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <video1> <video2>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
