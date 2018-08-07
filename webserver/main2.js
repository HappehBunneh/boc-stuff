var currentData = [];
var voltageData = [];
var tempData = [];
var powerData = [];
var data = ['currentData', 'voltageData', 'tempData', 'powerData'];
var graphs = document.getElementsByClassName('graph');
var xhr = new XMLHttpRequest();

window.onload = function() {
    console.log('boom');
    currentChart = new CanvasJS.Chart("currentGraph", {title :{text: "Current"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: currentData}]});
    voltageChart = new CanvasJS.Chart("voltageGraph", {title :{text: "Voltage"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: voltageData}]});
    tempChart = new CanvasJS.Chart("tempGraph", {title :{text: "Temperature"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: tempData}]});
    powerChart = new CanvasJS.Chart("powerGraph", {title :{text: "Power"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: powerData}]});
    for (var i = 1; i < graphs.length; i++){
        graphs[i].style.visibility = 'hidden';
    }
    setInterval(function(){updateData()}, 1000);
}

xhr.onload = function () {
    data = eval(xhr.responseText);
    for (var i = 0; i < data.length; i++) {
        currentData[i] = {x: i, y: parseFloat(data[i][0])};
        voltageData[i] = {x: i, y: parseFloat(data[i][1])};
        tempData[i] = {x: i, y: parseFloat(data[i][2])};
        powerData[i] = {x: i, y: parseFloat(data[i][3])};
    }
}

function updateData() {
    xhr.open('GET', 'updateData.php'); 
    xhr.send(null);
    currentChart.render();
    voltageChart.render();
    tempChart.render();
    powerChart.render();
}

function graph_click(element){
    for (var i = 0; i < graphs.length; i++){
        if (graphs[i].id != element + 'Graph') {
            graphs[i].style.visibility = 'hidden';
        } else {
            graphs[i].style.visibility = 'visible';
        }
    }
}

function button_click(element){
    if (element == 'start') {
        console.log('starting hook up to python script python start.py');
    } else if (element  == 'stop') {
        console.log('stopping, hook up to python script python stop.py');
    } else if (element == 'clear') {
        console.log('send sql');
    }
}

/*
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) { // if request done
            if (xhr.status === 200) { // if successful return
                data = eval(xhr.responseText);
                console.log(data); 
            };
        };
    };
*/

/*
    currentData = [];
    voltageData = [];
    tempData = [];
    powerData = [];
    xhr.open('GET', 'updateData.php'); 
    xhr.onload = function () {
        data = eval(xhr.responseText);
    }
    xhr.send(null);
    for(var i = 0; i < data.length; i++) {
        console.log(data[i]);
        currentData.push({x: i, y: parseFloat(data[i][0])});
        voltageData.push({x: i, y: parseFloat(data[i][1])});
        tempData.push({x: i, y: parseFloat(data[i][2])});
        powerData.push({x: i, y: parseFloat(data[i][3])});
    };
    currentChart.render();
    voltageChart.render();
    tempChart.render();
    powerChart.render();
*/