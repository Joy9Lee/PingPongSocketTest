from threading import Event
from queue import Queue


class GameStartEvent:
    def __init__(self):
        self.event = Event()
        self.ack = None
        self.mode = None

    def set(self, mode):
        self.event.set()
        self.mode = mode

    def wait(self):
        if self.event.wait():
            return self.mode
        else:
            return None

    def clear(self):
        self.event.clear()


class ShootEvent:
    def __init__(self):
        self.event = Event()
        self.number = None
        self.times = None

    def set(self, number, time):
        self.event.set()
        self.number = number
        self.times = time

    def wait(self):
        if self.event.wait():
            return self.number, self.times
        else:
            return None

    def clear(self):
        self.event.clear()


class ResultEvent:
    def __init__(self):
        self.event = Event()
        self.x = None
        self.y = None
        self.v = None

    def set(self, x, y, v):
        self.event.set()
        self.x = x
        self.y = y
        self.v = v

    def wait(self):
        if self.event.wait():
            return self.x, self.y, self.v
        else:
            return None

    def clear(self):
        self.event.clear()


''' Local events '''
init_complete = Event()
game_over = Event()
shoot = ShootEvent()


''' Unity events '''
game_start = GameStartEvent()
shut_down = Event()
result = ResultEvent()
