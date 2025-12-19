import cv2
import numpy as np
import matplotlib.pyplot as plt
import yaml
import os



# ---- Settings for LOOP CLOSURE -----
KEYFRAME_INTERVAL = 20   # Save a "memory" every 20 frames
keyframe_database = []   # Stores descriptors, frame_index
LOOP_THRESHOLD = 0.6      # Match percentrage to trigger a "loop"




# Load your camera calibration
with open("phone_camera.yaml", 'r') as f:
    # Remove the %YAML:1.0 header if it causes issues
    calib = yaml.safe_load(f.read().replace("%YAML:1.0", ""))


# Camera Matrix K
K = np.array([
    [calib['Camera.fx'],0,calib['Camera.cx']],
    [0,calib['Camera.fy'],calib['Camera.cy']],
    [0,0,1]
])


# Setup ORB Extractor (Standard ORB-SLAM2 settings)

orb = cv2.ORB_create(
    nfeatures=calib['ORBextractor.nFeatures'],
    scaleFactor = calib['ORBextractor.scaleFactor'],
    nlevels = calib['ORBextractor.nLevels'],
    edgeThreshold = 31,
    patchSize = 31,
    fastThreshold = calib['ORBextractor.iniThFAST']
)


# Load the dataset manifest
images_path = "dataset/rgb.txt"
with open(images_path,'r') as f:
    lines = [l.strip() for l in f.readlines() if not l.startswith("#")]


print(f'Starting ORB Slam logic on {len(lines)} frames')


# Variables for tracking
prev_kp,prev_des = None,None
trajectory = []


for i,line in enumerate(lines):
    parts = line.split()
    img_name = parts[1]
    img_path = os.path.join('dataset',img_name)


    frame = cv2.imread(img_path)
    if frame is None : continue

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    kp,des = orb.detectAndCompute(gray,None)


    # Visualization of features (what ORB-SLAM2 sees)
    display_frame = cv2.drawKeypoints(frame,kp,None,color=(0,255,0))


    # KEYFRAME SELECTRON
    if i % KEYFRAME_INTERVAL == 0:
        if des is not None:
          keyframe_database.append({'des' : des, 'id' : i})
          print(f'Stored KeyFrame : {i}')


    # Loop Detection (check against past memory)
    if i > 100 and kp is not None and len(kp) > 0:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)

        for kf in keyframe_database[:5]:
            matches = bf.match(des,kf['des'])

            match_ratio = len(matches) / len(kp)

            if match_ratio > LOOP_THRESHOLD:
                print(f'Loop Detected!  Frame : {i} matches keyframe at {kf['id']}')

                cv2.putText(display_frame,'LOOP DETECTED!',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)


    cv2.imshow('ORB-SLAM2 + Loop Closure',display_frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
print('Tracking Complete.')





