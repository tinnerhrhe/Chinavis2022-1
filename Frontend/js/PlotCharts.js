function plotBarsPieGraph(barsId, pieId1, pieId2, graphId){
    //var reqStr = "stat.json?graphid="+graphId;
    var reqStr = "./output/" + graphId + "/stat.json";
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
                //console.log(graphId);
                var divId01 = "bar-pie-id";
                var divId02 = "wordcloud-container-id";
                var ele1 = document.getElementById(divId01);
                var ele2 = document.getElementById(divId02);
                var flag1 = 0;
                if (ele1.style.display == 'none') {
                    flag1 = 1;
                    ele1.style.display = 'inherit';
                }
                realPlotBars(graphId, barsId, nodesNum, edgesNum);
                realPlotPie(graphId, pieId1, data['nodes'], 'node');
                realPlotPie(graphId, pieId2, data['edges'], 'edge');
                if (flag1 == 1) ele1.style.display = 'none';

                flag1 = 0;
                if (ele2.style.display == 'none') {
                    flag1 = 1;
                    ele2.style.display = 'inherit';
                }
                realPlotWordCloud("word-cloud-id", data['industries']);
                if (flag1 == 1) ele2.style.display = 'none';
            }
        }
    }
}

function realPlotBars(graphId, divId, nodesNum, edgesNum) {
    var dom = document.getElementById(divId);
    var myChart = echarts.init(dom, 'dark', {
        renderer: 'canvas',
        useDirtyRect: false
    });
    //var app = {};
    
    var option;

    ///
    console.log("Really enter...");

    option = {
        backgroundColor: 'transparent',
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
    var myChart = echarts.init(chartDom, 'dark');
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
        backgroundColor: 'transparent',
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
        grid:{
            top: '0%',
            bottom: '0%'
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
var graphId = 0;

function mainplot() {
    
    var ele_cap = document.getElementById('select-scan-id');
    ///
    console.log("Begin to plot..." + graphId);
    ele_cap.innerHTML = '子图' + graphId;
    plotBarsPieGraph('right-bar-id','right-pie-id1','right-pie-id2',graphId);
    getJsonAndPlot(graphId);
}

function prevSelect() {
    //从sessionStorage中读取img个数
    var imgNum = Number(sessionStorage.getItem('img-num'));
    var isp2 = document.getElementById('select1-id').value == 2;
    graphId = (graphId + 1) % imgNum + (isp2 ? 5 : 0);
    ele1 = document.getElementById('img0-id');
    ele2 = document.getElementById('img1-id');
    ele3 = document.getElementById('img2-id');
    ele4 = document.getElementById('img3-id');
    ele5 = document.getElementById('img4-id');

    ele1.setAttribute('src', ele2.getAttribute('src'));
    ele1.setAttribute('ImageId', ele2.getAttribute('ImageId'));
    ele2.setAttribute('src', ele3.getAttribute('src'));
    ele2.setAttribute('ImageId', ele3.getAttribute('ImageId'));
    ele3.setAttribute('src', ele4.getAttribute('src'));
    ele3.setAttribute('ImageId', ele4.getAttribute('ImageId'));
    ele4.setAttribute('src', ele5.getAttribute('src'));
    ele4.setAttribute('ImageId', ele5.getAttribute('ImageId'));
    ele5.setAttribute('src', ele1.getAttribute('src'));
    ele5.setAttribute('ImageId', ele1.getAttribute('ImageId'));
    //var nextId = (Number(ele2.getAttribute('ImageId')) + 1) % imgNum;
    var tmp_path = './images/' + graphId + '.png';
    //ele5.setAttribute('src', tmp_path);
    //ele5.setAttribute('ImageId', '' + nextId);

    mainplot();
}

function nextSelect() {
    //从sessionStorage中读取img个数
    var imgNum = Number(sessionStorage.getItem('img-num'));
    var isp2 = document.getElementById('select1-id').value == 2;
    graphId = (graphId +imgNum- 1) % imgNum + (isp2 ? 5 : 0);
    ele1 = document.getElementById('img0-id');
    ele2 = document.getElementById('img1-id');
    ele3 = document.getElementById('img2-id');
    ele4 = document.getElementById('img3-id');
    ele5 = document.getElementById('img4-id');

    ele5.setAttribute('src', ele4.getAttribute('src'));
    ele5.setAttribute('ImageId', ele4.getAttribute('ImageId'));
    ele4.setAttribute('src', ele3.getAttribute('src'));
    ele4.setAttribute('ImageId', ele3.getAttribute('ImageId'));
    ele3.setAttribute('src', ele2.getAttribute('src'));
    ele3.setAttribute('ImageId', ele2.getAttribute('ImageId'));
    ele2.setAttribute('src', ele1.getAttribute('src'));
    ele2.setAttribute('ImageId', ele1.getAttribute('ImageId'));
    ele1.setAttribute('src', ele5.getAttribute('src'));
    ele1.setAttribute('ImageId', ele5.getAttribute('ImageId'));
   // var nextId = (Number(ele1.getAttribute('ImageId')) + imgNum - 1) % imgNum;
    //ele1.setAttribute('src', tmp_path);
    //ele1.setAttribute('ImageId', '' + nextId);
    var tmp_path = './images/' + graphId + '.png';
    //ele5.setAttribute('src', tmp_path);
    //ele5.setAttribute('ImageId', '' + nextId);

    mainplot()
}

function changeProblem(){
    if (document.getElementById("select1-id").value == 1) {
        for (var i = 0; i <= 4; ++i) {
            var imgdom = document.getElementById('img' + i + '-id');
            imgdom.setAttribute('src', './images/' + i + '.png');
            imgdom.setAttribute('ImageId', i);
        }
    } else {
        for (var i = 0; i <= 4; ++i) {
            var imgdom = document.getElementById('img' + i + '-id');
            imgdom.setAttribute('src', './images/' + (i + 5) + '.png');
            imgdom.setAttribute('ImageId', (i + 5));
        }
    }
    if (graphId <= 4) graphId = 5;
    else graphId = 0;
    mainplot();
}

function realPlotWordCloud(divId, data) {
    // div-id
    var div_id = divId;
    var typeMap = {
        "A": "涉黄",
        "B": "涉赌",
        "C": "诈骗",
        "D": "涉毒",
        "E": "涉枪",
        "F": "黑客",
        "G": "非法交易平台",
        "H": "非法支付平台",
        "I": "其他"
    };
    var new_data = [];
    for (var key in data) {
        if (key == "") continue;
        var name = typeMap[key];
        var value = data[key] > 40 ? 40 : data[key];
        value = value * 7.6;
        new_data.push([
            name,
            value
        ]);
    }

    console.log(new_data);
    console.log(div_id);

    var options = [];
    options.list = new_data;

    var ele = document.getElementById(div_id);
    WordCloud(ele, options);
}

function selectDisplay(divId1, divId2, op) {
    if (op == 1) {
        document.getElementById(divId1).style.display = 'inherit';
        document.getElementById(divId2).style.display = 'none';
    }
    else if (op == 2) {
        document.getElementById(divId2).style.display = 'inherit';
        document.getElementById(divId1).style.display = 'none';
    }
}
