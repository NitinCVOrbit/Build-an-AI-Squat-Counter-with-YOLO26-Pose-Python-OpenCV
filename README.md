# 🏋️ AI Squat Counter Using YOLO26 Pose Estimation

Build an AI-powered Squat Counter using YOLO26 Pose Estimation, Python, and OpenCV!

This Computer Vision project detects human body keypoints, calculates knee angles, identifies squat movements, and automatically counts completed repetitions.

## 🎥 YouTube Tutorial

Watch the complete step-by-step tutorial on YouTube:

👉 [Build an AI Squat Counter Using YOLO26 Pose Estimation](https://youtu.be/vkEww1K8MSc)

## 🚀 Features

- 🤖 Human Pose Estimation using YOLO26.
- 📐 Left and right knee angle calculation using the vector method.
- 🏋️ Automatic squat detection using DOWN and UP angle thresholds.
- 🔢 Automatic repetition counting.
- 🎯 Stable frame detection to reduce false counting.
- 📊 Live information panel displaying squat count, movement state, and average knee angle.
- 🎥 Real-time video processing using OpenCV.

## 🛠️ Technologies Used

- Python
- YOLO26 Pose Estimation
- OpenCV
- NumPy
- Ultralytics

## ⚙️ How It Works

1. YOLO26 detects the human body and extracts pose keypoints.
2. The system identifies the left and right hips, knees, and ankles.
3. Knee angles are calculated using the vector-based angle calculation method.
4. The average knee angle determines whether the person is in the DOWN or UP position.
5. Stable frame detection confirms each movement state across consecutive frames.
6. A squat is counted when the person completes a DOWN-to-UP movement.

## 📐 Squat Counter Configuration

| Parameter | Value | Description |
|---|---:|---|
| Down Angle | 140° | Detects the downward squat position |
| Up Angle | 165° | Detects the standing position |
| Stable Frames | 3 | Consecutive frames required to confirm a state |
| Confidence | 0.5 | YOLO pose detection confidence |

## ⭐ Support

If you find this project helpful, please consider giving this repository a ⭐ star!

Subscribe to the channel for more Python, Computer Vision, Deep Learning, and AI projects.

#ComputerVision #YOLO26 #PoseEstimation #Python #OpenCV #SquatCounter #AIProjects
