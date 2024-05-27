import socket
def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

# Constants
ip_address = "1.1.1.1"
port_number = 62520

if is_port_open(ip_address, port_number):
    print(f"The port {port_number} is open on the IP address {ip_address}.")
else:
    print(f"The port {port_number} is closed on the IP address {ip_address}.")
