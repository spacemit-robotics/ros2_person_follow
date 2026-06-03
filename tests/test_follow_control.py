# Copyright 2026 SpacemiT (Hangzhou) Technology Co. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
import threading
import queue
import numpy as np
import pytest

try:
    from sensor_msgs.msg import CompressedImage
except ImportError:
    pytest.skip('ROS2 sensor_msgs is unavailable', allow_module_level=True)

from person_follow.person_follow_node import FollowControl


class DummyLogger:
    def __init__(self):
        self.infos = []
        self.warns = []

    def info(self, message):
        self.infos.append(message)

    def warn(self, message):
        self.warns.append(message)


class DummyBridge:
    def __init__(self, image):
        self.image = image

    def imgmsg_to_cv2(self, msg, desired_encoding='bgr8'):
        return self.image


class DummyPublisher:
    def __init__(self):
        self.published = []

    def publish(self, msg):
        self.published.append(msg)


class DummyClock:
    def now(self):
        return self

    def to_msg(self):
        try:
            from builtin_interfaces.msg import Time

            return Time(sec=123, nanosec=0)
        except ImportError:
            class TimeMessage:
                def __init__(self):
                    self.sec = 123
                    self.nanosec = 0

            return TimeMessage()


class DummyRequest:
    def __init__(self, data):
        self.data = data


class DummyResponse:
    def __init__(self):
        self.success = None
        self.message = None


def make_follow_control():
    follow_control = FollowControl.__new__(FollowControl)
    follow_control.lock = threading.Lock()
    follow_control.ai_enabled = False
    follow_control.infer_queue = queue.Queue(maxsize=2)
    follow_control.img_queue = queue.Queue(maxsize=2)
    follow_control.bridge = DummyBridge(np.zeros((16, 16, 3), dtype=np.uint8))
    follow_control.velocity_publisher = DummyPublisher()
    follow_control.publisher_img = DummyPublisher()
    follow_control.get_clock = lambda: DummyClock()
    follow_control.get_logger = lambda: DummyLogger()
    return follow_control


def test_callback_toggles_follow_state_and_returns_success_message():
    follow_control = make_follow_control()

    request = DummyRequest(True)
    response = DummyResponse()
    follow_control.callback(request, response)

    assert response.success is True
    assert '已开启' in response.message
    assert follow_control.ai_enabled is True

    request = DummyRequest(False)
    response = DummyResponse()
    follow_control.callback(request, response)

    assert response.success is True
    assert '已关闭' in response.message
    assert follow_control.ai_enabled is False


def test_image_callback2_publishes_frames_and_handles_full_queue():
    follow_control = make_follow_control()

    follow_control.bridge = DummyBridge(np.zeros((8, 8, 3), dtype=np.uint8) + 1)
    follow_control.image_callback2(object())

    assert follow_control.infer_queue.qsize() == 1
    assert follow_control.img_queue.qsize() == 1
    assert np.array_equal(follow_control.infer_queue.get_nowait(), np.ones((8, 8, 3), dtype=np.uint8))

    # Fill the queues and ensure image_callback2 does not raise when full.
    follow_control.image_callback2(object())
    follow_control.image_callback2(object())

    assert follow_control.infer_queue.qsize() == 2
    assert follow_control.img_queue.qsize() == 2


def test_publish_velocity_emits_twist_message():
    follow_control = make_follow_control()
    follow_control.publish_velocity(0.42, -0.13)

    assert len(follow_control.velocity_publisher.published) == 1
    msg = follow_control.velocity_publisher.published[0]
    assert msg.linear.x == 0.42
    assert msg.angular.z == -0.13


def test_publish_compressed_img_encodes_and_publishes_jpeg():
    follow_control = make_follow_control()
    image = np.full((32, 32, 3), 128, dtype=np.uint8)

    follow_control.publish_compressed_img(image)

    assert len(follow_control.publisher_img.published) == 1
    msg = follow_control.publisher_img.published[0]
    assert isinstance(msg, CompressedImage)
    assert msg.format == 'jpeg'
    assert len(msg.data) > 0
