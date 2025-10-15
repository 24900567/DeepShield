import os
from detector import detect_deepfake

def test_detect_deepfake_valid_video():
    # Test with existing video
    result = detect_deepfake("assets/sample.mp4")
    assert isinstance(result, dict)
    assert "score" in result
    assert "label" in result
    assert "suspicious_frames" in result
    assert "total_frames" in result
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 100
    assert isinstance(result["suspicious_frames"], int)
    assert isinstance(result["total_frames"], int)
    assert result["total_frames"] >= 0
    assert result["suspicious_frames"] >= 0
    assert result["suspicious_frames"] <= result["total_frames"]

def test_detect_deepfake_invalid_video():
    # Test with non-existent video
    try:
        detect_deepfake("nonexistent.mp4")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass

def test_detect_deepfake_no_frames():
    # Test with a video that has no analyzable frames (if possible, or mock)
    # For now, assume sample.mp4 has frames
    result = detect_deepfake("assets/sample.mp4")
    assert result["total_frames"] >= 0

def test_detect_deepfake_labels():
    result = detect_deepfake("assets/sample.mp4")
    assert result["label"] in ["High chance of deepfake", "Possibly manipulated", "Likely authentic"]
