import socket

MASTER_SERVER = 'muchomath.us.to'
PORT = 5001
KEY = b'0kXMZqwpoAgRUqOXk2Tjsubd1qndPyGR'
NUL = b'\0'

class SocketCommunicator:
    @staticmethod
    def server():
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((socket.gethostname(), PORT))
        serversocket.listen(1)
        serversocket = serversocket

        connected = False
        while not connected:
            (sock, addr) = serversocket.accept()
            client = SocketCommunicator(sock)
            message = client.read_to_nul()
            if message == KEY:
                connected = True
        return client

    @staticmethod
    def client():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((MASTER_SERVER, PORT))
        client = SocketCommunicator(sock)
        client.send_nul(KEY)
        return client

    def __init__(self, sock):
        self.buffer = b''
        self.sock = sock

    def read_to_nul(self):
        while self.buffer.find(NUL) < 0:
            chunk = self.sock.recv(1024)
            if chunk == '':
                break
            self.buffer += chunk
        index = self.buffer.find(NUL)
        if index >= 0:
            message = self.buffer[:index]
            self.buffer = self.buffer[index+1:]
            return message
        return b''

    def send_nul(self, message):
        self.sock.send(message + NUL)

if __name__ == '__main__':
    import threading

    def start_server():
        print('starting server')
        server = SocketCommunicator.server()
        print('server connected')

    def start_client():
        print('starting client')
        #client = SocketCommunicator.client()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((socket.gethostname(), PORT))
        client = SocketCommunicator(sock)
        client.send_nul(KEY)
        print('client key sent')

    st = threading.Thread(target=start_server, name='server')
    ct = threading.Thread(target=start_client, name='client')
    st.start()
    ct.start()
    st.join()
    ct.join()
    print('done')

