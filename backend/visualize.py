from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from meta import *
from ucs import *
import copy

root = Tk()

labelId = Label(root, text='Node ID:').grid(sticky=E)
labelLimit = Label(root, text='Limitation:').grid(sticky=E)

selId = StringVar()
comboId = ttk.Combobox(root, textvariable=selId)
comboId['values'] = [e[0] for e in evidence]
comboId.grid(row=0, column=1)

selLimit = StringVar()
comboLimit = ttk.Combobox(root, textvariable=selLimit, state='readonly')
comboLimit['values'] = [n for n in net_limit.keys()]
comboLimit.grid(row=1, column=1)

labelNode = Label(root, text='Node', anchor=W, width=20)
labelNode.grid(sticky=E, row=0, column=2)
progressNode = ttk.Progressbar(root)
progressNode.grid(row=0, column=3)

labelEdge = Label(root, text='Edge', anchor=W, width=20)
labelEdge.grid(sticky=E, row=1, column=2)
progressEdge = ttk.Progressbar(root)
progressEdge.grid(row=1, column=3)

WIDTH = 700
HEIGHT = 700
PADDING = 30
c = Canvas(root, width=WIDTH, height=HEIGHT)
c.grid(row=2, column=0, columnspan=5)

def generate(*args):
    c.delete(ALL)
    node_id = comboId.get()
    limitation = comboLimit.get()
    if node_id == "" or limitation == "":
        messagebox.showerror('Generate Error', 'Empty Node ID or Limitation!')
        return
    node_limit = net_limit[limitation]['node']
    progressNode['maximum'] = node_limit
    progressEdge['maximum'] = net_limit[limitation]['edge']

    nodes = {}
    cton = {}
    edges = {}
    node_side_num = int(math.sqrt(node_limit)) + 1
    BANDWIDTH = int((WIDTH - PADDING * 2) / (node_side_num - 1))
    BANDHEIGHT = int((HEIGHT - PADDING * 2) / (node_side_num - 1))
    R = 5

    def position(coord):
        return [
            PADDING + coord[0] * BANDWIDTH,
            PADDING + coord[1] * BANDHEIGHT
        ]
    
    def minepaths(event):
        cid = c.find_closest(event.x, event.y)[0]
        coreid = cton[cid]

        subgraph = copy.deepcopy(search.subgraph)
        corenodes = copy.deepcopy(search.corenodes)
        pathucs = pathUCS(Graph(subgraph.getNodes(),subgraph.getEdges()))
        pathucs.path_run(coreid, corenodes)

        def showpath(event):
            c.delete('cpath')
            cid = c.find_closest(event.x, event.y)[0]
            coreid = cton[cid]
            tEdges = pathucs.targetPaths[coreid]
            labelNode['text'] = coreid
            labelEdge['text'] = str(tEdges)
            for eid in tEdges:
                e = edges[eid]
                sourcepos = position(nodes[e[0]])
                targetpos = position(nodes[e[1]])
                c.create_line(sourcepos[0], sourcepos[1], targetpos[0], targetpos[1], fill='purple', width=3, tags='cpath')

        def rmcritical(event):
            c.delete('cpath')
            c.delete('critical')
            labelNode['text'] = 'Node'
            labelEdge['text'] = 'Edge'

        for eid in pathucs.visitedEdges:
            e = edges[eid]
            sourcepos = position(nodes[e[0]])
            targetpos = position(nodes[e[1]])
            c.create_line(sourcepos[0], sourcepos[1], targetpos[0], targetpos[1], fill='red', width=2, tags='critical')

        pos = position(nodes[coreid])
        coreobj = c.create_oval(pos[0] - R, pos[1] - R, pos[0] + R, pos[1] + R, fill='yellow',tags='critical')
        labelNode['text'] = coreid
        c.tag_bind(coreobj, '<Button-1>', func=rmcritical)
        
        for corenode in pathucs.targetPaths.keys():
            pos = position(nodes[corenode])
            coreobj = c.create_oval(pos[0] - R, pos[1] - R, pos[0] + R, pos[1] + R, fill='red',tags='critical')
            c.tag_bind(coreobj, '<Button-1>', func=showpath)
            cton[coreobj] = corenode


    def vis_node_search(node: Node):
        curid = node.node_id
        progressNode['value'] = search.node_limit
        labelNode['text'] = curid
        cnt = node_limit - search.node_limit - 1 # start from 0
        loc = [math.floor(cnt / node_side_num), cnt % node_side_num]
        nodes[str(curid)] = loc
        pos = position(loc)
        if node.iscore:
            cid = c.create_oval(pos[0] - R, pos[1] - R, pos[0] + R, pos[1] + R, fill='blue')
        else:
            cid = c.create_oval(pos[0] - R, pos[1] - R, pos[0] + R, pos[1] + R)
        root.update()
    def vis_edge_search(e, curnode):
        progressEdge['value'] = search.edge_limit
        labelEdge['text'] = e['id']
        edges[str(e['id'])] = [e['source'], e['target']]
        sourcepos = position(nodes[e['source']])
        targetpos = position(nodes[e['target']])
        c.create_line(sourcepos[0], sourcepos[1], targetpos[0], targetpos[1])
        root.update()
    search = searchUCS(Graph(node, link), limitation, vis_node=vis_node_search, vis_edge=vis_edge_search)
    search.search_run(node_id)
    labelNode['text'] = 'Node'
    labelEdge['text'] = 'Edge'
    cton = {}
    for corenode in search.corenodes:
        pos = position(nodes[corenode])
        coreobj = c.create_oval(pos[0] - R, pos[1] - R, pos[0] + R, pos[1] + R, fill='blue',tags=(corenode))
        c.tag_bind(coreobj, '<Button-1>', func=minepaths)
        cton[coreobj] = corenode

buttonGen = Button(root, text='Generate')
buttonGen.bind('<Button-1>', generate)
buttonGen.grid(row=1, column=4)

root.mainloop()