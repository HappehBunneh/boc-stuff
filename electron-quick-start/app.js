const CanvasJS =  require('./canvasjs.min');
const fs = require('fs');
var bufferData = JSON.parse(fs.readFileSync('../buffer.txt', 'utf8').replace(/'/g , '"'));
var read = require('read-yaml');
var config = read.sync('../config.yaml');
var a = 0;
var currentData = [];
var voltageData = [];
var tempData = [];
var powerData = [];
var currentChart;
var voltageChart;
var powerChart;
var tempChart;
var updateChart;
var xVal = 0;
var yVal = 0; 
var updateInterval = 1000;

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

    readData = function (fileLocation) {
        bufferData = JSON.parse(fs.readFileSync('../buffer.txt', 'utf8').replace(/'/g , '"'));
    }    

    updateChart = function (count) {
        a = a+1
        document.getElementById('output').textContent = JSON.stringify(bufferData, null, 2);
        count = count || 1;
        for (var j = 0; j < count; j++) {
            currentData.push({x: xVal,y: parseFloat(bufferData.STACK_I.replace('A', ""))});
            voltageData.push({x: xVal,y: parseFloat(bufferData.STACK_V.replace('A', ""))});
            powerData.push({x: xVal,y: Math.round(parseFloat(bufferData.STACK_I.replace('A', ""))*parseFloat(bufferData.STACK_V.replace('A', "")))});
            tempData.push({x: xVal,y: parseFloat(bufferData.STACK_TEMP.replace('C', ""))});
            yVal++;
            xVal++;
        }
        currentChart.render();
        voltageChart.render();
        tempChart.render();
        powerChart.render();
    };
    readData(config['buffer']);
    updateChart(currentData.length);
    setInterval(function(){updateChart()}, updateInterval);   
}


function reply_click(clicked_id)
{
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
        updateChart();
    }
}