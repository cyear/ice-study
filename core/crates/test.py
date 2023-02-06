from Progress import ibar
import time
bar = ibar("ice", 100)
for i in bar:
    if i == bar.end:
        break
    time.sleep(0.1)
