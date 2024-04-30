import cv2
import socket
import pickle
import struct

# Configurer le socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.24'  # Remplacez par l'adresse IP de la machine B
port = 9999
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

# Recevoir les données de la capture vidéo
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
client_socket.close()
cv2.destroyAllWindows()
