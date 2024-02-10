import cv2
import time

def capture_image(file_path='snapshot.jpg'):
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    time.sleep(1)
    
    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    
    # Save the captured image
    cv2.imwrite(file_path, frame)
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# Usage
capture_image('snapshot.png')
