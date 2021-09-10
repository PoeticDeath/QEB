import os
def QEBIsHost():
    QEBrsFile = open('QEB.bin', 'rb')
    QEBrs = QEBrsFile.read(1)
    QEBrsFile.close()
    QEBrsFile = open('QEB.bin', 'rb+')
    if QEBrs == bytes.fromhex('10'):
        QEBrsFile.write(bytes.fromhex('00'))
        QEBrsFile.close()
        return False
    QEBrsFile.write(bytes.fromhex('10'))
    QEBrsFile.close()
    return True
def QEBHasClient():
    QEBrsFile = open('QEB.bin', 'rb')
    ANS = QEBrsFile.read(1)
    QEBrsFile.close()
    if ANS == bytes.fromhex('00'):
        return True
    else:
        return False
def QEBAwaitingRequest(Host):
    QEBrsFile = open('QEB.bin', 'rb')
    QEBrsFile.seek(1)
    Request = QEBrsFile.read(1)
    QEBrsFile.close()
    if Request == bytes.fromhex('00'):
        return [True]
    elif Host == True:
        if Request == bytes.fromhex('ff'):
            Message = b'Hello World!'
            QEBWriteResponse(Message)
        if Request == bytes.fromhex('f0'):
            Filename = QEBReadResponse()
            QEBrsOFile = open(str(Filename, encoding='utf-8'), 'rb')
            Data = QEBrsOFile.read()
            QEBrsOFile.close()
            QEBWriteResponse(Data)
        if Request == bytes.fromhex('0f'):
            Filename = QEBReadResponse()
            QEBFinishRequest()
            QEBRequest(bytes.fromhex('0f'))
            Data = QEBReadResponse()
            QEBrsOFile = open(str(Filename, encoding='utf-8'), 'wb')
            QEBrsOFile.write(Data)
            QEBrsOFile.close()
            QEBFinishRequest()
        return [False, Request]
    else:
        return [False]
def QEBRequest(Request):
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(1)
    QEBrsFile.write(Request)
    QEBrsFile.close()
def QEBReadResponse():
    QEBrsFile = open('QEB.bin', 'rb')
    QEBrsFile.seek(2)
    LEN = int.from_bytes(QEBrsFile.read(5), 'big')
    QEBrsFile.close()
    QEBrsFile = open('QEB.bin', 'rb')
    QEBrsFile.seek(7)
    Data = QEBrsFile.read(LEN)
    QEBrsFile.close()
    return Data
def QEBWriteResponse(Data):
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(2)
    QEBrsFile.write(len(Data).to_bytes(5, 'big'))
    QEBrsFile.close()
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(7)
    QEBrsFile.write(Data)
    QEBrsFile.close()
def QEBAwaitingFinishedRequest():
    QEBrsFile = open('QEB.bin', 'rb')
    QEBrsFile.seek(1)
    if QEBrsFile.read(1) != bytes.fromhex('00'):
        QEBrsFile.close()
        return True
    QEBrsFile.close()
    return False
def QEBFinishRequest():
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(1)
    QEBrsFile.write(bytes.fromhex('00'))
    QEBrsFile.close()
def QEBOverWriteZero():
    QEBrsFile = open('QEB.bin', 'rb')
    QEBrsFile.seek(2)
    LEN = int.from_bytes(QEBrsFile.read(5), 'big')
    QEBrsFile.close()
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(2)
    QEBrsFile.write(bytes.fromhex('00'*6))
    QEBrsFile.close()
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.write(bytes.fromhex('00')*LEN)
    QEBrsFile.close()
def Server():
    print('QEB Hosting Started.')
    while True:
        while QEBHasClient() == False:
            pass
        print('QEB Client Connected.')
        while True:
            Request = [True]
            while Request[0] == True:
                Request = QEBAwaitingRequest(True)
            QEBFinishRequest()
            print(Request[1])
            if Request[1] == bytes.fromhex('01'):
                print('QEB Client Disconnected.')
                QEBIsHost()
                False
def Client():
    print('Connected to QEB Host.')
    try:
        while True:
            Request = bytes.fromhex(input('What is your request? : '))
            if Request == bytes.fromhex('ff'):
                QEBRequest(Request)
                Response = [True]
                while Response[0] == True:
                    Response = QEBAwaitingRequest(False)
                while QEBAwaitingFinishedRequest() == True:
                    pass
                print(QEBReadResponse())
            if Request == bytes.fromhex('f0'):
                Filename = input('Request a File by name : ')
                QEBWriteResponse(bytes(Filename, encoding='utf-8'))
                QEBRequest(Request)
                Response = [True]
                while Response[0] == True:
                    Response = QEBAwaitingRequest(False)
                while QEBAwaitingFinishedRequest() == True:
                    pass
                QEBFile = open(Filename, 'wb')
                QEBFile.write(QEBReadResponse())
                QEBFile.close()
            if Request == bytes.fromhex('0f'):
                Filename = input('Send a File by name : ')
                QEBWriteResponse(bytes(Filename, encoding='utf-8'))
                QEBRequest(Request)
                Response = [True]
                while Response[0] == True:
                    Response = QEBAwaitingRequest(False)
                while QEBAwaitingFinishedRequest() == True:
                    pass
                QEBFile = open(Filename, 'rb')
                Data = QEBFile.read()
                QEBFile.close()
                QEBWriteResponse(Data)
                while QEBAwaitingFinishedRequest() == True:
                    pass
            QEBOverWriteZero()
    except KeyboardInterrupt:
        QEBRequest(bytes.fromhex('01'))
if __name__ == '__main__':
    if QEBIsHost():
        Server()
    else:
        Client()
