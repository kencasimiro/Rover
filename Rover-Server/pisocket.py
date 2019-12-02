import socket
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MASTER_SERVER = '192.168.1.3'

PORT = 5001
KEY = b'0kXMZqwpoAgRUqOXk2Tjsubd1qndPyGR'
NUL = b'\0'

class SocketCommunicator:
    @staticmethod
    def server():
        logger.info('starting server...')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info('determining ip address')
        myip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        logger.info('starting server at {myip}'.format(**vars()))
        serversocket.bind((myip, PORT))
        serversocket.listen(1)

        connected = False
        while not connected:
            (sock, addr) = serversocket.accept()
            logger.info('accepting message from {}'.format(addr))
            client = SocketCommunicator(sock)
            message = client.read_to_nul()
            if message == KEY:
                connected = True
            else:
                logger.info('received invalid key: {}'.format(message))
        logger.info('client connection established')
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

