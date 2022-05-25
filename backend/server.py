from flask import Flask, render_template
import copy
import json
from ucs import *
from meta import *

app = Flask(__name__, template_folder='../templates/', static_folder='../Frontend/')

@app.route('/')
def root():
    return render_template('index.html')

search = None
corenodes = None
curid = None

@app.route('/mining/<gid>')
def mining(gid):
    global search, curid
    gid = int(gid)
    curid = gid
    source = evidence[gid][0]
    limitation = evidence[gid][1]
    search = searchUCS(Graph(node, link), net_limit[limitation])
    search.search_run(source)
    subgraph = copy.deepcopy(search.subgraph)
    outputgraph = {
        "nodes": toRecords(subgraph.nodes),
        "edges": toRecords(subgraph.edges),
    }
    return json.dumps(outputgraph)

@app.route('/corenodes')
def corenodes():
    global corenodes
    if search is not None:
        corenodes = copy.deepcopy(search.corenodes)
        return json.dumps(corenodes)
    return json.dumps({})

@app.route('/stats/<gid>')
def stats(gid):
    global search, curid
    gid = int(gid)
    if curid == gid and search is not None:
        return json.dumps(search.statdata)
    return json.dumps({})

@app.route('/route/<source>')
def route(source):
    if search is not None and corenodes is not None:
        subgraph = copy.deepcopy(search.subgraph)
        pathtracing = pathUCS(Graph(subgraph.getNodes(), subgraph.getEdges()))
        pathtracing.run(source, corenodes)
        paths = {}
        paths['targetPaths'] = pathtracing.targetPaths
        paths['visitedPaths'] = pathtracing.visitedEdges
        return json.dumps(paths)
    return json.dumps({'targetPaths':{},'visitedPaths':[]})


if __name__ == '__main__':
    app.run()