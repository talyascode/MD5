"""
Author: Talya Gross
MD5 CLIENT
"""
# import
import os
import hashlib
import socket

CPU = os.cpu_count()


class Client:
    """
        build function of the Client class.
    """
    def __init__(self, port, ip):
        print("connecting...")
        self.sock = socket.socket()
        self.sock.connect((ip, port))
        print("connected!")

    def start_client(self):
        """
            the function receives input from the user and according to that it
            starts or exits and closes the socket. here is all the communication
             with the server after connecting.
        """
        try:
            while True:

                start = input("enter yes to start, exit to quit ")
                if start == "yes":
                    self.sock.send("start".encode())
                    #print("the server is looking for more clients...")
                    answer = self.sock.recv(1024).decode()
                    if answer == "start":
                        # sending the nu,ber of logic processors to the server
                        self.sock.send("cpu".encode())
                        self.sock.send(str(CPU).encode())
                        server_hash = self.sock.recv(1024).decode()
                        print(server_hash)
                        msg, digit = self.search(server_hash)
                        self.sock.send(msg.encode())
                        if msg == "yes":  # if the string was found
                            found = True
                            self.sock.send(digit.encode())
                            break

                    #if answer == "found":
                     #   print("the string was already found")
                        # close the socket
                     #   self.sock.send("exit".encode())
                    #    self.sock.close()
                     #   return None
                if start == "exit":
                    self.sock.send("exit".encode())
                    print("exiting...")
                    break
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            self.sock.close()

    def search(self, server_hash):
        digit = 0
        found = False
        for i in range(0, 100):
            digit = f'{i:03}'
            num = hashlib.md5(digit.encode())
            print(digit)
            # printing the equivalent byte value.
            print("The byte equivalent of hash is : ", end="")
            print(num.digest())
            print(str(num.digest()) == server_hash)
            if str(num.digest()) == server_hash:
                print('found the string:')
                print(digit)
                return "yes", digit
                break
        if not found:
            return  "no"
def main():
    """
         the main function of the client
    """
    try:
        my_client = Client(7000, "127.0.0.1")
        client = my_client.start_client()
    except socket.error as err:
        print('received socket exception - ' + str(err))
        print("couldn't make a connection... try again")
    finally:
        pass  # there is no socket to close when the client wasn't able to connect.


if __name__ == "__main__":
    # Call the main handler function
    main()

