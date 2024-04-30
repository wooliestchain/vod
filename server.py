import cv2
import socket
import pickle
import struct

# Configurer le socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Liaison du socket à l'adresse et au port
server_socket.bind(socket_address)

# Écouter les connexions entrantes
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Accepter la connexion entrante
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)

        while (vid.isOpened()):
            ret, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)

            cv2.imshow('VIDEO FROM SERVER', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
