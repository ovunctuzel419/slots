from typing import Optional

import cv2
import os
import numpy as np

from utils.paths import resource_path


templates = {}
path = os.path.join(resource_path('digits'))

for i in range(10):
    img = cv2.imread(f'{path}/{i}.png', cv2.IMREAD_GRAYSCALE)
    templates[i] = img


def read_frame_index(cropped_image: np.ndarray) -> Optional[int]:
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # 1. Boost Contrast: Ensures noise doesn't dim the digit intensity
    # This stretches the histograms so white is TRULY white
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    all_detections = []
    threshold = 0.75

    for digit, temp in templates.items():
        w, h = temp.shape[::-1]
        res = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)

        # Find all matches above threshold
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            score = res[pt[1], pt[0]]
            # Store (x_start, x_end, score, digit)
            all_detections.append({
                'x1': pt[0],
                'x2': pt[0] + w,
                'score': score,
                'digit': str(digit)
            })

    # 2. Sort by score so we keep the BEST matches first
    all_detections.sort(key=lambda x: x['score'], reverse=True)

    # 3. Non-Maximum Suppression (Keep highest score, discard overlapping boxes)
    final_hits = []
    used_pixels = np.zeros(gray.shape[1], dtype=bool)

    for det in all_detections:
        # If the center of this digit hasn't been "claimed" by a better match
        center_x = (det['x1'] + det['x2']) // 2
        if not used_pixels[center_x]:
            final_hits.append((det['x1'], det['digit']))
            # Mark the width of this digit as "occupied"
            used_pixels[det['x1']:det['x2']] = True

    # 4. Final Sort by X to read left-to-right
    final_hits.sort(key=lambda x: x[0])
    final_hits_str = "".join([h[1] for h in final_hits])
    try:
        return int(final_hits_str)
    except ValueError:
        return None