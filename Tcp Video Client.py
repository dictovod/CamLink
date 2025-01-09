import socket
import cv2
import numpy as np
import time

# Client parameters
SERVER_IP = '83.147.255.66'  # Replace with server IP
SERVER_PORT = 8000

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Connected to server {SERVER_IP}:{SERVER_PORT}")

# Access webcam
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Failed to open camera.")
    client_socket.close()
    exit()

# Variables for FPS calculation
frame_count = 0
start_time = time.time()
log_interval = 2  # Log every 2 seconds
last_log_time = time.time()

try:
    while True:
        # Read frame from the camera
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame from camera.")
            break

        # Resize frame for efficiency
        frame = cv2.resize(frame, (640, 480))

        # Compress frame before sending
        _, buffer = cv2.imencode('.jpg', frame)
        client_socket.sendall(buffer.tobytes() + b'END')

        # Calculate FPS
        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 1:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = current_time

            # Log FPS and delay at the specified interval
            if current_time - last_log_time >= log_interval:
                print(f"FPS: {fps:.2f}")
                last_log_time = current_time

        # Display local video
        cv2.imshow('Client Video', frame)

        # Close window on key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.release()
    client_socket.close()
    cv2.destroyAllWindows()
    print("Client stopped.")
