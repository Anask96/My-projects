import socket
import dns.resolver
import time
import threading
from operator import attrgetter

ip = "127.0.0.1"
port = 53

#Global var for checking
checker = 1
#Cache memory containers
IPCache = []
domainCache = []
cacheMemory = []
extraContainer = []

#Best server containers
timesList = []

#Roots and names containers 
nameServers = []
nameServerList = []

class Domein_in_cashe:
    pass

class Times_list:
    pass

ROOT_SERVERS = [  "198.41.0.4",
                    "199.9.14.201",
                    "192.33.4.12",
                    "199.7.91.13",
                    "192.203.230.10",
                    "192.5.5.241",
                    "192.112.36.4",
                    "198.97.190.53",
                    "192.36.148.17",
                    "192.58.128.30",
                    "193.0.14.129",
                    "199.7.83.42",
                    "202.12.27.33"
]


def buildFlags(userData):    
    QR = '1'

    extractByte1 = bytes(userData[0:1])
    extractByte2 = bytes(userData[1:2])
    OPCODE = ''
    for bits in range(1,5):
        OPCODE += str(ord(extractByte1)&(1<<bits))
    AA = '0'
    TC = '0'
    RD = '0'
    Z = '000'
    RCODE = '0000'

    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder = 'big') + int(Z+RCODE,2).to_bytes(1, byteorder = 'big')

def getQuestionDomain(userData):
    state = 0
    expectedLength = 0
    domainStr = ''
    domainList = []
    x = 0
    y = 0 

    for byte in userData:
        if (state == 1):
            if (byte != 0):
                domainStr += chr(byte)
            x += 1
            if (x == expectedLength):
                domainList.append(domainStr)
                state = 0
                x = 0
                domainStr = ''
            if (byte == 0):
                domainList.append(domainStr)
                break
        else:
            state = 1
            expectedLength = byte
        y += 1 

    questionType = userData[y:y+2]

    return (domainList, questionType)

def checkingDomein():
    delete = ""
    nothing = {}
    while True:
        for data in cacheMemory:
            if delete == "delete":
                cacheMemory.remove(nothing)
                delete = ""
            time.sleep(2)
            t3 = time.time()
            timeVar = int(t3 - data.timeInServer)
            if timeVar > 3600:
                #delete = "delete"
                cacheMemory.remove(data)

threading._start_new_thread(checkingDomein,())

