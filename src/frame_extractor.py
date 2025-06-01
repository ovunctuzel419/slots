import os
from typing import Optional, Generator, Union, List

import cv2
from attr import define

from change_detection import ChangeDetector, ChangeDetectorAntiCorruption
from icon_extractor import IconExtractor
from utils.custom_types import BGRImageArray
from subframe_finder import SubframeFinder


@define
class FrameExtractor:
    """ Extracts frames from a video (ignoring static frames), and splits grid components. """
    video_paths: Union[str, List[str]]
    subframe_finder: SubframeFinder
    icon_extractor: IconExtractor
    change_detector: Union[ChangeDetector, ChangeDetectorAntiCorruption] = ChangeDetector()
    _last_frame: Optional[BGRImageArray] = None

    def extract_frames(self) -> Generator[BGRImageArray, None, None]:
        video_paths = self.video_paths if isinstance(self.video_paths, list) else [self.video_paths]
        video_paths = sorted(video_paths)
        for path in video_paths:
            assert os.path.exists(path), f"Video path {path} does not exist"
        print("Processing", len(video_paths), "videos: ", str([str(p) + '\n' for p in video_paths]))

        for video_path in video_paths:
            cap = cv2.VideoCapture(video_path)
            # cap.set(cv2.CAP_PROP_POS_FRAMES, 400000)  # 223937

            while cap.isOpened():
                frame = self._get_next_frame_with_change(cap)
                if frame is None:
                    break
                subframes = self.subframe_finder.find_subframes(frame, video_filename=os.path.basename(video_path))
                for subframe in subframes:
                    yield subframe
            cap.release()

    def extract_icons(self) -> Generator[BGRImageArray, None, None]:
        for frame in self.extract_frames():
            icons = self.icon_extractor.extract_icons(frame)
            for icon in icons:
                yield icon

    def _get_next_frame_with_change(self, cap: cv2.VideoCapture) -> Optional[BGRImageArray]:
        has_change = False

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # The first frame is always provided
            if self._last_frame is None:
                self._last_frame = frame
                return frame

            if self._last_frame is not None:
                if self.change_detector.has_change(frame, self._last_frame):
                    has_change = True
                elif has_change:
                    self._last_frame = frame
                    return frame
            self._last_frame = frame
        return None

