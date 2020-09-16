import socket
import threading
import random
random.seed(0)

class Server:

    def __init__(self):
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def Decrypt(self, a):
        p=683
        q=751
        revcipher={i+1:chr(i+97) for i in range(26)}
        print("p taken -",p)
        print("q taken -",q)
        n=p*q
        phi=(p-1)*(q-1)
        from math import gcd
        e=0
        for i in range(2,phi):
            if(gcd(i,phi)==1):
                e=i
                break
        d=0
        for i in range(1,10): 
            x = 1 + i*phi 
            if x % e == 0: 
                d = int(x/e) 
                break
        print("Public key -",(e,n))
        print("Private key -",(d,n))
        revcipher={i+1:chr(i+97) for i in range(26)}
        a=[int(i) for i in a.split()]
        decrypted=[]
        for i in a:
            decrypted.append((i**d)%n)
        decrypted=''.join([revcipher[i] for i in decrypted])
        return decrypted

    def show(self):
        print(self.HEADER)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False

                print('Encrypted message = ', msg)
                print('Decrypted Message = ', self.Decrypt(
                    msg))
                # conn.send("Msg received".encode(self.FORMAT))
        conn.close()

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            # self.conn, self.addr = conn, addr
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


Server().start()
