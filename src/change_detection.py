from typing import List

import attr
import cv2
import numpy as np
from attr import define

from grid_crop import GridCrop
from utils.custom_types import BGRImageArray


@define
class ChangeDetector:
    threshold: float = 7.5
    downsample_factor = 0.1
    percentile: float = 97.5
    debug: bool = False

    def has_change(self, frame1: BGRImageArray, frame2: BGRImageArray) -> bool:
        f = self.downsample_factor
        frame1_downsampled = cv2.resize(frame1, (0, 0), fx=f, fy=f)
        frame2_downsampled = cv2.resize(frame2, (0, 0), fx=f, fy=f)
        frame1_downsampled = cv2.GaussianBlur(frame1_downsampled, (5, 5), 0)
        frame2_downsampled = cv2.GaussianBlur(frame2_downsampled, (5, 5), 0)
        absdiff = cv2.absdiff(frame1_downsampled, frame2_downsampled)

        diff_score = np.percentile(np.max(absdiff, axis=2), self.percentile)

        if self.debug:
            viz = np.hstack((frame1_downsampled, frame2_downsampled, absdiff))
            viz = cv2.putText(viz, f'absdiff: {diff_score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow('Change Detector', viz)
            cv2.imshow('Change Detector 2', np.hstack((frame1, frame2)))
            cv2.waitKey()

        return diff_score > self.threshold


@define
class ChangeDetectorAntiCorruption:
    segment_ys: List[int]
    segment_h: int
    icon_rows: int
    divide_each_segment: bool = False
    threshold: float = 7.5
    downsample_factor: float = 0.1
    percentile: float = 97.5
    stability_threshold: int = 4
    debug: bool = False
    _stability_counter: int = 0
    _change_list: List[bool] = attr.field(init=False)

    def has_change(self, frame1: BGRImageArray, frame2: BGRImageArray) -> bool:
        f = self.downsample_factor
        segment_h = int(self.segment_h * f)
        segment_ys = []
        for y in self.segment_ys:
            for i in range(self.icon_rows):
                base_y = int(y * f + i * segment_h)
                if self.divide_each_segment:
                    segment_ys.append(base_y)
                    segment_ys.append(base_y + segment_h // 2)
                else:
                    segment_ys.append(base_y)

        segment_h = segment_h // 2 if self.divide_each_segment else segment_h

        f1 = cv2.GaussianBlur(cv2.resize(frame1, (0, 0), fx=f, fy=f), (5, 5), 0)
        f2 = cv2.GaussianBlur(cv2.resize(frame2, (0, 0), fx=f, fy=f), (5, 5), 0)
        absdiff = cv2.absdiff(f1, f2)

        if not hasattr(self, "_change_list") or len(self._change_list) != len(segment_ys):
            self._change_list = [False] * len(segment_ys)

        diffscores = []
        for i, y_start in enumerate(segment_ys):
            y_end = y_start + segment_h
            seg = absdiff[y_start:y_end]
            if seg.size == 0:
                diffscores.append(0.0)
                continue
            score = np.percentile(np.max(seg, axis=2), self.percentile)
            diffscores.append(score)
            if score > self.threshold:
                self._change_list[i] = True

        all_changed = all(self._change_list)

        if self.debug:
            for y in segment_ys:
                cv2.putText(f1, f'{y}', (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.line(f1, (0, y), (absdiff.shape[1], y), (255, 255, 255), 1)

            viz = np.hstack((f1, f2, absdiff))
            for i, d in enumerate(diffscores):
                color = (0, 255, 0) if self._change_list[i] else (255, 255, 255)
                cv2.putText(viz, f'{min(99, int(d))}', (30 + 30 * i, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            if all_changed:
                color = (0, 255, 0)
                if self._stability_counter + 1 >= self.stability_threshold:
                    color = (0, 0, 255)
                viz = cv2.copyMakeBorder(viz, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=color)
            cv2.imshow('Debug Anti Corruption Lines', f1)
            cv2.imshow('Change Detector', viz)
            cv2.waitKey()

        if all_changed:
            self._stability_counter += 1
            if self._stability_counter >= self.stability_threshold:
                self._change_list = [False] * len(segment_ys)
                self._stability_counter = 0
                return True

        return False
