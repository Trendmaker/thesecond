"""Frame navigation utilities.

This module provides functionality to jump to specific frames in a video
using the :class:`VideoManager` wrapper. It keeps track of the current
frame index and exposes helper methods to move forward/backward or
retrieve arbitrary frames.
"""

from typing import Optional, Tuple

import cv2

from .video_manager import VideoManager


class FrameNavigator:
    """Manage random access to frames of a video file."""

    def __init__(self, path: str) -> None:
        self._video = VideoManager(path)
        self._current_index = 0

    @property
    def current_index(self) -> int:
        """Return the last successfully retrieved frame index."""
        return self._current_index

    def goto(self, index: int) -> Optional[Tuple[bool, any]]:
        """Retrieve frame at ``index`` and update ``current_index``.

        Parameters
        ----------
        index:
            Zero-based frame number to jump to.

        Returns
        -------
        Optional[Tuple[bool, any]]
            Tuple ``(ret, frame)`` from OpenCV or ``None`` if ``index`` is
            out of range or the frame could not be read.
        """
        frame = self._video.get_frame(index)
        if frame:
            self._current_index = index
        return frame

    def next(self) -> Optional[Tuple[bool, any]]:
        """Advance to the next frame."""
        return self.goto(self._current_index + 1)

    def prev(self) -> Optional[Tuple[bool, any]]:
        """Step back to the previous frame."""
        return self.goto(self._current_index - 1)

    def frame_count(self) -> int:
        return self._video.frame_count()

    def fps(self) -> float:
        return self._video.fps()

    def release(self) -> None:
        self._video.release()


def display_frame(frame: any, window_name: str = "Frame") -> None:
    """Display a frame using ``cv2.imshow``.

    This convenience function is provided mainly for manual testing and
    demonstrates how returned frames can be shown on screen.
    """
    if frame is not None:
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)
