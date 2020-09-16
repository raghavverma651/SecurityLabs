import socket
import random
random.seed(0)
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
cipher={chr(i+97):i+1 for i in range(26)}
def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

from random import choice 
p=683
q=751
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

def Encrypt(plain):
        plain=[cipher[i] for i in plain]
        num=""
        for i in plain:
            if(i>9):
                num+=str(i)
            else:
                num+="0"+str(i)
        encrypted=[]
        for i in range(0,len(num),2):
            smt=((int(str(num[i]+num[i+1])))**e)%n
            encrypted.append(str(smt))
        print("Encrypted message (numeric) - ",end='')
        for i in encrypted:
            print(i,end=' ')
        return ' '.join(encrypted)


plain = input('Enter Message to Send: ')
final = Encrypt(plain)
send(final)
send(DISCONNECT_MESSAGE)
