var currentData = [];
var voltageData = [];
var tempData = [];
var powerData = [];
var data = ['currentData', 'voltageData', 'tempData', 'powerData'];
var graphs = document.getElementsByClassName('graph');
var xhr = new XMLHttpRequest();
var datalols = [];


window.onload = function() {
    console.log('boom');
    mainChart = new CanvasJS.Chart("mainGraph", { 
        title: {
            text: "One Graph to rule them all"
        },
        axisY: {
            includeZero: false
        },
        legend:{
            cursor: "pointer",
            fontSize: 16,
            itemclick: toggleDataSeries
        },
        toolTip:{
            shared: true
        },
        zoomEnabled: true,
        data: [
            {
                showInLegend: true,
                name: "Current",
                type: "line",
                dataPoints: currentData
            },
            {
                showInLegend: true,
                name: "Voltage",
                type: "line",
                dataPoints: voltageData
            },
            {
                showInLegend: true,
                name: "Temperature",
                type: "line",
                dataPoints: tempData
            },
            {
                showInLegend: true,
                name: "Power",
                type: "line",
                dataPoints: powerData
            }
        ]
    });
    var g = new Dygraph(document.getElementById("div_g"), datalols, {
        drawPoints: true,
        showRoller: true,
        labels: ['Time', 'Random']
    });
    setInterval(function(){updateData()}, 1000);
}

function toggleDataSeries(e){
	if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;
	}
	else{
		e.dataSeries.visible = true;
	}
	mainChart.render();
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
    mainChart.render();
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