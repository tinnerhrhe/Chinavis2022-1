/*
graph.json?graphid={graphId}
core.json?graphid={graphId}
path.json?graphid={graphId}
*/
function getJsonAndPlot(graphId) {
    var reqStr = "graph.json?graphid=" + graphId;
    var xmlHttp = null;
    if (window.ActiveXObject) {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    else if (window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
    }
    else {
        alert("Unsupported Website Broswer!");
    }

    if (xmlHttp != null) {
        xmlHttp.open("GET", reqStr, true);
        xmlHttp.send();
        xmlHttp.onreadystatechange = getText;
    }

    function getText() {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                data = JSON.parse(xmlHttp.responseText);
                plotGraph(data);
            }
        }
    }
    getText();
}

function plotGraph(remoteData) {
    var main = function (remoteData) {
        var graph = new G6.Graph({
            container: 'div-id',
            width: 2000,
            height: 1300,
        });

        for (var i = 0; i < remoteData['nodes'].length; ++i){
            remoteData['nodes']['size'] = 100;
        }

        remoteData['layout'] = {
            type: 'force',
            preventOverlap: true,
            linkDistance: 100
        };
    
        graph.data(remoteData); // 加载远程数据
        graph.render(); // 渲染
    };
    main(remoteData);
}