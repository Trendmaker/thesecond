"""Video loading and frame extraction utilities."""

import cv2
from typing import Optional, Tuple


class VideoManager:
    """Simple wrapper around cv2.VideoCapture."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open video file: {path}")

    def frame_count(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def fps(self) -> float:
        return float(self.cap.get(cv2.CAP_PROP_FPS))

    def get_frame(self, index: int) -> Optional[Tuple[bool, any]]:
        """Return frame at given index (0-based)."""
        if index < 0 or index >= self.frame_count():
            return None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self.cap.read()
        if not ret:
            return None
        return ret, frame

    def release(self) -> None:
        self.cap.release()
