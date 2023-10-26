import socket
import threading
import time
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostport =  ("localhost", 8080)                           #("18.195.107.195", 5378)        #("192.168.1.35", 8080)                
sock.connect(hostport)
userCommand = "dummy"

username = input("Pick a username: ")
loginSession= ("HELLO-FROM " + username + " \n ").encode("utf-8")
sock.sendall(loginSession)
string = ""
while True:
        read,write,error = select.select([sock],[],[],0.1)
        if read:
                buffer = sock.recv(1024).decode("utf-8")
                string += buffer
                if(buffer == "BAD-RQST-BODY\n" or  buffer == "IN-USE\n" or buffer == "BAD-RQST-HDR\n"):
                        break
        if not read:
                buffer = string
                break

class messageCheck():
        def __init__(self):
                usersThread = threading.Thread(target = self.nonstop,args = (buffer,) )
                usersThread.daemon = True
                usersThread.start()

        def nonstop(self,buffer):
                while True:
                        newLine = 0
                        multipleMessages = ""
                        echoMessage = False
                        read,write,error = select.select([sock],[sock],[sock],0.1)
                        if read:
                                buffer = sock.recv(4096)
                                dummy = buffer.decode("utf-8")
                                dummy = dummy.replace("\n", "±")
                                for a in range(0,len(buffer)):
                                        if (dummy[a] == '±'):
                                                newLine += 1

                                if (buffer.find(b'echobot') != -1):
                                        echoMessage = True

                                if (buffer.find(b'DELIVERY') != -1 and (newLine == 1 or echoMessage == True)):
                                        echoMessage = False
                                        message = buffer.decode("utf-8")
                                        print("\nIncoming message from User: @" + message[9:len(message)])
                                        print("\nEnter a command: ", end = "")
                                elif (newLine > 1):
                                        print("\nWARNING: MULTIPLE MESSAGES SENT BY THE SERVER")
                                        multipleMessages = buffer.decode("utf-8")
                                        multipleMessages = multipleMessages.replace("\n", "±")
                                        firstCheck = True
                                        secondCheck = True
                                        thirdCheck = True
                                        fourthCheck = True
                                        fifthCheck = True
                                        while (newLine > 0):
                                                if (multipleMessages.find("DELIVERY") != -1 and firstCheck == True):
                                                        firstCheck = False
                                                        newLine -= 1
                                                        index = multipleMessages.find("DELIVERY") + 8
                                                        print("\nIncoming message from user: ", end = "")
                                                        while (index != "±" and index < len(multipleMessages) - 1):
                                                                if (index != "±"):
                                                                        print(multipleMessages[index], end = "")
                                                                index += 1
                                                        print("\n")
                                                elif (multipleMessages.find("WHO-OK") != -1 and secondCheck == True):
                                                        secondCheck = False
                                                        newLine -= 1
                                                        activeUsers = ("WHO\n").encode("utf-8")
                                                        sock.sendall(activeUsers)
                                                        buffer = sock.recv(4096)
                                                        if (buffer == b'BAD-RQST-HDR\n' ):
                                                                print("\nOops, seems like something went wrong. Try again! \n")
                                                        else:   
                                                                print("\nUsers currently online:")
                                                                dummyList = buffer.decode("utf-8")
                                                                tempString = ""
                                                                i = 7
                                                                tracker = 1     
                                                                while (i < len(dummyList)):
                                                                        while (dummyList[i] != "," and i < len(dummyList) - 1):
                                                                                tempString += dummyList[i]
                                                                                i += 1
                                                                        i+=1
                                                                        print("{}".format(tracker) + ") " + tempString, end = " ")
                                                                        tracker +=1
                                                                        tempString = ""
                                                        print("\n")
                                                elif (multipleMessages.find("SEND-OK") != -1) and thirdCheck == True:
                                                        thirdCheck = False
                                                        print("Your message was sent successfully \n")
                                                        newLine -= 1
                                                elif (multipleMessages.find("HELLO") != -1 and fourthCheck == True):
                                                        fourthCheck = False
                                                        newLine -= 1
                                                        index = multipleMessages.find("HELLO") + 6
                                                        username = ""
                                                        while (index != "±" and index < len(multipleMessages) - 1 and multipleMessages[index] != " "):
                                                                username += multipleMessages[index]
                                                                index += 1
                                                        print("Hello " + username[0:len(username) - 1] + "\n")
                                                elif (multipleMessages.find("UNKNOWN") != -1 and fifthCheck == True):
                                                        fifthCheck = False
                                                        print("The user is currently offline\n")
                                                        newLine -= 1
                                        if (newLine == 0):
                                                print("\nEnter a command: ", end = "")
                        time.sleep(0.5)                                                        

if (buffer.find('BUSY\n') != -1 ):
        print("The server is full at the moment, please try again at a later time.")
        userCommand = "!quit"
        sock.close()