def getRecs(userData):
    domain, questionType = getQuestionDomain(userData)
    qt = ''
    TLD = domain[1] + '.'
    domainName = '.'.join(domain)
    

    if (questionType == b'\x00\x01' or questionType == b'\x00\x0f'):
        qt = 'NS'

    for data in cacheMemory:
        if questionType == b'\x00\x01':
            qt = 'A'
        if questionType == b'\x00\x0f':
            qt = 'MX'
        if data.name == domainName:
            if data.requestType == qt:
                qt = data.requestType
                yo = data.server
                query = dns.message.make_query(domainName,qt)
                try:
                    response = dns.query.udp(query, str(yo), timeout = 0.1)
                except:
                    continue
                if response.answer:
                    webIP = ''
                    domainIP = str(response.answer[0])
                    domainIP = domainIP.split(' ')
                    if (domainIP[3] == "A"):
                        dotCounter = 0
                        for i in range(0, len(domainIP[4])):
                            if (domainIP[4][i].isdigit() or domainIP[4][i] == '.'):
                                if (domainIP[4][i] == '.'):
                                    dotCounter += 1
                                if (dotCounter < 4):
                                    webIP += domainIP[4][i]
                    elif (domainIP[3] == "MX"):
                        webIP = domainIP[4] + "."
                        dotCounter = 0
                        for i in range(0, len(domainIP[5])):
                            if (domainIP[5][i] == '.'):
                                dotCounter += 1
                            if (domainIP[5][i].isalnum and dotCounter < 4):
                                webIP += domainIP[5][i]
                        webIP = webIP + "."
                    if webIP not in IPCache:
                        IPCache.append(webIP)
                answerCount = len(IPCache).to_bytes(2, byteorder = 'big')
                return (qt, domain, answerCount)
    answerCount = 0
    i = 0
    for servers in ROOT_SERVERS:
        query = dns.message.make_query(TLD,qt)
        response = dns.query.udp(query, servers)
        rootIP = str(response.additional[0])
        rootIP = rootIP.split(' ')
        query = dns.message.make_query(domainName, qt)
        response = dns.query.udp(query, rootIP[4])

        if (len(response.additional) > 0):
            for x in range(0, len(response.additional)):
                nameServer = str(response.additional[x])
                index = nameServer.find("A") + 1
                if (nameServer[index] != "A"):
                    nameServer = nameServer[index + 1:]
                    if nameServer not in nameServerList:
                        nameServerList.append(nameServer)
        
        if (questionType == b'\x00\x01'):
            qt = 'A'
        elif (questionType == b'\x00\x0f'):
            qt = 'MX'
        
        for x in range(0, len(nameServerList)):
            t1 = time.time()
            query = dns.message.make_query(domainName,qt)
            try:
                response = dns.query.udp(query, str(nameServerList[x]), timeout = 0.1)
            except:
                continue
            if response.answer:
                webIP = ''
                domainIP = str(response.answer[0])
                domainIP = domainIP.split(' ')
                if (domainIP[3] == "A"):
                    dotCounter = 0
                    for i in range(0, len(domainIP[4])):
                        if (domainIP[4][i].isdigit() or domainIP[4][i] == '.'):
                            if (domainIP[4][i] == '.'):
                                dotCounter += 1
                            if (dotCounter < 4):
                                webIP += domainIP[4][i]
                elif (domainIP[3] == "MX"):
                    webIP = domainIP[4] + "."
                    dotCounter = 0
                    for i in range(0, len(domainIP[5])):
                        if (domainIP[5][i] == '.'):
                            dotCounter += 1
                        if (domainIP[5][i].isalnum and dotCounter < 4):
                            webIP += domainIP[5][i]
                    webIP = webIP + "."
                if webIP not in IPCache:
                    IPCache.append(webIP)
        
        t2 = time.time()
        tim = str(t2-t1)
        if (len(timesList) < 13):
            newTime = Times_list()
            newTime.server = nameServerList[x]
            newTime.time = tim
            timesList.append(newTime)

    answerCount = len(IPCache).to_bytes(2, byteorder = 'big') 

    timesList.sort(key = attrgetter('time'))

    check = 0
    
    if IPCache:
        for data in cacheMemory:
            if domainName == data.name:
                if data.requestType == qt:
                    check = True

        if check == False:
            newDomain = Domein_in_cashe()                                               #Each new domain has the following atterbutes:
            newDomain.name = domainName                                                 #Domain name it self
            newDomain.numIp = len(nameServerList)                                              #Number of IP address in the cache memory)
            newDomain.timeInServer = time.time()                                        #Time function for removing the domein from cache memory after a specific time 
            newDomain.server = timesList[0].server
            newDomain.requestType = qt
            cacheMemory.append(newDomain)
        timesList.clear()
   
    return (qt, domain, answerCount)

def buildDNSQuestion(domainName, rectype):
    qbytes = b''

    for labels in domainName:
        labelLength = len(labels)
        qbytes += bytes([labelLength])

        for character in labels:
            qbytes += ord(character).to_bytes(1, byteorder = 'big')
        
    if (rectype == "A"):
        qbytes += (1).to_bytes(2, byteorder = 'big')
    elif (rectype == "MX"):
        qbytes += (15).to_bytes(2, byteorder = 'big')

    qbytes += (1).to_bytes(2, byteorder = 'big')

    return qbytes

