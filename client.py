import socket
import threading
import found
import hashlib
import os


CPU = os.cpu_count()
NUMBERS_FOR_CPU = 10000


class Client():
    """
        build function of the Client class.
    """
    def __init__(self, port, ip):
        self.digit = 0
        self.msg = ""
        self.start = 0
        self.server_hash = ""
        self.jobs = []
        # self.found = False
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
            while True and not found.found:
                start = input("enter yes to start, exit to quit ")
                if start == "yes":
                    self.sock.send("start".encode())
                    #print("the server is looking for more clients...")
                    answer = self.sock.recv(1024).decode()
                    if answer == "start":
                        # sending the number of logic processors to the server
                        #self.sock.send("cpu".encode())
                        self.sock.send(str(CPU).encode())
                        self.server_hash = self.sock.recv(1024).decode()
                        self.start = int(self.sock.recv(1024).decode())
                        print("CPU" + self.server_hash)
                        print(self.start)

                        while True and not found.found:
                            self.jobs = []
                            self.open_threads()  # open threads
                            # join- waiting for the threads to finish
                            for job in self.jobs:
                                job.join()
                            # print("continue....")
                            self.sock.send(self.msg.encode())
                            if self.msg == "yes":  # if the string was found
                                # found = True
                                print('found the string:')
                                print(self.digit)
                                self.sock.send(self.digit.encode())
                                break
                            else:  # the string wasn't found
                                msg1 = self.sock.recv(1024).decode()  # if the client should keep searching
                                print(msg1)
                                if msg1 == "yes":
                                    self.start = int(self.sock.recv(1024).decode())  # receiving the start pos
                                    print("start :" + str(self.start))
                                    print("continue searching...")

                                else:  # stop searching
                                    found.found = True
                                    print("stop")
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
            self.sock.close()

    def open_threads(self):
        for i in range(CPU):
            start = str(self.start)
            t = threading.Thread(target=self.search, args=[start])
            self.jobs.append(t) # adding the threads to a list
            t.start()
            self.start += NUMBERS_FOR_CPU

    def search(self, start):
        digit = 0
        start = int(start)
        # while loop
        for i in range(start, NUMBERS_FOR_CPU + start):
            if not found.found:  # if the string wasnt found
                digit = f'{i:06}'
                num = hashlib.md5(digit.encode())
                print(digit)
                # printing the equivalent byte value.
                # print("The byte equivalent of hash is : ", end="")
                # print(num.digest())
                # print(str(num.digest()) == self.server_hash)
                if str(num.digest()) == self.server_hash:  # the string was found
                    self.msg = "yes"
                    self.digit = digit
                    found.found = True  # update the status of the string so the search will stop
                    break
            else:
                break
        if not found.found: # if the string wasnt found
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
