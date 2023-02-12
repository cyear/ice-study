import os
from Log import iLog
Length = iLog().w
class TprogressBar:
    def __init__(self) -> None:
        self.diagonal = '+'
        self.wh = ('-', '|')
    def new(self, array):
        '''
        Display on the left side of the next line
                          |
            Left display  |
                  |       |
        array = [(a, b), (c, d)]
                     |
                Right display
        '''
        cache = ""
        def msg(arr):
            return "{0}{1:{3}<12}{0:{3}^5}{2:{3}^12}{0:{3}>5}".format(self.wh[1], arr[0], arr[1], chr(12288))
        cache = ""
        for i in array:
            message = msg(i)
            if Length(cache) < Length(message):
                cache = message
        msg_s = self.diagonal
        w = Length(cache)
        for i in range(Length(cache)):
            msg_s += self.wh[0]
            if Length(msg_s) >= w - 1:
                msg_s += self.diagonal
                break
        message = msg_s
        for i in array:
            message += f"\n{msg(i)}"
        message += f"\n{msg_s}"
        cache = message.split("\n")
        message = ""
        c = ""
        for i in cache:
            c = i
            while(Length(c)<Length(cache[0])):
                c = c[:-1] + " " + self.wh[1]
            message += c + "\n"
        print(message[:-1])
        # for i in message.split("\n"):
            # print(i, Length(i))

