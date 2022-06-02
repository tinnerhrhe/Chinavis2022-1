from data import *
import json
import os

def fileWhois(filepath):
    with open(filepath, 'r') as f:
        querynodes = json.load(f)['nodes']
    names = {}
    emails = {}
    phones = {}
    def add_stat(dic, query):
        if query == '': return
        if query in dic:
            dic[query] += 1
        else:
            dic[query] = 1
    def top_dict(dic):
        if len(dic) == 0: return ''
        new_dic = {}
        toplist = sorted(dic.items(),key=lambda x:x[1],reverse=True)
        for key in toplist:
            new_dic[key[0]] = dic.get(key[0])
        return new_dic
    for qnode in querynodes:
        qnode = qnode['id']
        if qnode.startswith('Domain_'):
            name, email, phone = queryWhois(qnode)
            add_stat(names, name)
            add_stat(emails, email)
            add_stat(phones, phone)
    names = top_dict(names)
    emails = top_dict(emails)
    phones = top_dict(phones)
    top_name = '' if len(names) == 0 else list(names.items())[0][0]
    top_email = '' if len(emails) == 0 else list(emails.items())[0][0]
    top_phone = '' if len(phones) == 0 else list(phones.items())[0][0]
    info = [top_name, top_email, top_phone]
    print(info)
    return info, { 'name': names, 'email': emails, 'phone': phones }

def isEmptyWhois(info):
    return info[0] == '' and info[1] == '' and info[2] == ''

outputdir = 'output'
if os.path.islink(outputdir):
    outputdir = os.readlink(outputdir)
MAX_GRAPH = 10

all_top_info = []
# Output coregraph infos.
for i in range(0,MAX_GRAPH):
    info, infos = fileWhois(outputdir + '/' + str(i) + '/coregraph.json')
    if isEmptyWhois(info):
        info, infos = fileWhois(outputdir + '/' + str(i) + '/subgraph.json')
        if isEmptyWhois(info):
            print('{} - No whois in coregraph and subgraph, fallback to graph!'.format(i))
            info, infos = fileWhois(outputdir + '/' + str(i) + '/graph.json')

    all_top_info.append(info)
    with open(outputdir + '/' + str(i) + '/whois.json','w',encoding='utf8') as f:
        json.dump(infos,f,ensure_ascii=False)

all_top_info = pd.DataFrame(all_top_info, columns=['name', 'email', 'phone'])
all_top_info.to_csv('info.csv',index=True,encoding='utf8')

# Index the node and edge
node_indexed = node.set_index('id')
link_indexed = link.set_index('id')

# Transfer graph.json to node.csv and link.csv
for i in range(0, MAX_GRAPH):
    with open(outputdir + '/' + str(i) + '/graph.json', 'r') as f:
        graph = json.load(f)
        nodes = pd.json_normalize(graph, record_path='nodes')
        edges = pd.json_normalize(graph, record_path='edges')
        edges['id'] = edges['id'].astype(int)
        node_indexed[node_indexed.index.isin(nodes['id'])].to_csv(outputdir + '/' + str(i) + '/node.csv', encoding='utf8')
        link_indexed[link_indexed.index.isin(edges['id'])].to_csv(outputdir + '/' + str(i) + '/link.csv', encoding='utf8')