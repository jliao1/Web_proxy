from socket import *
from urllib.parse import urlparse
import sys
from pathlib import Path

def main():
    # Cache the files into the relative folder ‘./cache/SUB_FOLDERS_IF_NEEDED’.
    # The proxy should be able to create such folder(s) if they do not exist.
    Path('./cache/SUB_FOLDERS_IF_NEEDED').mkdir(parents=True, exist_ok=True)

    server_port = 11249
    # Create a socket for proxy
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_socket.bind(('', server_port))

    proxy_socket.listen(1)
    print("******************** Ready to Serve... **************************")

    while True:

        # Start receiving data from the client
        connection_socket, addr = proxy_socket.accept()
        message_from_client = connection_socket.recv(1024)
        print("Received a client connection from:", addr)
        print("Client message is:", message_from_client)


        # parse the requested URL to retrieve three pieces of information: the requested host, port, and path
        message_list = message_from_client.decode().split()
        # if len(message_list) != 3:
        method = message_list[0]
        url = message_list[1]
        http_version = message_list[2]
        parsed_rul = urlparse(url)
        host_name = parsed_rul.hostname
        path = parsed_rul.path
        port = parsed_rul.port if parsed_rul.port else 80


        print("Oops! No cache hit! Requesting sever for the file...")
        proxy_to_server_socket = socket(AF_INET, SOCK_STREAM)
        proxy_to_server_socket.connect((host_name, port))
        request = ' '.join([method, path, http_version])
        # (1)
        proxy_to_server_socket.send((request + '\r\n').encode())
        # (2)
        proxy_to_server_socket.send(("Host: " + host_name + '\r\n').encode())
        # (3)
        proxy_to_server_socket.send(("Connection: close" + '\r\n').encode())
        proxy_to_server_socket.send(("\r\n").encode())
        # Printers
        print("Sending the following msg from proxy to server:")
        print('  ' + request)
        print("Host: " + host_name)
        print("Connection: close")


        msg_from_remote = proxy_to_server_socket.recv(1024)

        print("msg_from_remote(decode): ", msg_from_remote.decode())
        print("msg_from_remote(not decode): ", msg_from_remote)


        # Close the client and the server sockets
        connection_socket.close()


main()

