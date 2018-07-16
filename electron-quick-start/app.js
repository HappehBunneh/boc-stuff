const CanvasJS =  require('./canvasjs.min')
var a = 0;
var currentData = [];
var voltageData = [];
var tempData = [];
var powerData = [];
var currentChart;
var voltageChart;
var powerChart;
var tempChart;
window.onload = function () {
    currentChart = new CanvasJS.Chart("currentGraph", {
        title :{
            text: "Current"
        },
        axisY: {
            includeZero: false
        },      
        data: [{
            type: "line",
            dataPoints: currentData
        }]
    });
    voltageChart = new CanvasJS.Chart("voltageGraph", {
        title :{
            text: "Voltage"
        },
        axisY: {
            includeZero: false
        },      
        data: [{
            type: "line",
            dataPoints: voltageData
        }]
    });
    powerChart = new CanvasJS.Chart("powerGraph", {
        title :{
            text: "Power"
        },
        axisY: {
            includeZero: false
        },      
        data: [{
            type: "line",
            dataPoints: powerData
        }]
    });
    tempChart = new CanvasJS.Chart("tempGraph", {
        title :{
            text: "Temp"
        },
        axisY: {
            includeZero: false
        },      
        data: [{
            type: "line",
            dataPoints: tempData
        }]
    });
    var xVal = 0;
    var yVal = 0; 
    var updateInterval = 1000;
    var updateChart = function (count) {
        a = a+1
        document.getElementById('output').textContent = a;
        count = count || 1;
        for (var j = 0; j < count; j++) {
            currentData.push({x: xVal,y: yVal});
            voltageData.push({x: xVal,y: yVal*2});
            powerData.push({x: xVal,y: yVal*yVal});
            tempData.push({x: xVal,y: yVal*-1});
            yVal++;
            xVal++;
        }
        currentChart.render();
        voltageChart.render();
        tempChart.render();
        powerChart.render();
    };
    updateChart(currentData.length);
    setInterval(function(){updateChart()}, updateInterval);   
}
function reply_click(clicked_id)
{
    console.log(powerChart);
    if (clicked_id == 'current') {
        document.getElementById('currentGraph').style.display = 'block';
        currentChart.render();
        document.getElementById('voltageGraph').style.display = 'none';
        document.getElementById('tempGraph').style.display = 'none';
        document.getElementById('powerGraph').style.display = 'none';
    } else if (clicked_id == 'voltage') {
        document.getElementById('currentGraph').style.display = 'none';
        document.getElementById('voltageGraph').style.display = 'block';
        voltageChart.render();
        document.getElementById('tempGraph').style.display = 'none';
        document.getElementById('powerGraph').style.display = 'none';
    } else if (clicked_id == 'temp') {
        document.getElementById('currentGraph').style.display = 'none';
        document.getElementById('voltageGraph').style.display = 'none';
        document.getElementById('tempGraph').style.display = 'block';
        tempChart.render();
        document.getElementById('powerGraph').style.display = 'none';
    } else if (clicked_id == 'power') {
        document.getElementById('currentGraph').style.display = 'none';
        document.getElementById('voltageGraph').style.display = 'none';
        document.getElementById('tempGraph').style.display = 'none';
        document.getElementById('powerGraph').style.display = 'block';
        powerChart.render();
    } else if (clicked_id == 'clear') {
        currentData = [];
        voltageData = [];
        tempData = [];
        powerData = [];
        console.log(currentData);
    }
}