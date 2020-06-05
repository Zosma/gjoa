import socket
import sys


# Method to check which IP to connect to the database
# Starts at localhost and farther from there.
def check_ip(debug=False):
    if debug:
        return 0
    # Create a socket scanner to check the ports of mysql server on various IPs
    ips = ['127.0.0.1', '192.168.1.10']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for ip in ips:
        try:
            target = s.connect((ip, 3306))
            return ip
        except:
            continue
    sys.exit("Program halted: no sufficient IP addresses found for database.")
