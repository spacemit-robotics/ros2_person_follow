# Person Follow

## Overview

`person_follow` is a ROS2-based human tracking package that enables robots to automatically follow a target person through visual detection. This component subscribes to camera image topics, uses the YOLOv8 model for human detection, and outputs velocity control commands based on detection results, allowing the robot to autonomously follow the target person.

## Features

**Supported:**
- Real-time human detection based on YOLOv8
- Dynamically enable/disable tracking via ROS2 service
- Configurable linear and angular velocity parameters
- Configurable image deviation tolerance and detection timeout
- SpaceMIT hardware-accelerated inference support (if available)
- Optional detection result image publishing

**Not Supported:**
- Multi-target simultaneous tracking (currently only tracks the target closest to the image center)
- Depth information fusion
- Target re-identification (ReID)

## Quick Start

### Prerequisites

- ROS2 Humble or later
- Python 3.8+
- Install dependencies:
```
sudo apt install python3-opencv
```

### Build

```bash
# Navigate to workspace
cd <your_ros2_workspace>

# Build
colcon build --packages-select person_follow

# Source environment
source install/setup.bash
```

### Running Examples

1. Start the camera node:
```bash
ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:="/dev/video12"
```
This will publish to /image_raw

2. Launch the tracking node:
```bash
ros2 launch person_follow person_follow.launch.py
```

3. Enable tracking:
```bash
ros2 service call /toggle_follow std_srvs/srv/SetBool "{data: true}"
```

4. Disable tracking:
```bash
ros2 service call /toggle_follow std_srvs/srv/SetBool "{data: false}"
```

**Configurable Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `sub_image_topic` | `/image_raw` | Subscribed image topic |
| `linear_x` | `0.4` | Forward linear velocity (m/s) |
| `angular_z` | `0.37` | Turning angular velocity (rad/s) |
| `allowable_deviation` | `90.0` | Allowable image center deviation (pixels) |
| `detection_timeout` | `4.0` | Timeout to stop after target lost (seconds) |
| `publish_result_img` | `false` | Whether to publish detection result image |

## Detailed Usage

Please refer to the official documentation for detailed usage instructions.

## FAQ

**Q: Where is the model file?**
A: The default model file path is `~/.brdk_models/jobot_mono_follow/yolov8n.q.onnx`, which will be automatically downloaded on first run.

**Q: How to adjust tracking sensitivity?**
A: You can adjust the `allowable_deviation` parameter to control turning sensitivity. A smaller value results in more sensitive turning.

**Q: What if no person is detected?**
A: Please ensure:
- The camera topic is correctly publishing images
- Lighting conditions are adequate
- The target person is within the camera's field of view

## Version & Release

| Version | Date | Description |
|---------|------|-------------|
| 0.0.0 | - | Initial version |

## Contributing

Issues and Pull Requests are welcome.

## License

The source code files in this component are declared as Apache-2.0 in their headers. The `LICENSE` file in this directory shall prevail.
