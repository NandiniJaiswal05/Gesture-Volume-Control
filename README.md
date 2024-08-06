# Gesture-Volume-Control

### Overview
This project implements a system to control the system volume using hand gestures. Two methods are provided:

1. **Thumb-Index Distance:** The volume is adjusted based on the distance between the thumb and index finger. Bringing the fingers closer decreases the volume, while moving them apart increases it.
2. **Index Finger Rotation:** The volume is controlled by rotating the index finger clockwise (decrease) or anticlockwise (increase).

### Dependencies
* **OpenCV:** For image processing and hand detection.
* **MediaPipe:** For hand landmark detection.
* **PyAutoGUI:** For system volume control.

### Installation
Ensure you have Python installed. Then, install the required dependencies using pip:

```bash
pip install opencv-python mediapipe pyautogui
```

### Usage
1. Run the Python script.
2. Position your hand in front of the camera.
3. Perform the desired hand gestures to control the volume.

### Customization
* **Camera:** Adjust the camera parameters (resolution, FPS) in the code.
* **Hand Detection Model:** Experiment with different hand detection models provided by MediaPipe.
* **Volume Control Sensitivity:** Modify the sensitivity of volume changes based on gesture movements.
* **Gesture Recognition:** Improve the accuracy of gesture recognition by fine-tuning the algorithm.

### Known Issues
* Hand detection might be affected by lighting conditions and background complexity.
* Gesture recognition accuracy can vary depending on hand position and movement speed.

### Contributing
Contributions are welcome! Please feel free to fork the repository and submit pull requests.
 
