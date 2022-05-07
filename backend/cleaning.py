from priority import *
import pandas as pd

node = pd.read_csv('data/Node.csv')

link = pd.read_csv('data/Link.csv')

# 可能的方法：

# 高优先级节点 node_priority[node['type']]==1       98.7%
# 空的 industry                                    13.8%
# 低优先级的 relation                               87.8%

# 按下划线分隔
nodespl = pd.merge(
    node, 
    node['id'].str.rsplit('_',1,expand=True),
    how='left', left_index=True, right_index=True)

# 计算优先级
nodespl['priority'] = nodespl[0].apply(lambda x: node_priority[x])

# 优先级为 1
nodefil = nodespl[nodespl['priority'] == 1]

## 行业不为空
nodefil = nodefil[nodespl['industry'] != '[]']

# 联系
linkspl = pd.merge(link, pd.merge(link['source'].str.rsplit('_',1,expand=True), link['target'].str.rsplit('_',1,expand=True), how='left', left_index=True, right_index=True), how='left', left_index=True, right_index=True)

linkspl['x_p'] = linkspl['0_x'].apply(lambda x: node_priority[x])
linkspl['y_p'] = linkspl['0_y'].apply(lambda x: node_priority[x])
linkfil = linkspl[(linkspl['x_p']==1) & (linkspl['y_p']==1)]

# 根据节点列表筛选边
linkfil = linkfil[(linkfil['source'].isin(nodefil['id'])) & (linkfil['target'].isin(nodefil['id']))]

# 图密度 = 1e-06 Sparse
density = 2 * len(linkfil) / (len(nodefil) * (len(nodefil) - 1))

# 输出
nodefil[['id','name','type','industry']].to_csv('data/Nodefil.csv')
linkfil[['relation','source','target']].to_csv('data/Linkfil.csv')
