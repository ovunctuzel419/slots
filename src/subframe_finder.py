from typing import List, Tuple, Optional

import cv2
import numpy as np
from attr import define

from grid_crop import GridCrop
from rectification import SubframeRectifier
from utils.custom_types import BGRImageArray, BGRColor


@define
class SubframeFinder:
    """ A class for finding subframes in a frame and rectifying them. """
    grid_crop: GridCrop
    background_colors: List[BGRColor]
    rectifier: Optional[SubframeRectifier] = None
    hue_tolerance: int = 10
    saturation_tolerance: int = 100
    value_tolerance: int = 150
    debug: bool = False

    def find_subframes(self, frame: BGRImageArray, video_filename: Optional[str] = None) -> List[BGRImageArray]:
        heuristic_cropped_subframes = self.grid_crop.crop(frame)
        bg_removed_subframes = heuristic_cropped_subframes.copy()
        for i, frame in enumerate(bg_removed_subframes):
            for bg_color in self.background_colors:
                bg_removed_subframes[i] = self._remove_background(frame, bg_color)

        if self.rectifier is None:
            return bg_removed_subframes
        clean_subframes = [self.rectifier.rectify(mask=bg_removed_subframes[i],
                                                  image=heuristic_cropped_subframes[i],
                                                  cache_hash=f'{video_filename}_{i}') for i in range(len(heuristic_cropped_subframes))]

        return clean_subframes

    def _remove_background(self, subframe: BGRImageArray, bg_color: BGRColor) -> BGRImageArray:
        # Convert to HSV for better color tolerance
        hsv = cv2.cvtColor(subframe, cv2.COLOR_BGR2HSV)
        target_hsv = cv2.cvtColor(np.uint8([[bg_color]]), cv2.COLOR_BGR2HSV)[0][0]

        # Define a range around the target color
        lower = np.clip(target_hsv - [self.hue_tolerance, self.saturation_tolerance, self.value_tolerance], 0, 255)
        upper = np.clip(target_hsv + [self.hue_tolerance, self.saturation_tolerance, self.value_tolerance], 0, 255)

        # Create mask and remove background
        mask = cv2.inRange(hsv, lower, upper)
        mask_inv = cv2.bitwise_not(mask)
        foreground = cv2.bitwise_and(subframe, subframe, mask=mask_inv)

        if self.debug:
            viz = subframe.copy()
            cv2.putText(viz, f'target color: {bg_color}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 16)
            cv2.putText(viz, f'target color: {bg_color}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 10)
            cv2.putText(viz, f'target color: {bg_color}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, bg_color, 3)
            cv2.imshow('background_removal', cv2.resize(np.hstack((viz, foreground)), (0, 0), fx=0.25, fy=0.25))
            cv2.waitKey()

        return foreground





