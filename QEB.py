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
            QEBrsFile = open('QEB.bin', 'rb+')
            Message = b'Hello World!'
            QEBrsFile.seek(7)
            QEBrsFile.write(Message)
            QEBrsFile.close()
            QEBrsFile = open('QEB.bin', 'rb+')
            QEBrsFile.seek(2)
            QEBrsFile.write(len(Message).to_bytes(5, 'big'))
            QEBrsFile.close()
        if Request == bytes.fromhex('f0'):
            QEBrsFile = open('QEB.bin', 'rb')
            QEBrsFile.seek(2)
            LEN = int.from_bytes(QEBrsFile.read(5), 'big')
            QEBrsFile.close()
            QEBrsFile = open('QEB.bin', 'rb')
            QEBrsFile.seek(7)
            Filename = QEBrsFile.read(LEN)
            QEBrsOFile = open(str(Filename, encoding='utf-8'), 'rb')
            Data = QEBrsOFile.read()
            QEBrsOFile.close()
            QEBrsFile = open('QEB.bin', 'rb+')
            QEBrsFile.seek(7)
            QEBrsFile.write(Data)
            QEBrsFile.close()
            QEBrsFile = open('QEB.bin', 'rb+')
            QEBrsFile.seek(2)
            QEBrsFile.write(len(Data).to_bytes(5, 'big'))
            QEBrsFile.close()
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
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(7)
    Data = QEBrsFile.read(LEN)
    QEBrsFile.close()
    return Data
def QEBWriteRequest(Filename):
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(2)
    QEBrsFile.write(len(Filename).to_bytes(5, 'big'))
    QEBrsFile.close()
    QEBrsFile = open('QEB.bin', 'rb+')
    QEBrsFile.seek(7)
    QEBrsFile.write(Filename)
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
                QEBWriteRequest(bytes(Filename, encoding='utf-8'))
                QEBRequest(Request)
                Response = [True]
                while Response[0] == True:
                    Response = QEBAwaitingRequest(False)
                while QEBAwaitingFinishedRequest() == True:
                    pass
                QEBFile = open(Filename, 'wb')
                QEBFile.write(QEBReadResponse())
                QEBFile.close()
            QEBOverWriteZero()
    except KeyboardInterrupt:
        QEBRequest(bytes.fromhex('01'))
if __name__ == '__main__':
    if QEBIsHost():
        Server()
    else:
        Client()
