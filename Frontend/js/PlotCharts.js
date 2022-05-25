function plotBarsPieGraph(barsId, pieId1, pieId2, graphId){
    var reqStr = "/stat/"+graphId;
    // var reqStr = "./output/stat.json";
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
                var nodesNum = 0;
                var edgesNum = 0;
                for (var key in data['nodes']) nodesNum += data['nodes'][key];
                for (var key in data['edges']) edgesNum += data['edges'][key];
                ///
    console.log(graphId);
                realPlotBars(graphId, barsId, nodesNum, edgesNum);
                realPlotPie(graphId, pieId1, data['nodes'], 'node');
                realPlotPie(graphId, pieId2, data['edges'], 'edge');
            }
        }
    }
}

function realPlotBars(graphId, divId, nodesNum, edgesNum) {
    var dom = document.getElementById(divId);
    var myChart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });
    //var app = {};
    
    var option;

    ///
    console.log("Really enter...");

    option = {
        title: {
            text: 'SubGraph' + graphId
        },
        xAxis: {
            type: 'category',
            data: ['Node', 'Edge']
        },
        yAxis: {
            type: 'value'
        },
        legend: {
            data: ['Node', 'Edge']
        },
        series: [
            {
                name: 'Node',
                type: 'bar',
                label: {
                    show: true,
                },
                data: [nodesNum, '-']
            },
            {
                name: 'Edge',
                type: 'bar',
                label: {
                    show: true,
                },
                data: ['-', edgesNum]
            }
        ]
    };

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }
}

function realPlotPie(graphId, divId, jsonData, gtype) {
    var chartDom = document.getElementById(divId);
    var myChart = echarts.init(chartDom);
    var option;

    var data = [];
    for (var key in jsonData) {
        if (key.substring(0, 2) == 'r_') {
            var tmpKey = key.substring(2, key.length);
            data.push({
                value: jsonData[key],
                name: tmpKey
            });
        }
        else {
            data.push({
                value: jsonData[key],
                name: key
            });
        }
        
    }

    if (gtype == 'node' || gtype == 'Node' || gtype == 'NODE') gtype = 'Node';
    else if (gtype == 'edge' || gtype == 'Edge' || gtype == 'EDGE') gtype = 'Edge';

    option = {
        title: {
            text: gtype + ' Type',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Access From',
                type: 'pie',
                radius: '50%',
                label: {
                    show: false
                },
                labelLine: {
                    show: false
                },
                data: data,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }
}

function prevSelect() {
    //从sessionStorage中读取img个数
    var imgNum = Number(sessionStorage.getItem('img-num'));
    ele1 = document.getElementById('img0-id');
    ele2 = document.getElementById('img1-id');
    ele3 = document.getElementById('img2-id');

    var ele_cap = document.getElementById('select-scan-id');

    ele1.setAttribute('src', ele2.getAttribute('src'));
    ele1.setAttribute('ImageId', ele2.getAttribute('ImageId'));
    ele2.setAttribute('src', ele3.getAttribute('src'));
    ele2.setAttribute('ImageId', ele3.getAttribute('ImageId'));
    var nextId = (Number(ele3.getAttribute('ImageId')) + 1) % imgNum;
    var tmp_path = './images/' + nextId + '.jpg';
    ele3.setAttribute('src', tmp_path);
    ele3.setAttribute('ImageId', '' + nextId);

    ///
    console.log("Begin to plot..." + nextId);
    plotBarsPieGraph('right-bar-id','right-pie-id1','right-pie-id2',nextId);

    ele_cap.innerHTML = '子图' + ele2.getAttribute('ImageId');
}

function nextSelect() {
    //从sessionStorage中读取img个数
    var imgNum = Number(sessionStorage.getItem('img-num'));
    ele1 = document.getElementById('img0-id');
    ele2 = document.getElementById('img1-id');
    ele3 = document.getElementById('img2-id');

    var ele_cap = document.getElementById('select-scan-id');
    
    ele3.setAttribute('src', ele2.getAttribute('src'));
    ele3.setAttribute('ImageId', ele2.getAttribute('ImageId'));
    ele2.setAttribute('src', ele1.getAttribute('src'));
    ele2.setAttribute('ImageId', ele1.getAttribute('ImageId'));
    var nextId = (Number(ele1.getAttribute('ImageId')) + imgNum - 1) % imgNum;
    var tmp_path = './images/' + nextId + '.jpg';
    ele1.setAttribute('src', tmp_path);
    ele1.setAttribute('ImageId', '' + nextId);

    ///
    console.log("Begin to plot..." + nextId);
    plotBarsPieGraph('right-bar-id','right-pie-id1','right-pie-id2',nextId);

    ele_cap.innerHTML = '子图' + ele2.getAttribute('ImageId');
}