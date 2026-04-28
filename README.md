# Person Follow

## 项目简介

`person_follow` 是一个基于 ROS2 的人体跟踪功能包，通过视觉检测实现机器人对目标人物的自动跟随。该组件订阅相机图像话题，使用 YOLOv8 模型进行人体检测，并根据检测结果输出速度控制指令，使机器人能够自主跟随目标人物移动。

## 功能特性

**支持：**
- 基于 YOLOv8 的实时人体检测
- 通过 ROS2 服务动态开启/关闭跟踪功能
- 可配置的线速度和角速度参数
- 可配置的图像偏差容忍度和检测超时时间
- 支持 SpaceMIT 硬件加速推理（如可用）
- 可选的检测结果图像发布

**不支持：**
- 多目标同时跟踪（当前仅跟踪距离画面中心最近的目标）
- 深度信息融合
- 目标重识别（ReID）

## 快速开始

### 环境准备

- ROS2 Humble 或更高版本
- Python 3.8+
- 依赖包安装：
```
sudo apt install python3-opencv
```


### 构建编译

```bash
# 进入工作空间
cd <your_ros2_workspace>

# 编译
colcon build --packages-select person_follow

# 加载环境
source install/setup.bash
```

### 运行示例

1. 启动节点：
```bash
ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:="/dev/video12"
```
这将发布 /image_raw

2. 启动跟踪功能：
```bash
ros2 launch person_follow person_follow.launch.py
```

3. 开启跟踪功能：
```bash
ros2 service call /toggle_follow std_srvs/srv/SetBool "{data: true}"
```

4. 关闭跟踪功能：
```bash
ros2 service call /toggle_follow std_srvs/srv/SetBool "{data: false}"
```

**可配置参数：**

| 参数名 | 默认值 | 说明 |
|--------|--------|------|
| `sub_image_topic` | `/image_raw` | 订阅的图像话题 |
| `linear_x` | `0.4` | 前进线速度 (m/s) |
| `angular_z` | `0.37` | 转向角速度 (rad/s) |
| `allowable_deviation` | `90.0` | 允许的图像中心偏差 (像素) |
| `detection_timeout` | `4.0` | 目标丢失后停止的超时时间 (秒) |
| `publish_result_img` | `false` | 是否发布检测结果图像 |

## 详细使用

详细使用说明请参考官方文档。

## 常见问题

**Q: 模型文件在哪里？**
A: 模型文件默认路径为 `~/.brdk_models/jobot_mono_follow/yolov8n.q.onnx`，首次运行时会自动下载。

**Q: 如何调整跟踪灵敏度？**
A: 可通过调整 `allowable_deviation` 参数控制转向灵敏度，值越小转向越灵敏。

**Q: 检测不到人怎么办？**
A: 请确保：
- 相机话题正确发布图像
- 光照条件良好
- 目标人物在相机视野范围内

## 版本与发布

| 版本 | 日期 | 说明 |
|------|------|------|
| 0.0.0 | - | 初始版本 |

## 贡献方式

欢迎提交 Issue 和 Pull Request。

## License

本组件源码文件头声明为 Apache-2.0，最终以本目录 `LICENSE` 文件为准。
