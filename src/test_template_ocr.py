import os
import time
import unittest
import cv2

from template_ocr import read_frame_index

TEST_PATH = 'assets/ocr'


class TestOCR(unittest.TestCase):
    def test_ocr_accuracy(self):
        test_files = [f for f in os.listdir(TEST_PATH) if f.endswith(('.png', '.jpg'))]
        total = len(test_files)
        true_positives = 0
        total_time = 0

        print(f"Starting test on {total} samples...\n" + "-" * 30)

        for filename in test_files:
            # Ground Truth is the filename without extension
            gt_label = os.path.splitext(filename)[0]

            img = cv2.imread(os.path.join(TEST_PATH, filename))

            start_time = time.perf_counter()
            prediction = read_frame_index(img)
            end_time = time.perf_counter()

            latency_ms = (end_time - start_time) * 1000
            total_time += latency_ms

            if prediction == gt_label:
                true_positives += 1
                status = "PASS"
            else:
                status = f"FAIL (Got: {prediction})"

            print(f"File: {filename:15} | {status} | {latency_ms:.2f}ms")

        accuracy = (true_positives / total) * 100 if total > 0 else 0
        avg_speed = total_time / total if total > 0 else 0

        print("-" * 30)
        print(f"Accuracy: {accuracy:.2f}% ({true_positives}/{total})")
        print(f"Average Speed: {avg_speed:.2f}ms per frame")

