# Copyright 2026 SpacemiT (Hangzhou) Technology Co. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
import numpy as np

from person_follow.person_follow_cv.agv_detection import AGVDetection


def make_detection_helper():
    detection = AGVDetection.__new__(AGVDetection)
    detection.nms_thresh = 0.45
    detection.input_size = (320, 320)
    return detection


def test_calculate_iou_returns_expected_values():
    detector = make_detection_helper()

    box = np.array([0, 0, 10, 10], dtype=np.float32)
    boxes = np.array(
        [
            [0, 0, 10, 10],
            [5, 5, 15, 15],
            [20, 20, 30, 30],
        ],
        dtype=np.float32,
    )

    ious = detector.calculate_iou(box, boxes)

    assert np.isclose(ious[0], 1.0)
    assert 0.0 < ious[1] < 1.0
    assert np.isclose(ious[2], 0.0)


def test_nms_filters_overlapping_detections_by_confidence():
    detector = make_detection_helper()

    dets = [
        [0.0, 0.0, 10.0, 10.0, 0.0, 0.9],
        [1.0, 1.0, 11.0, 11.0, 0.0, 0.8],
        [50.0, 50.0, 60.0, 60.0, 0.0, 0.7],
    ]

    result = detector.nms(dets)
    assert len(result) == 2

    boxes = [tuple(det[:4]) for det in result]
    assert (0.0, 0.0, 10.0, 10.0) in boxes
    assert (50.0, 50.0, 60.0, 60.0) in boxes


def test_preprocess_postprocess_round_trip_preserves_detection_shape():
    detector = make_detection_helper()
    image = np.zeros((240, 320, 3), dtype=np.uint8)

    tensor = detector.preprocess(image, detector.input_size)
    assert tensor.shape == (1, 3, 320, 320)

    output = np.zeros((1, 7, 2), dtype=np.float32)
    output[0, 0, 0] = 160.0
    output[0, 1, 0] = 120.0
    output[0, 2, 0] = 40.0
    output[0, 3, 0] = 40.0
    output[0, 4, 0] = 0.4
    output[0, 5, 0] = 0.1
    output[0, 6, 0] = 0.1

    results = detector.postprocess(
        image,
        output,
        anchors=2,
        offset=7,
        conf_threshold=0.3,
        input_size=detector.input_size,
    )

    assert len(results) == 1
    assert results[0][4] == 0
    assert results[0][5] > 0.3
