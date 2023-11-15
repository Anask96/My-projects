import socket 
import select  
import threading 
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(("localhost", 8080))

sock.listen(64)

connections = []
if "sock" not in connections:
    connections.append("sock")
clients_names = []
if "echobot" not in clients_names:    
    clients_names.append("echobot")
charString = "§±!@#$%^&*()_+-={[]}\|;:?/>.<,~`\'\""


def newUser(client_sock):
    if(len(connections) <= 64 or len(clients_names) <= 64):
        while True: 
            non = ""
            readCheck = False
            clientName = ""
            while True:
                read,write,error = select.select([client_sock],[client_sock],[client_sock],0)
                if read:
                    buffer = client_sock.recv(1).decode("utf-8")
                    non += buffer
                    read,write,error = select.select([client_sock],[client_sock],[client_sock],0)
                    if not read:
                        readCheck = True
                    if not(buffer):
                        deleteUser(clientName, client_sock)
                        return

                if (readCheck == True):
                    buffer = non
                    break

            if ("HELLO-FROM " in buffer):
                i = 11
                clientName = ""
                while(i < len(buffer) - 3):
                    clientName += buffer[i]
                    i += 1
                i = 0
                check = True
                if (len(clientName) == 0):
                    check = False
                while (i < len(clientName)):
                        if clientName[i] in charString:        
                            check = False
                            i += 1
                        i += 1
                i = 0
                while (i < len(clientName)):
                        if (i != len(clientName) - 1):
                            if (clientName[i] == " "):
                                if (clientName[i + 1].isdigit() or clientName[i + 1].isalpha()):
                                    check = False
                                    break
                        i += 1
                if ("\n" not in buffer):
                    check = False
                
                if (check == True):
                    tracker = 0
                    i = 0
                    space = 0
                    while (i < len(clientName)):
                        if (i != len(clientName) - 1):
                            if (clientName[i].isdigit() or clientName[i].isalpha()):
                                if(clientName[i + 1] == " "):
                                    tracker += 1
                                    space = i + 1
                        i += 1
                    if (tracker == 0 and clientName[0] == " "):
                        check = False
                    if (tracker == 1):
                        i = 0
                        temp = ""
                        while(i < space):
                            temp += clientName[i]
                            i += 1
                        clientName = temp

                if (check == False):
                    message =("BAD-RQST-BODY\n").encode("utf-8")
                    client_sock.sendall(message)
                    return 
                elif (clientName in clients_names):
                    message =("IN-USE\n").encode("utf-8")
                    client_sock.sendall(message)
                    return 
                else:
                    message =("HELLO " + clientName + "\n").encode("utf-8")
                    client_sock.sendall(message)
                    clients_names.append(clientName)
                    connections.append(client_sock)
                    main_chat(clientName, client_sock)
                    #inChat = threading.Thread(target = main_chat,args = (clientName, client_sock) )
                    #inChat.start()
                    return
            else:
                message = ("BAD-RQST-HDR\n").encode("utf-8")
                client_sock.sendall(message)
                break
    else:
        noAccess = ("BUSY\n").encode("utf-8")
        client_sock.sendall(noAccess)
        return

            


