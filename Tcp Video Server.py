import socket
import cv2
import numpy as np

# Параметры сервера
HOST = '0.0.0.0'  # Слушать на всех интерфейсах
PORT = 8000

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Сервер запущен. Ожидание подключения на порту {PORT}...")

conn, addr = server_socket.accept()
print(f"Клиент подключился: {addr}")

# Буфер для приема данных
data_buffer = b''

try:
    while True:
        # Получаем данные от клиента
        data = conn.recv(4096)
        if not data:
            break

        data_buffer += data

        # Поиск маркера конца кадра
        while b'END' in data_buffer:
            # Разделяем буфер на один кадр и остаток
            frame_data, data_buffer = data_buffer.split(b'END', 1)

            # Преобразуем данные в изображение
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if frame is not None:
                # Отображение кадра
                cv2.imshow('Серверное видео', frame)

                # Закрытие окна при нажатии клавиши
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
    print("Сервер остановлен.")
