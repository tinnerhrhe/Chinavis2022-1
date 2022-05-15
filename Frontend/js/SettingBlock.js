function showSettingBlock(layer_id,box_id){
    var setting_layer = document.getElementById(layer_id);
    var setting_box = document.getElementById(box_id);

    setting_layer.style.display = "block";
    setting_box.style.display = "block";
}

function closeSettingBlock(layer_id,box_id){
    for (var i = 1; i < 10; ++i){
        var str = 'inner-select' + i;
        var ele = document.getElementById(str);
        if (ele == null) break;
        else {
            var val = sessionStorage.getItem(str);
            ele.selectedIndex = val;
        }
    }

    var setting_layer = document.getElementById(layer_id);
    var setting_box = document.getElementById(box_id);

    setting_layer.style.display = "none";
    setting_box.style.display = "none";
}

function saveSetting() {
    for (var i = 1; i < 10; ++i){
        var str = 'inner-select' + i;
        var ele = document.getElementById(str);
        if (ele == null) break;
        else {
            var val = ele.selectedIndex;
            sessionStorage.setItem(str, val);
        }
    }
}

function save_quitSetting(layer_id, box_id) {
    for (var i = 1; i < 10; ++i){
        var str = 'inner-select' + i;
        var ele = document.getElementById(str);
        if (ele == null) break;
        else {
            var val = ele.selectedIndex;
            sessionStorage.setItem(str, val);
        }
    }

    var setting_layer = document.getElementById(layer_id);
    var setting_box = document.getElementById(box_id);

    setting_layer.style.display = "none";
    setting_box.style.display = "none";
}

function quitSetting(layer_id, box_id) {
    for (var i = 1; i < 10; ++i){
        var str = 'inner-select' + i;
        var ele = document.getElementById(str);
        if (ele == null) break;
        else {
            var val = sessionStorage.getItem(str);
            ele.selectedIndex = val;
        }
    }

    var setting_layer = document.getElementById(layer_id);
    var setting_box = document.getElementById(box_id);

    setting_layer.style.display = "none";
    setting_box.style.display = "none";
}

function initAll() {
    for (var i = 1; i < 10; ++i){
        var str = 'inner-select' + i;
        var ele = document.getElementById(str);
        if (ele == null) break;
        else {
            var val = ele.selectedIndex;
            sessionStorage.setItem(str, val);
        }
    }

    //sessionStorage中img个数
    sessionStorage.setItem('img-num', 5);
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
    //console.log('curId' + Number(ele1.getAttribute('ImageId')));
    //console.log('add:' + (Number(ele1.getAttribute('ImageId')) + imgNum - 1));
    var nextId = (Number(ele1.getAttribute('ImageId')) + imgNum - 1) % imgNum;
    //console.log(nextId);
    var tmp_path = './images/' + nextId + '.jpg';
    ele1.setAttribute('src', tmp_path);
    ele1.setAttribute('ImageId', '' + nextId);

    ele_cap.innerHTML = '子图' + ele2.getAttribute('ImageId');
}