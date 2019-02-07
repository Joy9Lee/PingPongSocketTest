import events


def format_hex_str(num, num_of_byte):
    return hex(num).replace("0x", "").zfill(num_of_byte*2)


def get_packet_handler(command_code):
    # Local
    if command_code == InitCompleteR.TYPE_CODE:
        return InitCompleteR()
    elif command_code == GameOverR.TYPE_CODE:
        return GameOverR()
    elif command_code == ShootR.TYPE_CODE:
        return ShootR()
    # Unity
    elif command_code == ResultR.TYPE_CODE:
        return ResultR()
    elif command_code == GameStartR.TYPE_CODE:
        return GameStartR()
    elif command_code == ShutDownR.TYPE_CODE:
        return ShutDownR()
    else:
        print("Receive wrong type: ", command_code)


class ReceivePacket:
    TYPE_CODE = None

    def __init__(self):
        self.payload = None
        self.length = 0

    def get_payload(self, payload):
        self.payload = payload

    def handle(self):
        pass


""" Unity to Local Received packet """


class InitCompleteR(ReceivePacket):
    TYPE_CODE = "00"

    def __init__(self):
        self.length = 0

    def handle(self):
        events.init_complete.set()
        # print("初始化完毕")


class GameOverR(ReceivePacket):
    TYPE_CODE = "02"

    def __init__(self):
        self.length = 0

    def handle(self):
        events.game_over.set()
        # print("游戏结束")


class ShootR(ReceivePacket):
    TYPE_CODE = "03"

    def __init__(self):
        self.length = 2

    def handle(self, payload):
        # print("开始发球")
        number = payload[0]
        times = payload[1]
        # print("游戏开始: %d" % self.game_mode)
        events.shoot.set(number, times)


''' Local to Unity received packet '''


class ResultR(ReceivePacket):
    TYPE_CODE = "10"

    def __init__(self):
        self.length = 6

    def handle(self, payload):
        x = payload[0] * 255 + payload[1]
        y = payload[2] * 255 + payload[3]
        v = payload[4] * 255 + payload[5]
        # print("回球结果)
        events.result.set(x, y, v)


class ShutDownR(ReceivePacket):
    TYPE_CODE = "11"

    def __init__(self):
        self.length = 0

    def handle(self):
        # print("程序关闭")
        events.shut_down.set()


class GameStartR(ReceivePacket):
    TYPE_CODE = "12"

    def __init__(self):
        self.length = 1

    def handle(self, payload):
        game_mode = payload[0]
        # print("游戏开始: %d" % self.game_mode)
        events.game_start.set(game_mode)


''' Send Packet'''


class SendPacket:
    SYNC = 'AA44'

    def __init__(self):
        self.command_code = None
        self.payload_code = None
        self._combine_code()

    def _combine_code(self):
        if self.payload_code:
            hex_str = self.SYNC + self.command_code + self.payload_code
        else:
            hex_str = self.SYNC + self.command_code
        self._bytes = bytes.fromhex(hex_str)

    def bytes(self):
        return self._bytes


""" Unity to Local sent packet """


class InitCompleteS(SendPacket):
    def __init__(self):
        self.command_code = "00"
        self.payload_code = None
        self._combine_code()


class GameOverS(SendPacket):
    def __init__(self):
        self.command_code = "02"
        self.payload_code = None
        self._combine_code()


class ShootS(SendPacket):
    def __init__(self, number, times):
        self.command_code = "03"
        number_hex_str = format_hex_str(number, 1)
        time_hex_str = format_hex_str(times, 1)
        self.payload_code = number_hex_str + time_hex_str
        self._combine_code()


""" Local to Unity sent packet """


class GameStartS(SendPacket):
    def __init__(self, game_mode):
        self.command_code = "12"
        self.payload_code = format_hex_str(game_mode, 1)
        self._combine_code()


class ShutDownS(SendPacket):
    def __init__(self):
        self.command_code = "11"
        self.payload_code = None
        self._combine_code()


class ResultS(SendPacket):
    def __init__(self, x, y, v):
        self.command_code = "10"
        x_hex_str = format_hex_str(x, 2)
        y_hex_str = format_hex_str(y, 2)
        v_hex_str = format_hex_str(v, 2)
        self.payload_code = x_hex_str + y_hex_str + v_hex_str
        self._combine_code()


