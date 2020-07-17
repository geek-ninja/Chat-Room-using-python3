import socket
import select

size = 10
ip = '127.0.0.1'
port = 1234

try:
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind((ip,port))
    server_socket.listen()
    socket_list = [server_socket]
    clients = dict()
    
    def clientMessages(client_socket):
        try:
            msg_size = client_socket.recv(size)
            if not len(msg_size):
                return False
            msg_len = int(msg_size.decode('utf-8').strip())
            return {'size':msg_size,'data':client_socket.recv(msg_len)}
        except:
            return False
    print('------------------------------------ CHAT SERVER ------------------------------')
    
    #------------------ To clear the previous chats ----------------------
    f = open('chatbox.txt','w')
    f.close()
    #---------------------------------------------------------------------
    
    while True:
        f = open('chatbox.txt','a+')
        read_socket,_,exception_sockets = select.select(socket_list,[],socket_list)
        for notified_socket in read_socket:        
            if notified_socket == server_socket:
                client_socket,client_address = server_socket.accept()
                user = clientMessages(client_socket)
                if user is False:
                    continue
                socket_list.append(client_socket)
                clients[client_socket] = user
                print('connection accepted ',client_address,user['data'].decode('utf-8'),'\n')
                joinMsg = '\n'+user['data'].decode('utf-8')+' join the chat'+'\n'
                f.write(joinMsg)
                f.close()
            else:
                msg = clientMessages(notified_socket)
                if msg is False:
                    print('Connection is closed from',clients[notified_socket]['data'].decode('utf-8'))
                    leftMessage = '\n'+clients[notified_socket]['data'].decode('utf-8')+' left the chat'+'\n'
                    f.write(leftMessage)
                    f.close()
                    socket_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                user = clients[notified_socket]
                if int(msg['size'].decode('utf-8').strip())>0:
                    print(user['data'].decode('utf-8'),'>',msg['data'].decode('utf-8'))
                    chatText = user['data'].decode('utf-8')+' > '+msg['data'].decode('utf-8')+'\n'
                    print('total participants ',len(clients))
                    f.write(chatText)
                    f.close()
                    
                for rest_client in clients:
                    if rest_client != notified_socket:
                        if int(msg['size'].decode('utf-8').strip())>0:
                            rest_client.send(user['size']+user['data']+msg['size']+msg['data'])
        for notified_sockets in exception_sockets:
            socket_list.remove(notified_sockets)
            del clients[notified_sockets]
except Exception as e:
    print(e)