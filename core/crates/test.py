from Progress import ProgressBar
from Tprogress import TprogressBar
import time
# bar = ProgressBar("ice", 100)
# for i in bar:
#     time.sleep(0.1)
array = [
        ("第一单元", "使用Py干倒C++"),
        ("番外篇", "C++性能低于Py"),
        ("进阶", "Sql重构Go"),
        ("修仙篇", "Java重制乌班图")
        ]
bar = TprogressBar().new(array)
