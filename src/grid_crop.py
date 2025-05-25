from typing import List

import cv2
from attr import define

from utils.custom_types import BGRImageArray


@define
class GridCrop:
    rows: int
    cols: int
    width: int
    height: int
    x_offset: int
    y_offset: int
    debug: bool = False

    def crop(self, image: BGRImageArray) -> List[BGRImageArray]:
        viz = None
        if self.debug:
            viz = image.copy()

        cropped_images = []
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = self.x_offset + col * self.width
                y1 = self.y_offset + row * self.height
                x2 = x1 + self.width
                y2 = y1 + self.height
                cropped_images.append(image[y1:y2, x1:x2])

                if self.debug:
                    cv2.rectangle(viz, (x1, y1), (x2, y2), (255, 255, 0), 5)
        if self.debug:
            viz = cv2.resize(viz, (0, 0), fx=0.5, fy=0.5)
            cv2.imshow('debug', viz)
            cv2.waitKey()

        return cropped_images

