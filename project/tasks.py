import cv2

def capture_image_in_background():
    # Open the default camera (0 for the main camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a frame
    ret, frame = cap.read()

    if ret:
        # Save the image to disk silently (can be stored in a temp folder)
        image_path = "captured_image.png"
        cv2.imwrite(image_path, frame)
        print(f"Image saved as {image_path}")
        return image_path
    else:
        print("Error: Could not capture image.")
        return None

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
