"""
Author: Talya Gross
MD5 SERVER
"""
# import
import socket
import threading
import time
import hashlib
NUMBERS_FOR_CPU = 10000


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
        
        CAN START:
        ('127.0.0.1', 49944): True
        ('127.0.0.1', 49942): False
        
        RANGES: the ranges to check the string
        ('127.0.0.1', 49944): 1-2
        ('127.0.0.1', 49944): 6-7
        
        CPU: the number of logic processors
        ('127.0.0.1', 49944): 3
        ('127.0.0.1', 49944): 8

        """
        self.all_clients = {}
        self.cpu = {}
        self.ranges = {}
        self.can_start = {}
        # t = threading.Thread(target=self.check_4_ready)
        # t.start()
        print("looking for clients...")

    def wait_for_clients(self):
        """
            the function accepts new clients and calls the handle client in threading
        """
        try:
            while True and not self.found:
                client_socket, client_address = self.sock.accept()
                self.all_clients[client_address] = client_socket
                self.can_start[client_address] = False
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
                    print(self.found)
                    client_socket.send("found".encode())
                    break
                elif data == "start":
                    client_socket.send("start".encode())
                    # recieving the cpu
                    cpu_num = int(client_socket.recv(1024).decode())
                    print("CPU" + str(cpu_num))
                    self.cpu[client_address] = cpu_num
                    # sending the hash to the client
                    client_socket.send(str(self.hash).encode())
                    # sending the client where to start
                    client_socket.send(str(self.start).encode())
                    # print(self.cpu[client_address])
                    self.start += cpu_num * NUMBERS_FOR_CPU  # updating the start position
                    # power = cpu_sum / self.cpu[ready_addr[i]]
                    # ready_socket[i].send(.encode())  # sending the range
                    #self.can_start[ready_addr[i]] = False
                if data == "yes":
                    found = client_socket.recv(1024).decode()
                    print('the string is: ' + found)
                    # self.can_play[client_address] = True
                    self.found = True
                    # sending to the clients to stop

                elif data == "no":
                    #  closing current socket
                    client_socket.close()

                    # updating dictionaries
                    self.can_start[client_address] = False
                elif data == "exit":
                    #  closing current socket
                    client_socket.close()
                    # updating dictionaries
                    self.can_start[client_address] = False
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            client_socket.close()

    def check_4_ready(self):
        """
            the function checks if there are 4 clients that are ready, according to the can start dictionary
        """
        try:
            while True:
                ready_socket = []
                ready_addr = []
                print(self.can_start)
                """
                addr1: value
                addr2: value
                addr3: value
                for addr in dict:
                    dict[addr] - false/true
                """
                cpu_sum = 0
                for addr in self.can_start:
                    if self.can_start[addr]:
                        ready_socket.append(self.all_clients[addr])
                        ready_addr.append(addr)
                if len(ready_socket) == 4:
                    #for j in self.cpu:
                    #    cpu_sum += self.cpu[ready_addr[j]]
                    for i in range(4):
                        ready_socket[i].send("start".encode())
                        ready_socket[i].send(str(self.hash).encode())
                        ready_socket[i].send(self.start.encode())
                        # self.start += self.cpu[ready_addr[i]]
                        # power = cpu_sum / self.cpu[ready_addr[i]]
                        # ready_socket[i].send(.encode())  # sending the range
                        self.can_start[ready_addr[i]] = False
                time.sleep(1)
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            if self.all_clients:
                for i in range(len(self.all_clients)):
                    client_socket = list(self.all_clients.values())[i]
                    client_socket.close()


def main():
    """
        the main function of the server
    """
    num = input("Enter 5 digit number: ")
    my_server = Server(6000, num)
    my_server.wait_for_clients()


if __name__ == "__main__":
    # Call the main handler function
    main()
