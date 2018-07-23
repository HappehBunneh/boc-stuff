var currentData = [];
var voltageData = [];
var tempData = [];
var powerData = [];
var a = 0;
var xVal = 0;
var graphs = document.getElementsByClassName('graph');

window.onload = function() {
    currentChart = new CanvasJS.Chart("currentGraph", {title :{text: "Current"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: currentData}]});
    voltageChart = new CanvasJS.Chart("voltageGraph", {title :{text: "Voltage"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: voltageData}]});
    tempChart = new CanvasJS.Chart("tempGraph", {title :{text: "Temperature"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: tempData}]});
    powerChart = new CanvasJS.Chart("powerGraph", {title :{text: "Power"}, axisY: {includeZero: false}, data: [{type: "line",dataPoints: powerData}]});
    for (var i = 1; i < graphs.length; i++){
        graphs[i].style.visibility = 'hidden';
    }
    setInterval(function(){updateData()}, 1000);
    setInterval(function(){updateChart()}, 1000);
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
        console.log('starting');
    } else if (element  == 'stop') {
        console.log('stopping');
    } else if (element == 'clear') {
        voltageData = [];
        currentData = [];
        tempData = [];
        powerData = [];
    }
}

function updateData(){
    a++;
}

function updateChart(count) {
    count = count || 1;
    for (var j = 0; j < count; j++) {
        currentData.push({x: xVal,y: a});
        voltageData.push({x: xVal,y: a});
        powerData.push({x: xVal,y: a});
        tempData.push({x: xVal,y: a});
        xVal++;
    }
    currentChart.render();
    voltageChart.render();
    tempChart.render();
    powerChart.render();
};