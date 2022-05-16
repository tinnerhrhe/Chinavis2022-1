from flask import Flask, render_template
import copy
import json
from ucs import *
from meta import *

app = Flask(__name__, template_folder='../templates/', static_folder='../Frontend/')

@app.route('/')
def root():
    return render_template('index.html')

subgraph = None

@app.route('/mining/<source>')
def mining(source):
    limitation = 'small'
    for e in evidence:
        if e[0] == source:
            limitation = e[1]
            break
    search = searchUCS(Graph(node, link), net_limit[limitation])
    search.run(source)
    subgraph = copy.deepcopy(search.subgraph)
    outputgraph = {
        "nodes": toRecords(subgraph.nodes),
        "edges": toRecords(subgraph.edges),
    }
    return json.dumps(outputgraph)

if __name__ == '__main__':
    app.run()