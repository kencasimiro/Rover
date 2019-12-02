import atexit
import threading
import logging
from io import BytesIO
from base64 import b64encode
from picamera import PiCamera
from socketIO_client import SocketIO, BaseNamespace
from i2c_backend import PyCar

KEY = b'0kXMZqwpoAgRUqOXk2Tjsubd1qndPyGR'
HOST = '192.168.1.87'
#HOST = 'muchomath.us.to'
PORT = 5000

logging.getLogger('socketIO-client').setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

car = PyCar()


@atexit.register
def neutralize():
    car.control(90, 90)

class RoverNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        BaseNamespace.__init__(self, *args, **kwargs)
        self.camera = PiCamera()
        self.camera.resolution = (384, 216)
        self.buffer = BytesIO()
        self.neutralize_timer = None
        self.capture_timer = None
        self.continue_capture = True
        self.start_neutralize_timer()

    def start_neutralize_timer(self):
        self.neutralize_timer = threading.Timer(1.0, neutralize)
        self.neutralize_timer.start()

    def start_capture_timer(self):
        self.capture_timer = threading.Timer(0.5, self.capture)
        self.capture_timer.start()

    def capture(self):
        self.camera.capture(self.buffer, 'jpeg')
        stream = self.buffer.getvalue()
        data = b64encode(stream).decode()
        self.emit('image', data)
        self.buffer.seek(0)
        self.buffer.truncate()
        if self.continue_capture:
            self.start_capture_timer()
        else:
            self.capture_timer = None

    def on_connect(self):
        logger.info('connected')
        self.continue_capture = True
        self.capture()

    def on_reconnect(self):
        logger.info('reconnected')
        self.continue_capture = True
        self.capture()

    def on_disconnect(self):
        logger.info('disconnected')
        neutralize()
        self.continue_capture = False

    def on_control(self, message):
        if self.neutralize_timer:
            self.neutralize_timer.cancel()
        steering = message.get('steering', 90)
        throttle = message.get('throttle', 90)
        try:
            car.control(steering, throttle)
        except:
            logger.error('Car connection dropped')
        self.start_neutralize_timer()

socketIO = SocketIO(HOST, PORT)
rover_namespace = socketIO.define(RoverNamespace, '/rover')

if __name__ == '__main__':
    socketIO.wait()

