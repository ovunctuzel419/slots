import os

from change_detection import ChangeDetector, ChangeDetectorAntiCorruption
from fixture.predefined_slots import DEMO, BLAZINGHOT7, MUMMY, REELS, DISCO, DRAGON, MAJESTIC, BELLS, GANGSTER, \
    BLAZINGFRUITS, MEGAREELS, REELSDELUXE, CRYSTALTREASURE, VULCAN, ICEDFRUITS, HELLS, WORM, POSEIDON, ENERGY
from frame_extractor import FrameExtractor
from grid_crop import GridCrop
from icon_extractor import IconExtractor
from rectification import SubframeRectifier
from subframe_finder import SubframeFinder


class FrameExtractorBuilder:
    @staticmethod
    def demo() -> FrameExtractor:
        game = DEMO
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=850, height=650, x_offset=120, y_offset=110),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier())
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetector(threshold=40),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=141, height=179, x_offset=78, y_offset=95)))
        return extractor

    @staticmethod
    def fruit() -> FrameExtractor:
        game = BLAZINGHOT7
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=350,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor


    @staticmethod
    def mummy() -> FrameExtractor:
        game = MUMMY
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=115, height=100, x_offset=35, y_offset=25, debug=False)))
        return extractor

    @staticmethod
    def reels() -> FrameExtractor:
        game = REELS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=480, height=340, x_offset=190, y_offset=50, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=110,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[100, 455, 810],
                                                                                segment_h=70,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=86, height=90, x_offset=35, y_offset=53, debug=False)))
        return extractor

    @staticmethod
    def disco() -> FrameExtractor:
        game = DISCO
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=480, height=340, x_offset=190, y_offset=50, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=83, height=70, x_offset=40, y_offset=60, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=125,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[110, 455, 810],
                                                                                segment_h=52,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def dragon() -> FrameExtractor:
        game = DRAGON
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=480, height=340, x_offset=190, y_offset=50, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=83, height=70, x_offset=40, y_offset=40, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=80,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[90, 435, 790],
                                                                                segment_h=52,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)

        return extractor

    @staticmethod
    def majestic() -> FrameExtractor:
        game = MAJESTIC
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=480, height=340, x_offset=190, y_offset=50, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=111, height=82, x_offset=90, y_offset=55, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=0,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[100, 455, 810],
                                                                                segment_h=57,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),

                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def megareels() -> FrameExtractor:
        game = MEGAREELS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[90, 430, 775],
                                                                                segment_h=75,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=175, height=96, x_offset=56, y_offset=32, debug=False)))
        return extractor

    @staticmethod
    def bells() -> FrameExtractor:
        game = BELLS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=480, height=340, x_offset=190, y_offset=50, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=255,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[100, 455, 810],
                                                                                segment_h=70,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=84, height=96, x_offset=35, y_offset=53, debug=False)))
        return extractor

    @staticmethod
    def gangster() -> FrameExtractor:
        game = GANGSTER
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=1000,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor

    @staticmethod
    def reelsdeluxe() -> FrameExtractor:
        game = REELSDELUXE
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor

    @staticmethod
    def crystaltreasure() -> FrameExtractor:
        game = CRYSTALTREASURE
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor

    @staticmethod
    def blazingfruits() -> FrameExtractor:
        game = BLAZINGFRUITS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor

    @staticmethod
    def vulcan() -> FrameExtractor:
        game = VULCAN
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=100, height=90, x_offset=72, y_offset=52, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=72,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def icedfruits() -> FrameExtractor:
        game = ICEDFRUITS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=420,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor


    @staticmethod
    def worm() -> FrameExtractor:
        game = WORM
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         hue_tolerance=5,
                                         saturation_tolerance=50,
                                         background_colors=[(0, 0, 0), (150, 40, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=420,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor


    @staticmethod
    def hells() -> FrameExtractor:
        game = HELLS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=333, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=420,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor


    @staticmethod
    def poseidon() -> FrameExtractor:
        game = POSEIDON
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=635, height=330, x_offset=20, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=107, height=100, x_offset=55, y_offset=25, debug=False)))
        return extractor


    @staticmethod
    def energy() -> FrameExtractor:
        game = ENERGY
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=630, height=330, x_offset=10, y_offset=65, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   start_frame=400,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[75, 415, 760],
                                                                                segment_h=80,
                                                                                icon_rows=game.rows,
                                                                                threshold=40,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=150, height=100, x_offset=25, y_offset=25, debug=False)))
        return extractor


extractor_map = {
    DEMO.name: FrameExtractorBuilder.demo(),
    BLAZINGHOT7.name: FrameExtractorBuilder.fruit(),
    MUMMY.name: FrameExtractorBuilder.mummy(),
    REELS.name: FrameExtractorBuilder.reels(),
    DISCO.name: FrameExtractorBuilder.disco(),
    DRAGON.name: FrameExtractorBuilder.dragon(),
    MAJESTIC.name: FrameExtractorBuilder.majestic(),
    MEGAREELS.name: FrameExtractorBuilder.megareels(),
    BELLS.name: FrameExtractorBuilder.bells(),
    GANGSTER.name: FrameExtractorBuilder.gangster(),
    BLAZINGFRUITS.name: FrameExtractorBuilder.blazingfruits(),
    REELSDELUXE.name: FrameExtractorBuilder.reelsdeluxe(),
    CRYSTALTREASURE.name: FrameExtractorBuilder.crystaltreasure(),
    VULCAN.name: FrameExtractorBuilder.vulcan(),
    ICEDFRUITS.name: FrameExtractorBuilder.icedfruits(),
    WORM.name: FrameExtractorBuilder.worm(),
    HELLS.name: FrameExtractorBuilder.hells(),
    POSEIDON.name: FrameExtractorBuilder.poseidon(),
    ENERGY.name: FrameExtractorBuilder.energy(),
}
