from data import *
import json

outputdir = 'output'

# Output coregraph infos.
infos = []
for i in range(0,10):
    with open(outputdir + '/' + str(i) + '/coregraph.json') as f:
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
        return sorted(dic.items(),key=lambda x:x[1],reverse=True)[0]
    for qnode in querynodes:
        qnode = qnode['id']
        if qnode.startswith('Domain_'):
            name, email, phone = queryWhois(qnode)
            add_stat(names, name)
            add_stat(emails, email)
            add_stat(phones, phone)
    infos.append([top_dict(names), top_dict(emails), top_dict(phones)])

# still some graphs (4) missing data.
with open('info.txt','w',encoding='utf8') as f:
    f.write(str(infos))