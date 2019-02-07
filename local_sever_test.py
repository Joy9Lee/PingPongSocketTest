from tcp_socket import TcpClient, TcpServer
import events
from packet import GameStartS, ShutDownS, ResultS
import time

ip = "127.0.0.1"
port = 9000
server = TcpServer(ip, port)
server.run()

result_list = [
    # x, y ,v
    (120, 110, 100),
    (0, 0, 0),
    (20, 50, 200),
    (40, 10, 330),
    (90, 43, 230),
    (130, 123, 120),
    (110, 154, 130),
    (60, 11, 90),
    (60, 11, 90),
    (60, 11, 90)

]

# wait unity initialized completed
events.init_complete.wait()
events.init_complete.clear()
print("Unity初始化完毕")

# send the game start command
game_start_packet = GameStartS(2)
server.send(game_start_packet)

# wait game over signal
number, times = events.shoot.wait()
events.shoot.clear()
print("发%d球，每秒%d球" % (number, times/10))

# send result
for i in range(number):
    result_packet = ResultS(result_list[i][0], result_list[i][1], result_list[i][2])
    server.send(result_packet)
    time.sleep(10.0/times)

# wait game over signal
events.game_over.wait()
events.game_over.clear()
print("游戏结束")

# send shut down command
shut_down_packet = ShutDownS()
server.send(shut_down_packet)
exit()
