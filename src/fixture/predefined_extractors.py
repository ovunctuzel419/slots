import os

from change_detection import ChangeDetector, ChangeDetectorAntiCorruption
from fixture.predefined_slots import DEMO, BLAZINGHOT7, MUMMY, REELS, DISCO, DRAGON, MAJESTIC, BELLS, GANGSTER, BLAZINGFRUITS, \
    MEGAREELS, REELSDELUXE, CRYSTALTREASURE, VULCAN, ICEDFRUITS
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
                                   change_detector=ChangeDetector(threshold=7.5),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=141, height=179, x_offset=78, y_offset=95)))
        return extractor

    @staticmethod
    def fruit() -> FrameExtractor:
        game = BLAZINGHOT7
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=840, height=650, x_offset=85, y_offset=95, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetector(threshold=7.5, debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=141, height=179, x_offset=78, y_offset=95, debug=False)))
        return extractor

    @staticmethod
    def mummy() -> FrameExtractor:
        game = MUMMY
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=820, height=650, x_offset=95, y_offset=95, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetector(threshold=7.5, debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=142, height=176, x_offset=60, y_offset=100, debug=False)))
        return extractor

    @staticmethod
    def reels() -> FrameExtractor:
        game = REELS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=890, height=650, x_offset=40, y_offset=80, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetector(threshold=7.5, debug=False),
                                   icon_extractor=IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=160, height=176, x_offset=54, y_offset=100, debug=False)))
        return extractor

    @staticmethod
    def disco() -> FrameExtractor:
        game = DISCO
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=110, height=70, x_offset=40, y_offset=50, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[45, 385, 710],
                                                                                segment_h=52,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def dragon() -> FrameExtractor:
        game = DRAGON
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=110, height=70, x_offset=40, y_offset=30, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[25, 365, 690],
                                                                                segment_h=52,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def majestic() -> FrameExtractor:
        game = MAJESTIC
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=150, height=84, x_offset=100, y_offset=45, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[32, 370, 702],
                                                                                segment_h=64,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def megareels() -> FrameExtractor:
        game = MEGAREELS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=145, height=81, x_offset=110, y_offset=70, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[48, 388, 720],
                                                                                segment_h=64,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def bells() -> FrameExtractor:
        game = BELLS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=110, height=90, x_offset=40, y_offset=55, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=72,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def gangster() -> FrameExtractor:
        game = GANGSTER
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=104, height=90, x_offset=60, y_offset=55, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=72,
                                                                                icon_rows=3,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def reelsdeluxe() -> FrameExtractor:
        game = REELSDELUXE
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=108, height=90, x_offset=50, y_offset=52, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=65,
                                                                                icon_rows=3,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def crystaltreasure() -> FrameExtractor:
        game = CRYSTALTREASURE
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=106, height=85, x_offset=55, y_offset=55, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=65,
                                                                                icon_rows=3,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def blazingfruits() -> FrameExtractor:
        game = BLAZINGFRUITS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=115, height=90, x_offset=30, y_offset=50, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=72,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
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
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
        return extractor

    @staticmethod
    def icedfruits() -> FrameExtractor:
        game = ICEDFRUITS
        video_paths = game.get_video_filepaths()
        subframe_finder = SubframeFinder(grid_crop=GridCrop(rows=3, cols=3, width=620, height=325, x_offset=40, y_offset=0, debug=False),
                                         background_colors=[(0, 0, 0), (255, 0, 0)],
                                         rectifier=SubframeRectifier(debug=False), debug=False)
        icon_extractor = IconExtractor(grid_crop=GridCrop(rows=game.rows, cols=game.cols, width=102, height=90, x_offset=65, y_offset=52, debug=False))
        extractor = FrameExtractor(video_paths=video_paths,
                                   subframe_finder=subframe_finder,
                                   change_detector=ChangeDetectorAntiCorruption(segment_ys=[40, 378, 710],
                                                                                segment_h=72,
                                                                                icon_rows=game.rows,
                                                                                threshold=7.5,
                                                                                divide_each_segment=False,
                                                                                downsample_factor=0.25,
                                                                                debug=False),
                                   icon_extractor=icon_extractor)
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
}
