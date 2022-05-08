import numpy as np
import os
import pandas as pd
from utils import *
import time
#feature: 1.number of weighted neighbors(all types) 2. rules for elimination
# 3.(possible) consider jumps and corresponding neighbors
# method: record and iterate scores
domain_weight = {
    'r_cert': 18,            # 很强
    'r_subdomain': 1,
    'r_request_jump': 2,
    'r_dns_a': 10,
    'r_whois_name': 0.1,      # 较强
    'r_whois_email': 0.1,
    'r_whois_phone': 0.1,
    'r_cert_chain': 0,      # 一般
    'r_cname': 0.02,
    'r_asn': 0,             # 较弱
    'r_cidr': 0
}
ip_weight = {
    'r_cert': 0,            # 很强
    'r_subdomain': 0,
    'r_request_jump': 0,
    'r_dns_a': 1,
    'r_whois_name': 0,      # 较强
    'r_whois_email': 0,
    'r_whois_phone': 0,
    'r_cert_chain': 0,      # 一般
    'r_cname': 0,
    'r_asn': 0.01,             # 较弱
    'r_cidr': 0.01
}
cert_weight = {
    'r_cert': 1,            # 很强
    'r_subdomain': 0,
    'r_request_jump': 0,
    'r_dns_a': 0,
    'r_whois_name': 0,      # 较强
    'r_whois_email': 0,
    'r_whois_phone': 0,
    'r_cert_chain': 0.1,      # 一般
    'r_cname': 0,
    'r_asn': 0,             # 较弱
    'r_cidr': 0
}
def process_data():
    node = pd.read_csv('data/Nodefil.csv')
    link = pd.read_csv('data/Linkfil.csv')
    # select data without nan
    node = node.dropna()
    node = node.drop_duplicates('id', keep='first')
    link = link.dropna()
    link = link.drop_duplicates()
    #id = np.array(node.index.values)
    #type = np.array(type_value[node['type'][i]] for i in range(node.shape[0]))
    industry = np.array(0 if node['industry'][i] == '[]' else 1 for i in range(node.shape[0]))
    scores = []
    scores_dict={}
    domains = []
    new_node = node[(node['industry'] != '[]') |
                    (node['type'] != 'Domain')]
    t = time.time()
    for i, node_row in new_node.iterrows():
        score = 0
        ips = 0
        for j, link_row in link[(link['source'] == node_row['id']) | (link['target'] == node_row['id'])].iterrows():
            type = link_row['relation']
            if node_row['type'] == 'Domain':
                if type == 'r_dns_a':
                    ips += 1
                score += domain_weight[type]
            elif node_row['type'] == 'IP':
                score += ip_weight[type]
            elif node_row['type'] == 'Cert':
                score += cert_weight[type]
        if ips > 1:
            domains.append(i)
        if scores == 0:
            scores = value[node_row['type']]
        scores.append(score)
        scores_dict[node_row['id']] = score
        #print(scores)
        if i % 5e4 == 0:
            print(time.time()-t)
    np.save('data/score_1_fil.npy', np.array(scores))
    scores_2 = []
    t = time.time()
    for i, node_row in new_node.iterrows():
        score = 0
        if node_row['type'] == 'IP' or node_row['type'] == 'Cert':
            for j, link_row in link[link['target'] == node_row['id']].iterrows():
                score += scores_dict[link_row['source']] if link_row['source'] in scores_dict else 0
        elif node_row['type'] == 'Domain':
            for j, link_row in link[link['source'] == node_row['id']].iterrows():
                score += scores_dict[link_row['target']] if link_row['target'] in scores_dict else 0
        scores_2.append(score)
        if i % 5e4 == 0:
            print(time.time()-t)
    np.save('data/score_2_fil.npy', np.array(scores_2))
if __name__ == '__main__':
    process_data()
