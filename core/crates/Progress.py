import os, time

class ibar:
    def __init__(self,title="ice", max=100) -> None:
        self.max = max
        self.end = '\0'
        self.title = title
        self.columns =  os.get_terminal_size().columns
        self.time = time.time()
        # self.bar = 0
    def __iter__(self):
        self.bar = 0
        return self
    def __next__(self):
        n = self.bar
        m = n / self.max
        sp = 40
        s = round(((time.time() - self.time) * (self.max - self.bar)), 2)
        print(f"{round(m*100, 2)}%|{'█'*int(m*sp)}{'░'*(sp-int(m*sp))}|{self.title} < {s}s{' '*5}", end="\r")
        self.bar += 1
        self.time = time.time()
        if self.bar >= self.max:
            return '\0'
        return n
