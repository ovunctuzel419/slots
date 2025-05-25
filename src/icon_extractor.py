from typing import List

from attrs import define

from grid_crop import GridCrop
from utils.custom_types import BGRImageArray


@define
class IconExtractor:
    grid_crop: GridCrop
    def extract_icons(self, image: BGRImageArray) -> List[BGRImageArray]:
        return self.grid_crop.crop(image)
