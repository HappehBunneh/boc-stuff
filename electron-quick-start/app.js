const CanvasJS =  require('./canvasjs.min')
var a = 0;
var voltageData = [];
var tempData = [];
var powerData = [];
window.onload = function () {
    var currentData = []; // dataPoints
    var currentChart = new CanvasJS.Chart("currentGraph", {
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
    var voltageChart = new CanvasJS.Chart("voltageGraph", {
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
    var powerChart = new CanvasJS.Chart("powerGraph", {
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
    var tempChart = new CanvasJS.Chart("tempGraph", {
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
    if (clicked_id == 'current') {
        document.getElementById('currentGraph').style.display = 'block';
        document.getElementById('voltageGraph').style.display = 'none';
        document.getElementById('tempGraph').style.display = 'none';
        document.getElementById('powerGraph').style.display = 'none';
    } else if (clicked_id == 'voltage') {
        document.getElementById('currentGraph').style.display = 'none';
        document.getElementById('voltageGraph').style.display = 'block';
        document.getElementById('tempGraph').style.display = 'none';
        document.getElementById('powerGraph').style.display = 'none';
    } else if (clicked_id == 'temp') {
        document.getElementById('currentGraph').style.display = 'none';
        document.getElementById('voltageGraph').style.display = 'none';
        document.getElementById('tempGraph').style.display = 'block';
        document.getElementById('powerGraph').style.display = 'none';
    } else if (clicked_id == 'power') {
        document.getElementById('currentGraph').style.display = 'none';
        document.getElementById('voltageGraph').style.display = 'none';
        document.getElementById('tempGraph').style.display = 'none';
        document.getElementById('powerGraph').style.display = 'block';
    }
}