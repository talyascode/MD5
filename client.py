"""
Author: Talya Gross
MD5 Client
"""
# import
import socket
import threading
import hashlib
import os

# constants
CPU = os.cpu_count()
NUMBERS_FOR_CPU = 1000000


class Client:
    """
        build function of the Client class.
    """
    def __init__(self, port, ip):
        self.digit = 0
        self.msg = ""
        self.start = 0
        self.server_hash = ""
        self.jobs = []
        self.found = False  # if the string was found
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
            while True and not self.found:
                start = input("enter yes to start, exit to quit ")
                if start == "yes":
                    self.sock.send("start".encode())
                    answer = self.sock.recv(1024).decode()
                    if answer == "start":
                        self.sock.send(str(CPU).encode())  # sending the number of logic processors to the server
                        self.server_hash = self.sock.recv(1024).decode()  # receiving the hash from the server
                        self.start = int(self.sock.recv(1024).decode())  # receiving the start position from the server
                        while not self.found:
                            self.jobs = []
                            self.open_threads()  # open threads
                            for job in self.jobs:  # join- waiting for the threads to finish
                                job.join()
                            # sending yes--> the string was found. no --> keep searching
                            self.sock.send(self.msg.encode())
                            if self.msg == "yes":  # if the string was found
                                print('found the string:' + self.digit)
                                self.sock.send(str(self.digit).encode())  # sending the result
                                break
                            else:  # the string wasn't found
                                # msg1 = if the client should keep searching and where to start
                                msg1 = self.sock.recv(1024).decode()
                                if msg1[0:3] == "yes":
                                    self.start = int(msg1[3:])
                                    print("start :" + str(self.start))
                                    print("continue searching...")
                                else:  # stop searching
                                    self.found = True
                                    print("the string was found by another client! stop searching")
                    if answer == "found":
                        print("the string was already found")
                        # close the socket
                        self.sock.send("exit".encode())
                        self.sock.close()
                        break
                if start == "exit":
                    self.sock.send("exit".encode())
                    print("exiting...")
                    break
        except socket.error as err:
            print('received socket exception - ' + str(err))
        finally:
            print("closing the socket....")
            self.sock.close()

    def open_threads(self):
        """
        opens a thread for each logical processor
        """
        for i in range(CPU):
            start = str(self.start)
            t = threading.Thread(target=self.search, args=[start])
            self.jobs.append(t)  # adding the threads to a list
            t.start()
            self.start += NUMBERS_FOR_CPU

    def search(self, start):
        """
        searching for the string using the hash
        :param start: where to start the search
        """
        start = int(start)
        for i in range(start, NUMBERS_FOR_CPU + start):
            if not self.found:  # if the string wasn't found
                digit = f'{i:010}'
                num = hashlib.md5(digit.encode())
                # print(digit)
                if str(num.digest()) == self.server_hash:  # the string was found
                    self.msg = "yes"
                    self.digit = digit
                    self.found = True  # update the status of the string so the search will stop
                    break
            else:
                break
        if not self.found:  # if the string wasn't found
            print('didnt find the string')
            self.msg = "no"


def main():
    """
         the main function of the client
    """
    try:
        my_client = Client(6000, "127.0.0.1")
        my_client.start_client()
    except socket.error as err:
        print('received socket exception - ' + str(err))
        print("couldn't make a connection... try again")
    finally:
        pass  # there is no socket to close when the client wasn't able to connect.


if __name__ == "__main__":
    # Call the main handler function
    main()
