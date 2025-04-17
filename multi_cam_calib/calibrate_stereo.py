import cv2
import numpy as np
import json
import os
import glob

# Load intrinsic parameters from JSON files
def load_intrinsics(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    camera_matrix = np.array(data['camera_matrix'], dtype=np.float32)
    dist_coeffs = np.array(data['dist_coeffs'], dtype=np.float32)
    return camera_matrix, dist_coeffs

# Find chessboard corners in images
def find_chessboard_corners(image_path, board_size):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
            (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
    return ret, corners, gray.shape[::-1]

# Perform stereo calibration
def stereo_calibrate(cam1_images, cam2_images, board_size, square_size, cam1_intrinsics, cam2_intrinsics):
    objp = np.zeros((board_size[0]*board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints_cam1 = []
    imgpoints_cam2 = []
    image_size = None

    for cam1_img, cam2_img in zip(cam1_images, cam2_images):
        ret1, corners1, img_size = find_chessboard_corners(cam1_img, board_size)
        ret2, corners2, _ = find_chessboard_corners(cam2_img, board_size)

        if ret1 and ret2:
            objpoints.append(objp)
            imgpoints_cam1.append(corners1)
            imgpoints_cam2.append(corners2)
            image_size = img_size
        else:
            print(f"[WARN] Chessboard not found in {cam1_img} or {cam2_img}")

    # Stereo calibration
    ret, camera_matrix1, dist_coeffs1, camera_matrix2, dist_coeffs2, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints_cam1, imgpoints_cam2, cam1_intrinsics[0], cam1_intrinsics[1],
        cam2_intrinsics[0], cam2_intrinsics[1], image_size, flags=cv2.CALIB_FIX_INTRINSIC)

    return R, T, E, F

# Save extrinsics (rotation, translation) to a JSON file
def save_extrinsics(filename, R, T):
    data = {
        'rotation': R.tolist(),
        'translation': T.tolist()
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    # Parameters
    cam1_folder = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/cam1'
    cam2_folder = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/cam2'
    board_size = (9, 6)  # 9x6 inner corners
    square_size = 0.0244  # Square size in meters (adjust as needed)

    # Load intrinsic parameters
    cam1_intrinsics = load_intrinsics('intrinsics_cam1.json')
    cam2_intrinsics = load_intrinsics('intrinsics_cam2.json')

    # Get list of synchronized image pairs
    cam1_images = sorted(glob.glob(os.path.join(cam1_folder, '*.jpg')))
    cam2_images = sorted(glob.glob(os.path.join(cam2_folder, '*.jpg')))

    # Perform stereo calibration
    R, T, E, F = stereo_calibrate(cam1_images, cam2_images, board_size, square_size, cam1_intrinsics, cam2_intrinsics)

    # Save the extrinsic parameters
    save_extrinsics('extrinsics_cam1_cam2.json', R, T)

    print("[INFO] Stereo calibration complete. Extrinsics saved to 'extrinsics_cam1_cam2.json'.")
