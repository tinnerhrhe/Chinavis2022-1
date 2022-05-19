import numpy as np
import os
import pandas as pd
def core_ass():
    score_1 = np.load('data/score_1.npy')
    score_2 = np.load('data/score_2.npy')
    node = pd.read_csv('data/Node.csv')
    link = pd.read_csv('data/Link.csv')
    # select data without nan
    node = node.dropna()
    node = node.drop_duplicates('id', keep='first')
    link = link.dropna()
    link = link.drop_duplicates()
    node = node[(node['industry'] != '[]') |
                    (node['type'] != 'Domain')]
    node = node.reset_index() #index和npy对应
    #不同类型点在score中的index
    domain_index = node[node['type'] == 'Domain'].index.values
    domain_id = node[node['type'] == 'Domain'].id.values
    ip_index = node[node['type'] =='IP'].index.values
    ip_id = node[node['type'] == 'IP'].id.values
    cert_index = node[node['type'] == 'Cert'].index.values
    cert_id = node[node['type'] == 'Cert'].id.values
    '''
    domain_score_1 = score_1[domain_index]
    ip_score_1 = score_1[ip_index]
    cert_score_1 = score_1[cert_index]
    top_domain_1 = domain_score_1.argsort()[::-1][0:20]
    top_ip_1 = ip_score_1.argsort()[::-1][0:20]
    top_cert_1 = cert_score_1.argsort()[::-1][0:20]
    for i in top_domain_1:
        print(domain_id[i], '--->>>', domain_score_1[i])
    print("===============")
    for i in top_ip_1:
        print(ip_id[i], '--->>>', ip_score_1[i])
    print("===============")
    for i in top_cert_1:
        print(cert_id[i], '--->>>', cert_score_1[i])
    '''
    domain_score_2 = score_2[domain_index]
    ip_score_2 = score_2[ip_index]
    cert_score_2 = score_2[cert_index]
    top_domain_2 = domain_score_2.argsort()[::-1][0:20]
    top_ip_2 = ip_score_2.argsort()[::-1][0:20]
    top_cert_2 = cert_score_2.argsort()[::-1][0:20]
    for i in top_domain_2:
        print(domain_id[i], '--->>>', domain_score_2[i])
    print("===============")
    for i in top_ip_2:
        print(ip_id[i], '--->>>', ip_score_2[i])
    print("===============")
    for i in top_cert_2:
        print(cert_id[i], '--->>>', cert_score_2[i])
if __name__ == '__main__':
    core_ass()