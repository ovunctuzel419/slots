import os
from typing import Union, List

from attrs import define

from utils.paths import resource_path


@define
class SlotsGame:
    name: str
    video_folder_path: str
    dataset_folder_path: str
    model_path: str
    rows: int
    cols: int
    bets: List[int] = [20, 25, 40, 50, 100, 200]

    def get_video_filepaths(self) -> Union[List[str], str]:
        if os.path.isdir(self.video_folder_path):
            video_files = os.listdir(self.video_folder_path)
            return [os.path.join(self.video_folder_path, video_file) for video_file in sorted(video_files)]
        else:
            return self.video_folder_path

    def get_csv_filepath(self) -> str:
        return resource_path(f"extracts/{self.name}.csv")


DEMO = SlotsGame(name='DEMO',
                 video_folder_path=resource_path('media/Demo'),
                 dataset_folder_path=resource_path('dataset/GX010010.MP4'),
                 model_path=resource_path('models/Fruit.pth'),
                 rows=3,
                 cols=5)

BLAZINGHOT7 = SlotsGame(name='BLAZINGHOT7',
                        video_folder_path='../videos/BlazingHot7.mp4',
                        dataset_folder_path=resource_path('dataset/BlazingHot7.mp4'),
                        model_path=resource_path('models/BlazingHot7.pth'),
                        rows=3,
                        cols=5)

MUMMY = SlotsGame(name='MUMMY',
                  video_folder_path='../videos/Mummy.mp4',
                  dataset_folder_path=resource_path('dataset/mummy.mp4'),
                  model_path=resource_path('models/Mummy.pth'),
                  rows=3,
                  cols=5)

REELS = SlotsGame(name='REELS',
                  video_folder_path='E:/Slots/reels.mp4',
                  dataset_folder_path=resource_path('dataset/reels.mp4'),
                  model_path=resource_path('models/Reels.pth'),
                  rows=3,
                  cols=5)

DISCO = SlotsGame(name='DISCO',
                  video_folder_path='E:/Slots/discoo.mp4',
                  dataset_folder_path=resource_path('dataset/Disco.mp4'),
                  model_path=resource_path('models/Disco.pth'),
                  rows=4,
                  cols=5)

DRAGON = SlotsGame(name='DRAGON',
                   video_folder_path='E:/Slots/dragon.mp4',
                   dataset_folder_path=resource_path('dataset/Dragon'),
                   model_path=resource_path('models/Dragon.pth'),
                   rows=4,
                   cols=5)

MAJESTIC = SlotsGame(name='MAJESTIC',
                     video_folder_path='E:/Slots/majestic7 missing.mp4',
                     dataset_folder_path=resource_path('dataset/Majestic7 HD.mp4'),
                     model_path=resource_path('models/Majestic.pth'),
                     rows=3,
                     cols=3)

MEGAREELS = SlotsGame(name='MEGAREELS',
                      video_folder_path='../videos/Megareels.mp4',
                      dataset_folder_path=resource_path('dataset/MegareelsNew.mp4'),
                      model_path=resource_path('models/Megareels.pth'),
                      rows=3,
                      cols=3)

BELLS = SlotsGame(name='BELLS',
                  video_folder_path='E:/Slots/bells.mp4',
                  dataset_folder_path=resource_path('dataset/bells.mp4'),
                  model_path=resource_path('models/Bells.pth'),
                  rows=3,
                  cols=5)

GANGSTER = SlotsGame(name='GANGSTER',
                     video_folder_path='../videos/Gangster.mp4',
                     dataset_folder_path=resource_path('dataset/Gangster HD.mp4'),
                     model_path=resource_path('models/Gangster.pth'),
                     rows=3,
                     cols=5)

BLAZINGFRUITS = SlotsGame(name='BLAZINGFRUITS',
                          video_folder_path='../videos/BlazingFruits.mp4',
                          dataset_folder_path=resource_path('dataset/BlazingFruits.mp4'),
                          model_path=resource_path('models/BlazingFruits.pth'),
                          rows=3,
                          cols=5)

CRYSTALTREASURE = SlotsGame(name='CRYSTALTREASURE',
                            video_folder_path='../videos/CrystalTreasure.mp4',
                            dataset_folder_path=resource_path('dataset/crystaltreasure.mp4'),
                            model_path=resource_path('models/crystaltreasure.pth'),
                            rows=3,
                            cols=5)

REELSDELUXE = SlotsGame(name='REELSDELUXE',
                        video_folder_path='../videos/CrystalReelsDeluxe.mp4',
                        dataset_folder_path=resource_path('dataset/CrystalReelsDeluxe.mp4'),
                        model_path=resource_path('models/CrystalReelsDeluxe.pth'),
                        rows=3,
                        cols=5)

VULCAN = SlotsGame(name='VULCAN',
                   video_folder_path='E:/OneDrive/../videos/Vulcan.mp4',
                   dataset_folder_path=resource_path('dataset/Vulcan.mp4'),
                   model_path=resource_path('models/Vulcan.pth'),
                   rows=3,
                   cols=5)


ICEDFRUITS = SlotsGame(name='ICEDFRUITS',
                       video_folder_path='../videos/IcedFruits.mp4',
                       dataset_folder_path=resource_path('dataset/IcedFruits.mp4'),
                       model_path=resource_path('models/Ice.pth'),
                       rows=3,
                       cols=5)

WORM = SlotsGame(name='WORM',
                 video_folder_path='../videos/Worm.mp4',
                 dataset_folder_path=resource_path('dataset/Worm.mp4'),
                 model_path=resource_path('models/Worm.pth'),
                 rows=3,
                 cols=5)

HELLS = SlotsGame(name='HELLS',
                   video_folder_path='../videos/Hells.mp4',
                   dataset_folder_path=resource_path('dataset/Hells.mp4'),
                   model_path=resource_path('models/Hells.pth'),
                   rows=3,
                   cols=5)

POSEIDON = SlotsGame(name='POSEIDON',
                     video_folder_path='../videos/Poseidon.mp4',
                     dataset_folder_path=resource_path('dataset/Poseidon.mp4'),
                     model_path=resource_path('models/Poseidon.pth'),
                     rows=3,
                     cols=5)

ENERGY = SlotsGame(name='ENERGY',
                   video_folder_path='../videos/Energy.mp4',
                   dataset_folder_path=resource_path('dataset/Energy.mp4'),
                   model_path=resource_path('models/Energy.pth'),
                   rows=3,
                   cols=4)


available_games = [
    MUMMY,
    # BELLS,
    # MAJESTIC,
    BLAZINGFRUITS,
    MEGAREELS,
    BLAZINGHOT7,
    CRYSTALTREASURE,
    # REELS,
    REELSDELUXE,
    ICEDFRUITS,
    GANGSTER,
    # VULCAN,
    # DISCO,
    # DRAGON
    WORM,
    HELLS,
    POSEIDON,
    ENERGY
]



