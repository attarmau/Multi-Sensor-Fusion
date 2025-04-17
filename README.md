# Multi-Sensor-Fusion

This repo performs stereo calibration for a two-camera setup using OpenCV. It computes intrinsic and extrinsic parameters to align both cameras into a shared coordinate frame.

## Setup

```bash
pip install -r requirements.txt
```
## Folder Structure
```
Multi-Sensor-Fusion/
├── camera_calibration/
│   ├── calibrate_single.py        # Calibrate each camera separately
│   ├── calibrate_stereo.py        # Compute extrinsics between two cameras
│   ├── stereo_config.json         # Stores stereo calibration results
│   ├── intrinsics_cam0.json
│   ├── intrinsics_cam1.json
│   └── utils.py                   # Helper functions
│
├── data/
│   ├── cam0/                      # Calibration images from camera 0
│   │   ├── img_001.jpg
│   │   └── ...
│   └── cam1/                      # Calibration images from camera 1
│       ├── img_001.jpg
│       └── ...
│
├── README.md                      # Setup + usage instructions
├── requirements.txt               # Dependencies
└── .gitignore
```

Camera calibration finds the intrinsic parameters of your camera, like:
- fx, fy: focal length (in pixels)
- cx, cy: principal point (optical center)
- k1, k2, ...: lens distortion coefficients

These parameters describe how your camera "sees" the world and are essential for:
- 3D reconstruction
- Multi-camera fusion
- Removing lens distortion
- Projecting 3D points onto 2D images accurately

# Run 
## Step 1
```
  --images /Your-file-path/MultiSensor-Fusion-main/data/cam1 \
  --out intrinsics_cam1.json \
  --board 9x6
```
If it shows the message below then means the intrinsic parameters were saved successfully
```
[INFO] Calibration saved to intrinsics_cam1.json
```
