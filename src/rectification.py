from typing import Tuple, Optional, Dict

import attr
from attrs import define
import cv2
import numpy as np

from utils.custom_types import BGRImageArray


@define
class SubframeRectifier:
    debug: bool = False
    _corner_cache: Dict = attr.field(init=False, factory=dict)

    def rectify(self, mask: BGRImageArray, image: BGRImageArray, cache_hash: Optional[str] = None) -> BGRImageArray:
        # Fit a quadrilateral to the largest contour, i.e. find corners
        cache_hit = False
        corners = None
        if cache_hash is not None:
            if cache_hash in self._corner_cache:
                corners = self._corner_cache[cache_hash]
                cache_hit = True
        if not cache_hit:
            # Find the largest contour
            contours, _ = cv2.findContours(cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            largest_contour = self._get_largest_valid_contour(mask, contours)
            corners = self._fit_quadrilateral(mask, largest_contour).astype(np.float32)
            self._corner_cache[cache_hash] = corners

        # Apply perspective transform to rectify image
        targets = np.float32([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])
        M = cv2.getPerspectiveTransform(corners, targets)
        output = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))

        if self.debug:
            cv2.imshow('rectified', np.hstack((image, output)))
            cv2.waitKey()

        return output

    def _get_largest_valid_contour(self, mask: np.ndarray, contours: np.ndarray) -> np.ndarray:
        # Find valid contours
        h, w = mask.shape[:2]
        pad_x = int(w * 0.001)
        pad_y = int(h * 0.001)

        valid_contours = []
        for contour in contours:
            x, y, cw, ch = cv2.boundingRect(contour)
            # if x > pad_x and y > pad_y and (x + cw) < (w - pad_x) and (y + ch) < (h - pad_y):
            #     valid_contours.append(contour)
            area = cw * ch
            if area < 0.975 * mask.shape[0] * mask.shape[1] and area > 0.40 * mask.shape[0] * mask.shape[1]:
                valid_contours.append(contour)

        if self.debug:
            viz = mask.copy()
            for contour in contours:
                cv2.drawContours(viz, [contour], 0, (0, 0, 255), 2)
            for contour in valid_contours:
                cv2.drawContours(viz, [contour], 0, (0, 255, 0), 2)
            cv2.imshow('mask', viz)
            cv2.waitKey()

        if not valid_contours:
            raise RuntimeError('No valid contours found (all touch padded edges).')

        largest_contour = max(valid_contours, key=cv2.contourArea)

        return largest_contour


    def _fit_quadrilateral(self, image: BGRImageArray, contour: np.ndarray, scale: float = 0.25) -> BGRImageArray:
        """ Fits a quadrilateral to the given contour and returns the four corners. """

        def score_line_by_overlap_fast(line_pt1: np.ndarray, line_pt2: np.ndarray, contour: np.ndarray, step: int = 4,
                                       dist_thresh: int = 1) -> float:
            line_vec = line_pt2 - line_pt1
            line_len = int(np.linalg.norm(line_vec))
            if line_len < 1:
                return float('inf')
            num_pts = max(line_len // step, 2)
            t_vals = np.linspace(0, 1, num_pts).reshape(-1, 1)
            points = (line_pt1 + t_vals * line_vec).astype(np.float32)

            error = 0.0
            for pt in points:
                dist = abs(cv2.pointPolygonTest(contour, tuple(pt), True))
                if dist > dist_thresh:
                    error += 1
            return error

        def find_best_line(y_range: np.ndarray,
                           angle_range: np.ndarray,
                           contour: np.ndarray,
                           shape: Tuple[int, int]) -> Tuple[np.ndarray, float]:
            min_error = float('inf')
            best_line = np.zeros((2, 2), dtype=int)
            for y_offset in y_range:
                for slope in angle_range:
                    pt1 = np.array([0, y_offset])
                    pt2 = np.array([shape[1], y_offset + shape[0] * np.tan(slope)])
                    line = np.array([pt1, pt2])
                    error = score_line_by_overlap_fast(line[0], line[1], contour)

                    if error < min_error:
                        min_error = error
                        best_line = line.astype(int)
            return best_line, min_error

        def find_best_vertical_line(x_range: np.ndarray, angle_range: np.ndarray, contour: np.ndarray,
                                    shape: Tuple[int, int]) -> Tuple[np.ndarray, float]:
            min_error = float('inf')
            best_line = np.zeros((2, 2), dtype=int)
            for x_offset in x_range:
                for slope in angle_range:
                    pt1 = np.array([x_offset, 0])
                    pt2 = np.array([x_offset + shape[0] * np.tan(slope), shape[0]])
                    line = np.array([pt1, pt2])
                    error = score_line_by_overlap_fast(line[0], line[1], contour)
                    if error < min_error:
                        min_error = error
                        best_line = line.astype(int)
            return best_line, min_error

        # --- Step 1: Downsample input ---
        small = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        small_contour = (contour * scale).astype(np.int32)
        h, w = small.shape[:2]

        # --- Step 2: Sweep parameters ---
        angle_range = np.linspace(-np.pi / 16, np.pi / 16, 32)
        top_y_range = np.linspace(0, h * 0.25, 20, dtype=int)
        bottom_y_range = np.linspace(h * 0.75, h, 20, dtype=int)
        left_x_range = np.linspace(0, w * 0.25, 20, dtype=int)
        right_x_range = np.linspace(w * 0.75, w, 20, dtype=int)

        # --- Step 3: Fit lines ---
        top_line, _ = find_best_line(top_y_range, angle_range, small_contour, (h, w))
        bottom_line, _ = find_best_line(bottom_y_range, angle_range, small_contour, (h, w))
        left_line, _ = find_best_vertical_line(left_x_range, angle_range, small_contour, (h, w))
        right_line, _ = find_best_vertical_line(right_x_range, angle_range, small_contour, (h, w))

        # --- Step 4: Upscale lines back ---
        def upscale_line(line: np.ndarray) -> np.ndarray:
            return (line / scale).astype(int)

        top_line = upscale_line(top_line)
        bottom_line = upscale_line(bottom_line)
        left_line = upscale_line(left_line)
        right_line = upscale_line(right_line)

        def intersect_lines(p1: np.ndarray, p2: np.ndarray, q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
            """Compute intersection of lines (p1→p2) and (q1→q2)"""
            A = np.array([
                [p2[0] - p1[0], q1[0] - q2[0]],
                [p2[1] - p1[1], q1[1] - q2[1]]
            ])
            b = np.array([q1[0] - p1[0], q1[1] - p1[1]])

            if np.linalg.matrix_rank(A) < 2:
                return None  # parallel or degenerate

            t, s = np.linalg.solve(A, b)
            intersection = p1 + t * (p2 - p1)
            return intersection.astype(int)

        top_right = intersect_lines(top_line[0], top_line[1], right_line[0], right_line[1])
        bottom_left = intersect_lines(bottom_line[0], bottom_line[1], left_line[0], left_line[1])
        bottom_right = intersect_lines(bottom_line[0], bottom_line[1], right_line[0], right_line[1])
        top_left = intersect_lines(top_line[0], top_line[1], left_line[0], left_line[1])

        corners = np.array([top_left, top_right, bottom_right, bottom_left])

        if self.debug:
            viz = image.copy()
            # Contour
            cv2.drawContours(viz, [contour], 0, (255, 255, 255), 2)

            # Lines
            cv2.line(viz, tuple(top_line[0]), tuple(top_line[1]), (0, 0, 255), 2)
            cv2.line(viz, tuple(bottom_line[0]), tuple(bottom_line[1]), (0, 0, 255), 2)
            cv2.line(viz, tuple(left_line[0]), tuple(left_line[1]), (0, 0, 255), 2)
            cv2.line(viz, tuple(right_line[0]), tuple(right_line[1]), (0, 0, 255), 2)

            # Corners
            cv2.circle(viz, tuple(top_right), 5, (0, 255, 0), -1)
            cv2.circle(viz, tuple(bottom_left), 5, (0, 255, 0), -1)
            cv2.circle(viz, tuple(bottom_right), 5, (0, 255, 0), -1)
            cv2.circle(viz, tuple(top_left), 5, (0, 255, 0), -1)

            cv2.imshow('lines', viz)
            cv2.waitKey(0)

        return corners
