## Project for course CS 239

### data

Prepare data `Link.csv` and `Node.csv` in `backend/data/`.

### Get Started

Use Live Share to start the frontend page in `Frontend/index.html`.

### Dump output

Run the script to start mining.

```cmd
cd backend
python main.py
```

This will create output in `Frontend/output/*/` containing:
```
core.json
coregraph.json
graph.json
stat.json
subgraph.json
```

Run the script to get whois info and CSV graph:
```cmd
python export.py
```
which will generate in `Frontend/output/*/`
```
link.csv
node.csv
whois.json
```

### Run Backend Demo

For basic tkinter visualization,
```cmd
python visualize.py
```
To see how to use these API for interacting.