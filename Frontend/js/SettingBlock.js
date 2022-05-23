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