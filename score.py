import numpy as np
import os
import pandas as pd
from utils import *
#feature: 1.number of weighted neighbors(all types) 2. rules for elimination
# 3.(possible) consider jumps and corresponding neighbors
# method: record and iterate scores
def process_data():
    node = pd.read_csv('data/Node.csv')
    link = pd.read_csv('data/Link.csv')
    # select data without nan
    node = node.dropna()
    node = node.drop_duplicates('id', keep='first')
    link = link.dropna()
    link = link.drop_duplicates()
    #id = np.array(node.index.values)
    #type = np.array(type_value[node['type'][i]] for i in range(node.shape[0]))
    industry = np.array(0 if node['industry'][i] == '[]' else 1 for i in range(node.shape[0]))
    scores = []
    domains = []
    for i, s in enumerate(node['id']):
        score = 0
        ips = 0
        for j, t in enumerate(link['source']):
            if s == t:
                type = link.iloc[j, 0]
                if s == 'Domain':
                    if type == 'r_dns_a':
                        ips += 1
                    score += d_weight(type, i, industry)
                elif s == 'IP':
                    score += ip_weight(type, i, industry)
                elif s == 'cert':
                    score += c_weight(type, i, industry)
            if s == link.iloc[j, 2]:
                type = link.iloc[j, 0]
                if s == 'IP':
                    score += ip_weight(type, i, industry)
                elif s == 'cert':
                    score += c_weight(type, i, industry)
        if ips > 1:
            domains.append(i)
        if scores == 0:
            scores = value[s]
        scores.append(score)
    np.save('data/score_1.npy', np.array(scores))
    scores_2 = []
    for i, s in enumerate(node['id']):
        score = 0
        for j, t in enumerate(link['source']):
            if s == t:
                if s == 'Domain':
                    score += scores[node[node['id'] == link.iloc[j, 2]].index.values]
            if s == link.iloc[j, 'target']:
                if s == 'IP':
                    score += scores[node[node['id'] == link.iloc[j, 1]].index.values]
                elif s == 'cert':
                    score += scores[node[node['id'] == link.iloc[j, 1]].index.values]
        scores_2.append(score)
    np.save('data/score_2.npy', np.array(scores_2))

if __name__ == '__main__':
    process_data()