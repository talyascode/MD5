"""
Author: Talya Gross
MD5 SERVER
"""
# import
import socket
import threading
import hashlib

# constants
NUMBERS_FOR_CPU = 1000000


class Server:
    """
        build function of the Server class.
    """
    def __init__(self, port, num):
        self.start = 0  # the start position
        self.found = False  # when false- the clients haven't found the string
        # creating the hash
        self.hash = hashlib.md5(num.encode())
        self.hash = self.hash.digest()
        # opening the server
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen()
        print("server is up")

        """
        ALL CLIENTS:
        ('127.0.0.1', 49944): socket
        ('127.0.0.1', 49942): socket
        """
        self.all_clients = {}

        print("looking for clients...")

    def wait_for_clients(self):
        """
            the function accepts new clients and calls the handle client in threading
        """
        try:
            while True:
                client_socket, client_address = self.sock.accept()
                self.all_clients[client_address] = client_socket
                print("all clients:")
                print(self.all_clients)
                t = threading.Thread(target=self.handle_client, args=[client_address])
                t.start()
                print("new thread for client:", client_address)
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            if self.all_clients:
                client_socket.close()

    def handle_client(self, client_address):
        """
            the function receives data from the current client and checks what the data is and acts according
            to the protocol of the program.
        :param client_address: the address of the current client that is being handled
        """
        client_socket = self.all_clients[client_address]
        try:
            while True:
                print("listening to client:", client_address)
                data = client_socket.recv(1024).decode()
                if self.found:
                    # print(self.found)
                    client_socket.send("found".encode())
                    break
                elif data == "start":
                    client_socket.send("start".encode())
                    cpu_num = int(client_socket.recv(1024).decode())  # receiving the cpu
                    print("CPU" + str(cpu_num))
                    client_socket.send(str(self.hash).encode())  # sending the hash to the client
                    client_socket.send(str(self.start).encode())  # sending the client where to start
                    self.start += cpu_num * NUMBERS_FOR_CPU  # updating the start position
                if data == "yes":
                    found = client_socket.recv(1024).decode()
                    print('the string is: ' + found)
                    self.found = True
                    break

                elif data == "no":
                    if self.found:  # the current client didn't find but another client did
                        client_socket.send("no".encode())  # sending the client no- to stop searching
                        client_socket.close()  # closing current socket
                    else:  # the string wasn't find by anyone and the client should keep searching
                        print("client continue")
                        self.start += cpu_num * NUMBERS_FOR_CPU  # updating the start position
                        msg = "yes" + str(self.start)
                        # sending the client where to start and to keep searching
                        client_socket.send(msg.encode())
                if data == "exit":
                    break
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            client_socket.close()


def main():
    """
        the main function of the server
    """
    num = input("Enter 10 digit number: ")
    my_server = Server(6000, num)
    my_server.wait_for_clients()


if __name__ == "__main__":
    # Call the main handler function
    main()
