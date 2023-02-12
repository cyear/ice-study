# 闲来无事制作的log显示
# 兼容 Windiws
import os, time, sys
'''
FATAL #重大错误
ERROR #错误提示
WARN #潜在错误
INFO #普通信息
DEBUG #调试信息
------04.18------
添加了LINE输出调用日志的行数
添加了MODEL输出调用日志的函数
FATAL日志下添加了\a警告
添加了日志写入功能
添加了日志写入大小限制
添加了PATH输出调用日志的文件
添加了日志时间显示设置
优化不换行输出(\r)
------04.19------
'''
class iLog:
    FATAL = 4
    ERROR = 3
    WARN = 2
    INFO = 1
    DEBUG = 0
    YES = 1
    NO = 0
    LINE = 0 #1 输出行数
    MODEL = 0 #1 输出函数
    SIZE = 10240 #最大保存日志大小KB
    PATH = 0 #1 输出运行文件名称
    TIME = 1 #0 关闭日志显示时间
    def __init__(self, level: int = 1, file: str = None):
        self.file = file
        self.level = level
        self.widths = [(126, 1), (159, 0), (687, 1), (710, 0), (711, 1),(727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0), (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1), (8426, 0), (9000, 1), (9002, 2), (11021, 1), (12350, 2), (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1), (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0), (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2), (120831, 1), (262141, 2), (1114109, 1)]
    #公有
    def log(self, text: str, level: int = 1, end: str = "\n"):
        line = sys._getframe(1).f_lineno
        model = sys._getframe(1).f_code.co_name
        path = sys._getframe(1).f_code.co_filename.split("/")[-1]
        hms = time.strftime("%H:%M:%S", time.localtime(time.time()))
        text = self._c(text, hms, level, line, model, path)
        self._file(text, model)
        if level < self.level:
            return self.NO
        os.system("")
        print(text, end = end)
        return self.YES
    def error(self, e):
        self.log(e, 4)
        quit(255)
    #私有
    def w(self, text: str):
        def w(char):
            o = ord(char)
            if o == 0xe or o == 0xf:
                return 0
            for num, wid in self.widths:
                if o <= num:
                    return wid
        n = 0
        for i in text:
            n += w(i)
        return n
    def _file(self, text, model):
        if self.file != None:
            with open(self.file, "a+") as a:
                a.write(text[7:-4]+"\n")
            file_size = os.path.getsize(self.file) / 1024
            if file_size > self.SIZE and model != "_file":
                self.log(f"日志大小已到达: {round(file_size,2)}/{self.SIZE}KB 执行删除",2)
                with open(self.file, "r+") as w:
                    w.truncate()
    def _c(self, text: str, hms: str, level: int, line: int, model: str, path: str):
        line = f":{line}" if self.LINE else ""
        model = "" if model == "<module>" else f"({model})" if self.MODEL else ""
        path = f"-{path}" if self.PATH else ""
        hms = "-" + hms if self.TIME else ""
        return \
            {
                self.DEBUG: f"\033[1;38m[DEBUG{hms}{path}{model}{line}] {text}\033[0m", #白色
                self.INFO: f"\033[1;32m[INFO{hms}{path}{model}{line}] {text}\033[0m", #绿色
                self.WARN: f"\033[1;33m[WARN{hms}{path}{model}{line}] {text}\033[0m", #黄色
                self.ERROR: f"\033[1;35m[ERROR{hms}{path}{model}{line}] {text}\033[0m", #紫色
                self.FATAL: f"\033[1;31m[FATAL{hms}{path}{model}{line}] {text}\033[0m" #红色
            }[level]
#logn._w函数参考于urwid计算宽度源码
