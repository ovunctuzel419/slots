import os

from attrs import define


@define
class SlotsGame:
    name: str
    video_folder_path: str
    dataset_folder_path: str
    model_path: str

    def get_video_filepaths(self):
        if os.path.isdir(self.video_folder_path):
            video_files = os.listdir(self.video_folder_path)
            return [os.path.join(self.video_folder_path, video_file) for video_file in sorted(video_files)]
        else:
            return self.video_folder_path


DEMO = SlotsGame(name='DEMO',
                 video_folder_path='../media/Demo',
                 dataset_folder_path='../dataset/GX010010.MP4',
                 model_path='../models/Fruit.pth')

FRUIT = SlotsGame(name='FRUIT',
                  video_folder_path='E:/SlotVideos/Fruit',
                  dataset_folder_path='../dataset/Fruit_augmented',
                  model_path='../models/Fruit.pth')

MUMMY = SlotsGame(name='MUMMY',
                  video_folder_path='E:/OneDrive/Mummy',
                  dataset_folder_path='../dataset/Mummy_augmented',
                  model_path='../models/Mummy.pth')

REELS = SlotsGame(name='REELS',
                  video_folder_path='E:/OneDrive/Reels',
                  dataset_folder_path='../dataset/Reels_augmented',
                  model_path='../models/Reels.pth')

DISCO = SlotsGame(name='DISCO',
                  video_folder_path='E:/OneDrive/Disco',
                  dataset_folder_path='../dataset/Disco_augmented',
                  model_path='../models/Disco.pth')

DRAGON = SlotsGame(name='DRAGON',
                   video_folder_path='E:/SlotVideos/Dragon',
                   dataset_folder_path='../dataset/Dragon_augmented',
                   model_path='../models/Dragon.pth')

MAJESTIC = SlotsGame(name='MAJESTIC',
                     video_folder_path='E:/OneDrive/videos/Majestic7 HD.mp4',
                     dataset_folder_path='../dataset/Majestic7 HD.mp4_augmented',
                     model_path='../models/Majestic.pth')

BELLS = SlotsGame(name='BELLS',
                  video_folder_path='E:/OneDrive/videos/bells hd.mp4',
                  dataset_folder_path='../dataset/bells hd.mp4_augmented',
                  model_path='../models/Bells.pth')

GANGSTER = SlotsGame(name='GANGSTER',
                     video_folder_path='E:/OneDrive/videos/Gangster HD.mp4',
                     dataset_folder_path='../dataset/Gangster HD.mp4_augmented',
                     model_path='../models/Gangster.pth')

BLAZINGFRUITS = SlotsGame(name='BLAZINGFRUITS',
                          video_folder_path='E:/OneDrive/videos/BlazingFruits.mp4',
                          dataset_folder_path='../dataset/BlazingFruits.mp4_augmented',
                          model_path='../models/BlazingFruits.pth')


available_games = [GANGSTER, MAJESTIC, BELLS, DRAGON]
