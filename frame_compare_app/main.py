"""Entry point for the frame comparison application."""

import sys

from PyQt5 import QtWidgets

from modules.video_manager import VideoManager
from modules.gui import FrameCompareWindow


def main(path_a: str, path_b: str) -> None:
    video_a = VideoManager(path_a)
    video_b = VideoManager(path_b)
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
