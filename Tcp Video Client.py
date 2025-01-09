import socket
import cv2
import numpy as np

# Параметры клиента
SERVER_IP = '83.147.255.66'  # Замените на IP сервера
SERVER_PORT = 8000

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Подключено к серверу {SERVER_IP}:{SERVER_PORT}")

# Открываем доступ к веб-камере
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Не удалось открыть камеру.")
    client_socket.close()
    exit()

try:
    while True:
        # Чтение кадра с камеры
        ret, frame = camera.read()
        if not ret:
            print("Не удалось получить кадр с камеры.")
            break

        # Сжатие кадра перед отправкой
        _, buffer = cv2.imencode('.jpg', frame)
        client_socket.sendall(buffer.tobytes() + b'END')

        # Отображение локального видео
        cv2.imshow('Клиентское видео', frame)

        # Закрытие при нажатии клавиши
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.release()
    client_socket.close()
    cv2.destroyAllWindows()
    print("Клиент остановлен.")
