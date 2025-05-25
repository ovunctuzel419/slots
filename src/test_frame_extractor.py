import os

import cv2

from fixture.predefined_extractors import extractor_map
from fixture.predefined_slots import DEMO


if __name__ == '__main__':
    video_path = os.path.join('../media', DEMO)
    extractor = extractor_map[DEMO]

    for i, frame in enumerate(extractor.extract_frames()):
        frame_index = i + 1
        cv2.putText(frame, f'frame {frame_index}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        key = cv2.waitKey()
