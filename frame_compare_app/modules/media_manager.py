"""Load video files or image sequences as a uniform frame source."""

from __future__ import annotations

import os
from typing import List, Optional, Tuple

import cv2


_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}


class MediaSource:
    """Represents a sequence of frames from a video or folder of images."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.is_video = False
        self._cap: Optional[cv2.VideoCapture] = None
        self._frames: List[str] = []

        if os.path.isdir(path):
            self._init_from_folder(path)
        else:
            self._init_from_video(path)

    # ------------------------------------------------------------------
    def _init_from_video(self, path: str) -> None:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {path}")
        self.is_video = True
        self._cap = cap

    def _init_from_folder(self, folder: str) -> None:
        files = [
            os.path.join(folder, f)
            for f in sorted(os.listdir(folder))
            if os.path.splitext(f)[1].lower() in _IMAGE_EXTS
        ]
        if not files:
            raise IOError(f"No image files found in folder: {folder}")
        self._frames = files

    # ------------------------------------------------------------------
    def frame_count(self) -> int:
        if self.is_video and self._cap:
            return int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return len(self._frames)

    def fps(self) -> float:
        if self.is_video and self._cap:
            return float(self._cap.get(cv2.CAP_PROP_FPS))
        return 0.0

    def get_frame(self, index: int) -> Optional[Tuple[bool, any]]:
        """Return frame at given index (0-based)."""
        if index < 0 or index >= self.frame_count():
            return None

        if self.is_video and self._cap:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = self._cap.read()
            if not ret:
                return None
            return ret, frame

        img_path = self._frames[index]
        frame = cv2.imread(img_path)
        if frame is None:
            return None
        return True, frame

    def release(self) -> None:
        if self._cap:
            self._cap.release()
