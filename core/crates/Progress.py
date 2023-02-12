import os
import time

class ProgressBar:
    def __init__(self, title="ice", max_value=100):
        self.title = title
        self.max_value = max_value
        self.start_time = time.time()
        self.columns = os.get_terminal_size().columns
        self.bar_length = 40
        self.completed = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.completed > self.max_value:
            raise StopIteration
        completion = self.completed / self.max_value
        bar = int(completion * self.bar_length)
        color = int(completion * 100)
        elapsed_time = time.time() - self.start_time
        remaining_time = elapsed_time / completion * (1 - completion) if completion > 0 else 0
        message = f"\033[1;{color}m{completion:.2%}\033[0m|\033[1;{color}m{'█' * bar}\033[0m{'░' * (self.bar_length - bar)}|{self.title} < {elapsed_time:.2f}s/{remaining_time:.2f}s\r"
        print(message, end="", flush=True)
        self.completed += 1
        return self.completed
