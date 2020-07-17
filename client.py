import socket
import sys


size = 10
ip = '127.0.0.1'
port = 1234

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((ip,port))
client_socket.setblocking(False)

userName = input('Enter your user name: ')
print('------------------------SEND YOUR MESSAGES -----------------------------')
user_Name = userName.encode('utf-8')
username_size = f"{len(userName):<{size}}".encode('utf-8')
client_socket.send(username_size+user_Name)


while True:
    msg = input(f'{userName} > ')
    
    msg = msg.encode('utf-8')
    msg_size = f"{len(msg):<{size}}".encode('utf-8')
    client_socket.send(msg_size+msg)
    try:
        while True:
            
            chat_size = client_socket.recv(size)
            if not len(chat_size):
                print('chat is  closed by the server')
                sys.exit()
            chat_len = int(chat_size.decode('utf-8').strip())
            clientName = client_socket.recv(chat_len).decode('utf-8')
            
            message_size = client_socket.recv(size)
            message_len = int(message_size.decode('utf-8').strip())
            message = client_socket.recv(message_len).decode('utf-8')
            #print(clientName,'> ',message)
            #print('\npress enter to refresh')
            
    except Exception as e:
        continue
    except KeyboardInterrupt as e:
        print('Chat closed')
        sys.exit()
    except:
        continue
    