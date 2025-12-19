# Visual SLAM Exploration: From Raw Geometry to Loop Closure

A comprehensive study of Monocular Visual SLAM (Simultaneous Localization and Mapping) implemented in Python. This project tracks the evolution from basic frame-to-frame motion estimation to a structured system incorporating camera calibration, keyframe management, and loop closure detection.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10-green.svg)

## 📌 Project Milestones

### 1. The "Manual" Front-End
Developed a raw script to calculate the Essential Matrix and triangulate 3D points. 
* **Challenge:** Encountered the "Dead Reckoning" problem where numerical errors compounded exponentially.
* **Result:** Successfully extracted a sparse point cloud, proving the fundamental link between 2D pixel motion and 3D space.

### 2. Precise Camera Calibration
Transitioned from "guessed" focal lengths to a formal calibration pipeline.
* **Process:** Utilized a 12x8 checkerboard pattern on a digital display to calculate the **Intrinsic Matrix (K)** and distortion coefficients.
* **Impact:** Corrected lens warping, providing the mathematical foundation required for professional SLAM stability.

### 3. ORB-SLAM2 Architecture Logic
Implemented a structured pipeline inspired by the ORB-SLAM2 paper:
* **Preprocessing:** Converted MP4 video into a synchronized image sequence with a timestamped manifest (`rgb.txt`).
* **Feature Distribution:** Used ORB (Oriented FAST and Rotated BRIEF) to detect landmarks across 800+ frames of a room walk.
* **Memory & Loop Closure:** Developed a Keyframe Database to store "memories" of locations. Implemented a Hamming distance-based matching system to detect when the camera returned to a previously mapped area, successfully triggering **Loop Closure** alerts.

## 🛠️ Technical Stack
* **Language:** Python 3.12
* **Vision Engine:** OpenCV (`cv2.ORB`, `cv2.BFMatcher`)
* **Data Management:** YAML for configuration, custom manifest generation for dataset syncing.
* **Math:** NumPy for transformation matrix operations.

## 📂 Project Structure
``text
.
├── dataset/
│   ├── rgb/             # Extracted video frames
│   └── rgb.txt          # Timestamps and file associations
├── phone_camera.yaml    # Calibration parameters (fx, fy, cx, cy)
├── run_orbslam.py       # Main tracking and loop closure logic
└── camera_calibration.py # Checkerboard processing script

🧠 Key Learnings

Scale Ambiguity: Experienced firsthand that monocular SLAM requires a baseline to determine if a movement is 1 meter or 10 meters.

Robustness: Learned to handle ZeroDivisionError and tracking failures caused by motion blur or lack of texture (blank walls).

Optimization: Understood that while geometry gets you started, Bundle Adjustment and Loop Closure are what make a map reliable.
