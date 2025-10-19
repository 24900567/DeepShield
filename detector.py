import os
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"  # Fix for Streamlit/Windows video issues
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.system("apt-get update -qq && apt-get install -y libgl1 libglib2.0-0 ffmpeg > /dev/null 2>&1")
import logging
import numpy as np

# --- Safe import of OpenCV ---
try:
    import cv2
except ImportError:
    os.system("pip install opencv-python-headless==4.8.1.78")
    import cv2

from deepface import DeepFace


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def detect_deepfake(video_path, frame_skip=30, reports_dir="reports"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")

    suspicious_frames = 0
    total_frames = 0
    frame_count = 0
    total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    os.makedirs(reports_dir, exist_ok=True)
    logger.info(f"Analyzing {video_path} with {total_video_frames} frames...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        total_frames += 1
        try:
            result = DeepFace.analyze(frame, actions=['emotion', 'age', 'gender'], enforce_detection=False)
            if result and 'dominant_emotion' in result[0]:
                emotion = result[0]['dominant_emotion']
                age = result[0]['age']
                gender = result[0]['gender']

                score = 0
                suspicious = 0

                if emotion in ['neutral', 'surprised']:
                    score += 0.4
                    suspicious += 1
                if age < 18 or age > 70:
                    score += 0.3
                    suspicious += 1
                if gender not in ['Man', 'Woman'] or gender == 'Unknown':
                    score += 0.3
                    suspicious += 1
                if age <= 5:
                    suspicious += 1

                if suspicious >= 2 or score >= 0.6:
                    suspicious_frames += 1
                    resized_frame = cv2.resize(frame, (320, 240))
                    cv2.imwrite(f"{reports_dir}/frame_{total_frames}.jpg", resized_frame)
                    logger.info(f"Suspicious frame {total_frames}: emotion={emotion}, age={age}, gender={gender}")
        except Exception as e:
            logger.warning(f"Error analyzing frame {frame_count}: {str(e)}")
            continue

    cap.release()
    score_percent = (suspicious_frames / total_frames) * 100 if total_frames > 0 else 0

    if score_percent > 60:
        label = "Likely deepfake"
    elif score_percent > 30:
        label = "Suspicious content"
    else:
        label = "Authentic"

    logger.info(f"Done: score={score_percent:.2f}%, suspicious={suspicious_frames}/{total_frames}, label={label}")
    return {
        "score": score_percent,
        "label": label,
        "suspicious_frames": suspicious_frames,
        "total_frames": total_frames
    }