def main_chat(clientName, client_sock):
    while True:
        non = "".encode("utf-8")
        while True:
            read,write,error = select.select([client_sock],[client_sock],[client_sock],0)
            if read:
                buffer = client_sock.recv(1)   #.decode("utf-8")
                non += buffer
                read,write,error = select.select([client_sock],[client_sock],[client_sock],0)
                if not read:
                    buffer = non
                    buffer = buffer.decode("utf-8")
                    buffer = buffer.replace("\n", "±")
                    break
                if not buffer:
                    deleteUser(clientName, client_sock)
                    return

        i = 0
        num = 0
        multi = ""
        listA = []
        j = 0
        while(i < len(buffer)):
            multi += buffer[i]
            if(buffer[i] == '±'):
                listA.append(multi)
                multi = ""
                num += 1
            i += 1                    

        a = 0
        listTracker = 0
        multiCommand = "".encode("utf-8")
        while (a < len(listA)):
            buffer = listA[a]
            buffer = buffer.replace("±", "\n")

            if ("TEST" in buffer):
                testMessage = ("HELLO Michael\nSEND-OK\nDELIVERY anas hi\nWHO-OK\n").encode("utf-8")
                client_sock.sendall(testMessage)
                a += 1
            elif ("WHO" in buffer):
                if ("\n" not in buffer):
                    message2 = ("BAD-RQST-BODY\n").encode("utf-8")
                    client_sock.sendall(message2)
                    continue     
                i = 0
                content = ""
                while (i < len(clients_names)):
                    if (i == len(clients_names) - 1):
                        content += clients_names[i]
                    else:              
                        content += clients_names[i] + ","
                    i += 1
                messsag2 = ('WHO-OK ' + content + "\n").encode("utf-8")
                if (listTracker < len(listA)):
                    multiCommand += messsag2
                    listTracker += 1
                    if (listTracker == len(listA)):
                        client_sock.sendall(multiCommand)
                #client_sock.sendall(messsag2)
                a += 1
            elif ("SEND " in buffer):
                countInt = 0
                messageVar = ""
                userMessage = ""
                rceiver_name = ""
                for i in range(0, len(buffer)):
                    if (buffer[i] == " "):
                        countInt += 1
                    if (countInt == 2 and i == 5):
                        messageVar = "wrong"
                    elif (countInt == 1 and i > 4) or (countInt >= 2):
                        if (countInt == 1):
                            rceiver_name += buffer[i]
                        elif (countInt >= 2 and messageVar != "wrong"):
                            messageVar += buffer[i]

                userMessage = messageVar
                if (rceiver_name == clientName or userMessage == "wrong" or userMessage.isspace()):
                    message2 = ("BAD-RQST-BODY\n").encode("utf-8")
                    client_sock.sendall(message2)
                    a += 1
                    continue

                userMessage1 = ("DELIVERY " + clientName + userMessage).encode("utf-8")
                senderMessage = ("SEND-OK\n").encode("utf-8")
                if rceiver_name in clients_names:
                    if (rceiver_name == "echobot"):
                        client_sock.sendall(senderMessage)
                        time.sleep(0.1)
                        echoMessage = ("DELIVERY " + rceiver_name + userMessage).encode("utf-8")
                        if (listTracker < len(listA)): 
                            client_sock.sendall(echoMessage) 
                            listTracker += 1
                            if (listTracker == len(listA)):
                                client_sock.sendall(multiCommand)
                        #client_sock.sendall(echoMessage)
                        a += 1
                    else:
                        index = clients_names.index(rceiver_name)
                        #client_sock.sendall(senderMessage)
                        if (listTracker < len(listA)):
                            multiCommand += senderMessage
                            connections[index].send(userMessage1) 
                            listTracker += 1
                            if (listTracker == len(listA)):
                                client_sock.sendall(multiCommand)
    
                        a += 1
                else:
                    message2 = ("UNKNOWN\n").encode("utf-8")
                    #client_sock.sendall(message2)
                    if (listTracker < len(listA)): 
                            multiCommand += message2
                            listTracker += 1
                            if (listTracker == len(listA)):
                                print(multiCommand)
                                client_sock.sendall(multiCommand)
                    a += 1
        
            else:
                message2 = ("BAD-RQST-HDR\n").encode("utf-8")
                client_sock.sendall(message2)
                a += 1
                continue
            

def deleteUser(clientName, client_sock): 
    if client_sock in connections: 
        connections.remove(client_sock)
        if clientName in clients_names:
            clients_names.remove(clientName)
    return

while True:
    client_sock, client_ip_address = sock.accept()
    threading._start_new_thread(newUser,(client_sock,)) 

client_sock.close()
