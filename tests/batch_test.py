# batch_test.py
import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from detector import detect_deepfake

def run_batch_test(test_folder="tests"):
    """
    Run batch analysis on all videos in the test folder.
    """
    if not os.path.exists(test_folder):
        print(f"Test folder '{test_folder}' does not exist.")
        return

    video_files = [f for f in os.listdir(test_folder) if f.endswith((".mp4", ".mov", ".avi"))]
    if not video_files:
        print(f"No video files found in '{test_folder}'.")
        return

    print(f"Running batch test on {len(video_files)} video(s)...")
    results = []
    for file in video_files:
        path = os.path.join(test_folder, file)
        try:
            result = detect_deepfake(path)
            results.append((file, result))
            print(f"{file}: Score={result['score']:.2f}%, Label={result['label']}, Suspicious={result['suspicious_frames']}/{result['total_frames']}")
        except Exception as e:
            print(f"Error analyzing {file}: {e}")

    # Summary
    total_videos = len(results)
    high_risk = sum(1 for _, r in results if r['score'] > 70)
    medium_risk = sum(1 for _, r in results if 40 < r['score'] <= 70)
    low_risk = sum(1 for _, r in results if r['score'] <= 40)
    print(f"\nBatch Test Summary:")
    print(f"Total Videos: {total_videos}")
    print(f"High Risk: {high_risk}")
    print(f"Medium Risk: {medium_risk}")
    print(f"Low Risk: {low_risk}")

if __name__ == "__main__":
    run_batch_test()
