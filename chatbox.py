import sys
import time
import os
import platform

try:
    
    while True:
        
        Os = platform.system()
        if Os == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
            
        f = open('chatbox.txt','r')
        chats = f.read()
        if len(chats) > 0:
            print('---------------------------- CHAT BOX -------------------------')
            print(chats)
            print('--------------------------------------------------------------')
            f.close()
            time.sleep(1)
        else:
            print('---------------------------- CHAT BOX -------------------------')
            print('No messages in the chat box ...please wait for the sender')
            time.sleep(1)
            f.close()
    
except:
    print('Server is not yet started')
    print('Run the program after the server is started')