def rectobytes(domainName, recType, record, isInside):
    global checker
    rbytes = b'\xc0\x0c'
   
    if (recType == 'A'):
        rbytes = rbytes + bytes([0]) + bytes([1])
    elif (recType == 'MX'):
        rbytes = rbytes + bytes([0]) + bytes([15])
        
    rbytes = rbytes + bytes([0]) + bytes([1])

    rbytes += (200).to_bytes(4, byteorder = 'big')
    
    if (recType == 'A'):
        rbytes = rbytes + bytes([0]) + bytes([4])
        for address in record.split('.'):
            rbytes += bytes([int(address)])
    elif (recType == 'MX'):
        prefIndex = record.find('.')
        preference = record[0:prefIndex]
        if (domainName[0] in record):
            index = record.find(domainName[0])
            secondIndex = record.find(domainName[0]) + len(domainName[0])
            if (record[secondIndex] == '.'):
                record = record[prefIndex + 1:index]
            else:
                record = record[prefIndex + 1:]
        if (record[0] == 'g' and record[1] == 'm'):
            dataSize = len(record) + len(preference) + 3
        else:
            dataSize = len(record) + len(preference) + 2
        
        rbytes += (dataSize).to_bytes(2, byteorder = 'big') 
        rbytes = rbytes + bytes([0]) + bytes([int(preference)])
        
        myTuple = (record[:2], record)
        size = 0
        for y in range(0,len(myTuple[1])):
            if ( myTuple[1][y] != '.'):
                size += 1
            else:
                break
        
        firstPass = False
        for i in range(0, len(myTuple[1])):
            if (firstPass == False):
                rbytes += bytes([size])
                size = 0
                firstPass = True
            if (myTuple[1][i] != '.' and firstPass == True):
                rbytes += bytes([ord(myTuple[1][i])])
            elif (myTuple[1][i] == '.'):
                size = 0
                index = i + 1
                if (index >= len(myTuple[1])):
                    break
                else:
                    while (myTuple[1][index] != '.'):
                        size += 1
                        index += 1
                        if (index >= len(myTuple[1])):
                            break
                rbytes += bytes([size])

    if recType == 'MX':
        rbytes += b'\xc0\x0c'

    if recType == "MX":
        if (checker == len(IPCache)):
            checker = 0
            rbytes += bytes([0])
        else:
            checker += 1

    checker = 1
    
    return rbytes
    
def buildResponse (userData, connectionType):
    global checker
    #Get Transaction ID
    if connectionType == "TCP":
        uniqueID = userData[2:4]
    if connectionType == "UDP":
        uniqueID = userData[:2]

    #Get Flags
    if connectionType == "TCP":
        Flags = buildFlags(userData[4:6])
    if connectionType == "UDP":
        Flags = buildFlags(userData[2:4])

    #Question Count
    QDCOUNT = b'\x00\x01'

    #Answer Count
    if connectionType == "TCP":
        rectype, domain, ANCOUNT = getRecs(userData[14:])#[2]
    if connectionType == "UDP":
        rectype, domain, ANCOUNT = getRecs(userData[12:])#[2]

    NSCOUNT = (0).to_bytes(2, byteorder = 'big')

    ARCOUNT = (0).to_bytes(2, byteorder = 'big')

    dnsHeader = uniqueID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT
    
    dnsBody = b''

    dnsQuestion = buildDNSQuestion(domain, rectype)

    isInside = False
    for record in IPCache:
        if (domain[0] in record and domain[1] in record):
            isInside = True
                
    
    for record in IPCache:
        dnsBody += rectobytes(domain, rectype, record, isInside)
    
    if connectionType == 'TCP':
        count = dnsHeader + dnsQuestion + dnsBody

        length = 0
        for byte in count:
            length += 1

        length = (length).to_bytes(2, byteorder = 'big')
    
        return length + dnsHeader + dnsQuestion + dnsBody

    if connectionType == 'UDP':
        return dnsHeader + dnsQuestion + dnsBody

def main(dnsSocket, connectionType):

    while True:
        #Clear lists after use part
        nameServers.clear()
        IPCache.clear()
        
        if (connectionType == "UDP"):
            userData, userAddress = dnsSocket.recvfrom(512)
            print("udp")

        if (connectionType == "TCP"):
            client_sock, userAddress = dnsSocket.accept()
            userData = client_sock.recv(512)
            print("tcp")

        dnsResponse = buildResponse(userData, connectionType)
        if (connectionType == "UDP"):
            dnsSocket.sendto(dnsResponse,userAddress)
        if (connectionType == "TCP"):
            client_sock.send(dnsResponse)

def tcpCon(ip ,port):
    dnsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dnsSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    dnsSocket.bind((ip,port))
    dnsSocket.listen(2)
    connectionType1 = "TCP"
    main(dnsSocket, connectionType1)

def udpCon(ip ,port):
    dnsSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    dnsSocket.bind((ip,port))
    connectionType2 = "UDP"
    main(dnsSocket, connectionType2)

usersThread = threading.Thread(target = tcpCon,args = (ip ,port) )
usersThread.start()

usersThread = threading.Thread(target = udpCon,args = (ip ,port) )
usersThread.start()