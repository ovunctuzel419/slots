import os
from typing import Union, List

from attrs import define


@define
class SlotsGame:
    name: str
    video_folder_path: str
    dataset_folder_path: str
    model_path: str
    rows: int
    cols: int

    def get_video_filepaths(self) -> Union[List[str], str]:
        if os.path.isdir(self.video_folder_path):
            video_files = os.listdir(self.video_folder_path)
            return [os.path.join(self.video_folder_path, video_file) for video_file in sorted(video_files)]
        else:
            return self.video_folder_path

    def get_csv_filepath(self) -> str:
        return f"{self.name}.csv"


DEMO = SlotsGame(name='DEMO',
                 video_folder_path='../media/Demo',
                 dataset_folder_path='../dataset/GX010010.MP4',
                 model_path='../models/Fruit.pth',
                 rows=3,
                 cols=5)

FRUIT = SlotsGame(name='FRUIT',
                  video_folder_path='E:/SlotVideos/Fruit',
                  dataset_folder_path='../dataset/Fruit',
                  model_path='../models/Fruit.pth',
                  rows=3,
                  cols=5)

MUMMY = SlotsGame(name='MUMMY',
                  video_folder_path='E:/OneDrive/Mummy',
                  dataset_folder_path='../dataset/Mummy',
                  model_path='../models/Mummy.pth',
                  rows=3,
                  cols=5)

REELS = SlotsGame(name='REELS',
                  video_folder_path='E:/OneDrive/Reels',
                  dataset_folder_path='../dataset/Reels',
                  model_path='../models/Reels.pth',
                  rows=3,
                  cols=5)

DISCO = SlotsGame(name='DISCO',
                  video_folder_path='E:/OneDrive/videos/Disco.mp4',
                  dataset_folder_path='../dataset/Disco.mp4',
                  model_path='../models/Disco.pth',
                  rows=4,
                  cols=5)

DRAGON = SlotsGame(name='DRAGON',
                   video_folder_path='E:/SlotVideos/Dragon',
                   dataset_folder_path='../dataset/Dragon',
                   model_path='../models/Dragon.pth',
                   rows=4,
                   cols=5)

MAJESTIC = SlotsGame(name='MAJESTIC',
                     video_folder_path='E:/OneDrive/videos/Majestic7 HD.mp4',
                     dataset_folder_path='../dataset/Majestic7 HD.mp4',
                     model_path='../models/Majestic.pth',
                     rows=3,
                     cols=3)

MEGAREELS = SlotsGame(name='MEGAREELS',
                      video_folder_path='E:/OneDrive/videos/Megareels.mp4',
                      dataset_folder_path='../dataset/Megareels.mp4',
                      model_path='../models/Megareels.pth',
                      rows=3,
                      cols=3)

BELLS = SlotsGame(name='BELLS',
                  video_folder_path='E:/OneDrive/videos/bells hd.mp4',
                  dataset_folder_path='../dataset/bells hd.mp4',
                  model_path='../models/Bells.pth',
                  rows=3,
                  cols=5)

GANGSTER = SlotsGame(name='GANGSTER',
                     video_folder_path='E:/OneDrive/videos/Gangster HD.mp4',
                     dataset_folder_path='../dataset/Gangster HD.mp4',
                     model_path='../models/Gangster.pth',
                     rows=3,
                     cols=5)

BLAZINGFRUITS = SlotsGame(name='BLAZINGFRUITS',
                          video_folder_path='E:/OneDrive/videos/BlazingFruits.mp4',
                          dataset_folder_path='../dataset/BlazingFruits.mp4',
                          model_path='../models/BlazingFruits.pth',
                          rows=3,
                          cols=5)

CRYSTALTREASURE = SlotsGame(name='CRYSTALTREASURE',
                            video_folder_path='E:/OneDrive/videos/CrystalTreasure.mp4',
                            dataset_folder_path='../dataset/CrystalTreasure.mp4',
                            model_path='../models/CrystalTreasure.pth',
                            rows=3,
                            cols=5)

REELSDELUXE = SlotsGame(name='REELSDELUXE',
                          video_folder_path='E:/OneDrive/videos/CrystalReelsDeluxe.mp4',
                          dataset_folder_path='../dataset/CrystalReelsDeluxe.mp4',
                          model_path='../models/CrystalReelsDeluxe.pth',
                          rows=3,
                          cols=5)

VULCAN = SlotsGame(name='VULCAN',
                   video_folder_path='E:/OneDrive/videos/Vulcan.mp4',
                   dataset_folder_path='../dataset/Vulcan.mp4',
                   model_path='../models/Vulcan.pth',
                   rows=3,
                   cols=5)


ICEDFRUITS = SlotsGame(name='ICEDFRUITS',
                   video_folder_path='E:/OneDrive/videos/Ice.mp4',
                   dataset_folder_path='../dataset/Ice.mp4',
                   model_path='../models/Ice.pth',
                   rows=3,
                   cols=5)


available_games = [GANGSTER, MAJESTIC, BELLS, DRAGON, BLAZINGFRUITS]
