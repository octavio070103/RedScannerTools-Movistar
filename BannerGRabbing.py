import socket
import sys

IP_RANGE = "10.0.2"
ports = [21, 22, 25, 534, 79, 80, 110, 443, 8080]

for host in range(3, 5):
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((IP_RANGE + "." + str(host), port))
            banner = s.recv(1024)
            print("Banner encontrado en IP = " + IP_RANGE + "." + str(host) + ", puerto = " + str(port))
            print("Banner = " + banner.decode())
        except socket.error as e:
            print(f"Error al conectar a {IP_RANGE}.{host}, puerto {port}: {e}")
        finally:
            s.close()
