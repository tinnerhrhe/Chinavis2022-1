from priority import *
import pandas as pd

node = pd.read_csv('data/Node.csv')

link = pd.read_csv('data/Link.csv')

# 可能的方法：

# 高优先级节点 node_priority[node['type']]==1
# 空的 industry
# 低优先级的 relation