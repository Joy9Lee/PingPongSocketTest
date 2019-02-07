from tcp_socket import TcpClient, TcpServer
import time
from packet import InitCompleteS, ShootS, GameOverS
import events

ip = "127.0.0.1"
port = 9000
client = TcpClient(ip, port)
client.run()

# send initialized completed signal
init_packet = InitCompleteS()
client.send(init_packet)

# wait game start signal
game_mode = events.game_start.wait()
print("游戏开始，模式 %d" % game_mode)
events.game_start.clear()

# send shoot command
number = 10      # 20 balls
times = 15       # 10 times per second
shoot_packet = ShootS(number, times)
client.send(shoot_packet)

for i in range(number):
    x, y, v = events.result.wait()
    print("落点: %.2f, %.2f  速度： %d" % (x/100, y/100, v))
    events.result.clear()

# send game over signal
over_packet = GameOverS()
client.send(over_packet)

# wait shut down signal
events.shut_down.wait()
events.shut_down.clear()
print("关闭退出")
exit()

