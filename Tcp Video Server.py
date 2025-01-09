import socket
import cv2
import numpy as np
import time

# Server parameters
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server started. Waiting for connection on port {PORT}...")

conn, addr = server_socket.accept()
print(f"Client connected: {addr}")

# Buffer for receiving data
data_buffer = b''

# Variables for FPS and delay calculation
frame_count = 0
start_time = time.time()
log_interval = 2  # Log every 2 seconds
last_log_time = time.time()

try:
    while True:
        # Receive data from client
        data = conn.recv(4096)
        if not data:
            break

        data_buffer += data

        # Search for frame end marker
        while b'END' in data_buffer:
            # Split buffer into one frame and remaining data
            frame_data, data_buffer = data_buffer.split(b'END', 1)

            # Convert data to image
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if frame is not None:
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
                        delay = elapsed_time * 1000  # milliseconds
                        print(f"Delay: {delay:.2f} ms")
                        last_log_time = current_time

                # Display frame
                cv2.imshow('Server Video', frame)

                # Close window on key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
    print("Server stopped.")
