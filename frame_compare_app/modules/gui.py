"""GUI components and widgets for frame comparison application."""

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

from .video_manager import VideoManager


def frame_to_qimage(frame) -> QtGui.QImage:
    """Convert an OpenCV frame (BGR) to QImage."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    bytes_per_line = ch * w
    return QtGui.QImage(rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)


class FrameCompareWindow(QtWidgets.QMainWindow):
    """Main window to show frame comparisons."""

    def __init__(self, video_a: VideoManager, video_b: VideoManager) -> None:
        super().__init__()
        self.video_a = video_a
        self.video_b = video_b
        self.mode_scene = False  # False -> codec comparison, True -> scene comparison
        self.current_index = 0
        self._init_ui()
        self._update_slider_range()
        self.update_frames()

    # ------------------------------------------------------------------
    def _init_ui(self) -> None:
        self.setWindowTitle("Frame Compare")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)

        # Frame display labels
        label_layout = QtWidgets.QHBoxLayout()
        self.label_a = QtWidgets.QLabel("Video A")
        self.label_b = QtWidgets.QLabel("Video B")
        self.label_a.setAlignment(QtCore.Qt.AlignCenter)
        self.label_b.setAlignment(QtCore.Qt.AlignCenter)
        label_layout.addWidget(self.label_a)
        label_layout.addWidget(self.label_b)
        main_layout.addLayout(label_layout)

        # Controls
        controls = QtWidgets.QHBoxLayout()
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.on_slider_changed)
        self.frame_edit = QtWidgets.QLineEdit("0")
        self.frame_edit.setFixedWidth(60)
        self.frame_edit.returnPressed.connect(self.on_edit_return)
        self.mode_check = QtWidgets.QCheckBox("Scene compare (n / n+1)")
        self.mode_check.toggled.connect(self.on_mode_toggled)
        controls.addWidget(self.slider)
        controls.addWidget(self.frame_edit)
        controls.addWidget(self.mode_check)
        main_layout.addLayout(controls)

    # ------------------------------------------------------------------
    def _update_slider_range(self) -> None:
        if self.mode_scene:
            max_val = max(self.video_a.frame_count() - 2, 0)
        else:
            max_val = max(min(self.video_a.frame_count(), self.video_b.frame_count()) - 1, 0)
        self.slider.setMaximum(max_val)

    # ------------------------------------------------------------------
    def update_frames(self) -> None:
        index = self.current_index
        if self.mode_scene:
            frame1 = self.video_a.get_frame(index)
            frame2 = self.video_a.get_frame(index + 1)
        else:
            frame1 = self.video_a.get_frame(index)
            frame2 = self.video_b.get_frame(index)

        if frame1:
            img_a = frame_to_qimage(frame1[1])
            self.label_a.setPixmap(QtGui.QPixmap.fromImage(img_a))
        else:
            self.label_a.setText("-")

        if frame2:
            img_b = frame_to_qimage(frame2[1])
            self.label_b.setPixmap(QtGui.QPixmap.fromImage(img_b))
        else:
            self.label_b.setText("-")

        self.frame_edit.setText(str(index))
        if self.slider.value() != index:
            self.slider.setValue(index)

    # ------------------------------------------------------------------
    def on_slider_changed(self, value: int) -> None:
        self.current_index = value
        self.update_frames()

    def on_edit_return(self) -> None:
        try:
            value = int(self.frame_edit.text())
        except ValueError:
            return
        value = max(0, min(value, self.slider.maximum()))
        self.current_index = value
        self.update_frames()

    def on_mode_toggled(self, checked: bool) -> None:
        self.mode_scene = checked
        self._update_slider_range()
        self.current_index = min(self.current_index, self.slider.maximum())
        self.update_frames()

    # ------------------------------------------------------------------
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Left:
            self.current_index = max(0, self.current_index - 1)
            self.update_frames()
        elif event.key() == QtCore.Qt.Key_Right:
            self.current_index = min(self.slider.maximum(), self.current_index + 1)
            self.update_frames()
        else:
            super().keyPressEvent(event)