elif (buffer != 'IN-USE\n' and buffer != 'BAD-RQST-BODY\n'):
        dummyString = buffer
        printString = dummyString[0:len(dummyString) - 1]
        print(printString)

while (buffer == 'IN-USE\n' or buffer == 'BAD-RQST-BODY\n'):
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(hostport)

        if (buffer == 'IN-USE\n'):
            print("Oops! Error occured: Username Taken.")
        else:
            print("That doesn't look good, your username can only contain letters!")
        username = input("Pick another username: ")
        loginSession= ("HELLO-FROM " + username + " \n ").encode("utf-8")
        sock.sendall(loginSession)
        buffer = sock.recv(512).decode("utf-8")
        if (buffer != 'IN-USE\n' and buffer != 'BAD-RQST-BODY\n'):
                dummyString = buffer
                printString = dummyString[0:len(dummyString) - 1]
                print(printString)

  
def userChat():
        dummyMessage = buffer.decode("utf-8")
        print(datetime.strftime() + "INCOMING MESSAGE FROM USER: @" + dummyMessage[9:len(dummyMessage)])


if (buffer.find("BUSY") == -1):
        activeUsers = ("WHO\n").encode("utf-8")
        sock.sendall(activeUsers)
        buffer = sock.recv(2048)

while (userCommand != "!quit"):  
        messageCheck()
        
        if (userCommand == "dummy"):
                userCommand = input("Enter a command (!help for commands list.): ")
        elif (buffer.find('DELIVERY') != -1):
                time.sleep(0.5)
                userCommand = input("Enter a command: ")
        else:
                userCommand = input("Enter a command: ")

        while (userCommand == ""):
                print("Please type a command first!")
                userCommand = input("Enter a command: ")

        if (userCommand == "!help"):
            print("\nType !who to see all the users that are currently online.")
            print("Type @username to message somebody online.")
            print("Type !quit to exit the program.\n")

        if (userCommand == "!test"):
                testing = ("TEST").encode("utf-8")
                sock.sendall(testing)
        if (userCommand == "!server"):
                serverTest = ("WHO\n SEND\n ")                
        
        if (userCommand == "!who"):
                activeUsers = ("WHO\n").encode("utf-8")
                sock.sendall(activeUsers)
                string = ""
                while True:
                        read,write,error = select.select([sock],[],[],0.1)
                        if read:
                                buffer = sock.recv(1024).decode('utf-8')
                                string += buffer
                                check = False
                                check2 = False
                                if (buffer.find('BAD-RQST-HDR') != -1 ):
                                        check = True
                                if (buffer.find('BAD-RQST-BODY') != -1 ):
                                        check = True
                                if (check == True or check2 == True):
                                        break
                        if not read:
                                dummyList = string
                                break
                if (buffer == 'BAD-RQST-HDR\n' ):
                        print("\nOops, seems like something went wrong. Try again! \n")
                else:   
                        print("\nUsers currently online:")
                        dummyList = buffer
                        tempString = ""
                        i = 7
                        tracker = 1
                        while (i < len(dummyList)):
                                while (dummyList[i] != "," and i < len(dummyList) - 1):
                                        tempString += dummyList[i]
                                        i += 1
                                i+=1
                                print("{}".format(tracker) + ") " + tempString, end = " ")
                                tracker +=1
                                tempString = ""
                        print("\n")

        if (len(userCommand) > 1):        
                if (userCommand[0] == "@"):
                        i = 1
                        receiver = ""
                        msg = ""
                        numGab = 0
                        while (i < len(userCommand)):
                                if ((userCommand[i] == " ") and (numGab == 0)):
                                        receiver = msg 
                                        msg = ""
                                        i += 1
                                        numGab = 1
                                else:
                                        msg += userCommand[i] 
                                        i += 1
                        activeUsers = ("SEND " + receiver + " " + msg + "\n").encode("utf-8")
                        sock.sendall(activeUsers)
                        string = ""
                        while True:
                                read,write,error = select.select([sock],[],[],0.1)
                                if read:
                                        buffer = sock.recv(1024).decode("utf-8")
                                        string += buffer
                                        if (buffer == "SEND-OK\n" or buffer == 'UNKNOWN\n' or buffer == "BAD-RQST-HDR\n" or buffer == "BAD-RQST-BODY\n"):
                                                break
                                if not read:
                                        buffer = string
                                        break
                        if (buffer == 'SEND-OK\n'):
                                print("\nYour message has been delivered \n")
                        elif (buffer == 'UNKNOWN\n'):
                                print("\nIt appears the user is offline, please try again later.\n")
                        elif (buffer == 'BAD-RQST-BODY\n'):
                                print("\nOops, looks like you are trying to send an empty message. Type something!\n")
                        else:   
                                messageCheck()
                                print("Debugging: " + str(buffer))
        
        if (userCommand == "!quit"):
                print("Program exiting... See you soon!")


        
        

sock.close()