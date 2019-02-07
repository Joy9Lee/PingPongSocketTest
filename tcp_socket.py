import socket
import threading
import packet


class TcpSocket:
    def __init__(self, ip, port):
        self.ip_port = (ip, port)
        self.socket = socket.socket()
        self.conn = None
        self._listener_thread = threading.Thread(target=self._listener)

    def _wait_sync(self):
        while True:
            sync = self.conn.recv(1)
            if sync == bytes.fromhex('AA'):
                sync = self.conn.recv(1)
                if sync == bytes.fromhex('44'):
                    break
            print(sync)

    def _listener(self):
        while True:
            self._wait_sync()
            type_code = self.conn.recv(1).hex()
            print("received type_code: %s" % type_code)
            packet_handler = packet.get_packet_handler(type_code)
            if packet_handler.length > 0:
                payload = self.conn.recv(packet_handler.length)
                packet_handler.handle(payload)
            else:
                packet_handler.handle()

    def run(self):
        self._custom_init()
        self._listener_thread.start()

    def send(self, packet_):
        data = packet_.bytes()
        self.conn.sendall(data)

    def _custom_init(self):
        pass

    def release(self):
        self.socket.close()
        self.conn.close()


class TcpClient(TcpSocket):
    def _custom_init(self):
        print("start to connect")
        self.socket.connect(self.ip_port)
        print("connect OK")
        self.conn = self.socket


class TcpServer(TcpSocket):
    def _custom_init(self):
        print("wait connected")

        self.socket.bind(self.ip_port)
        self.socket.listen(5)
        self.conn, addr = self.socket.accept()
        print('%s connected' % addr[0])



