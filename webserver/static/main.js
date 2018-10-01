var currentData = [];
var voltageData = [];
var tempData = [];
var powerData = [];
var data = ['currentData', 'voltageData', 'tempData', 'powerData'];
var graphs = document.getElementsByClassName('graph');
var datalols = [];
var database = 'lol';
var check = [false,false,false];

window.onload = function() {
    disableButton();
    $('.filename').on('input', ':text', function(){ doSomething(); });
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
                xValueType: "dateTime",
                dataPoints: currentData,
            },
            {
                showInLegend: true,
                name: "Voltage",
                type: "line",
                xValueType: "dateTime",
                dataPoints: voltageData,
            },
            {
                showInLegend: true,
                name: "Temperature",
                type: "line",
                xValueType: "dateTime",
                dataPoints: tempData,
            },
            {
                showInLegend: true,
                name: "Power",
                type: "line",
                xValueType: "dateTime",
                dataPoints: powerData,
            }
        ]
    });
    mainChart.render();
    getDatabases();
    setInterval(function(){fetchData()}, 5000);
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

function updateData(data) {
    var values = data['results'][0]['series'][0]['values'];
    var columns = data['results'][0]['series'][0]['columns'];
    console.log(currentData);
    for(var i = 0; i < columns.length; i++){
        if (columns[i] == 'current') {
            var currentIndex = i;
        } else if (columns[i] == 'voltage') {
            var voltageIndex = i;
        } else if (columns[i] == 'power') {
            var powerIndex = i;
        } else if (columns[i] == 'temperature') {
            var tempIndex = i;
        } else if (columns[i] == 'time') {
            var timeIndex = i;
        }
    }
    if (currentData.length == values.length) {
        if ((currentData[currentData.length-1]['x'] == values[values.length-1][timeIndex]) && (currentData[0]['x'] == values[0][timeIndex])) {
            console.log('skip');
        } else {
            for (var j = 0; j < values.length; j++) {
                currentData[j] = {x: values[j][timeIndex], y:values[j][currentIndex]}
                voltageData[j]= {x: values[j][timeIndex], y:values[j][voltageIndex]}
                powerData[j] = {x: values[j][timeIndex], y:values[j][powerIndex]}
                tempData[j] ={x: values[j][timeIndex], y:values[j][tempIndex]}
            }
        }
    } else {
        currentData = [];
        voltageData = [];
        powerData = [];
        tempData = [];
        for (var j = 0; j < values.length; j++) {
            currentData.push({x: values[j][timeIndex], y:values[j][currentIndex]})
            voltageData.push({x: values[j][timeIndex], y:values[j][voltageIndex]})
            powerData.push({x: values[j][timeIndex], y:values[j][powerIndex]})
            tempData.push({x: values[j][timeIndex], y:values[j][tempIndex]})
        }
    }
    console.log(mainChart.data[0]);
    mainChart.options.data[0].dataPoints = currentData;
    mainChart.options.data[1].dataPoints = voltageData;
    mainChart.options.data[2].dataPoints = powerData;
    mainChart.options.data[3].dataPoints = tempData;
    mainChart.render();
    
}

function fetchData() {
    $.post("../database", {query: 'SELECT', measurement: database, batchsize: '*'}).done(function(response){
        data = eval(response);
        console.log(data);
        updateData(data);
    });
}

function getDatabases() {
    $.post('../database', {query: 'SHOW', measurement: 'None', batchsize: 0}).done(function(response){
        response = eval(response);
        $('.databases')
            .find('option')
            .remove();
        for (var i = 0; i < response.length; i++) {
            $('.databases').append('<option value="'+response[i]+'">'+response[i]+'</option>')
        }
    });
}

function updateDatabase() {
    database = $('.databases')[0].value;
    console.log(database);
    fetchData();
}

function removeDatabase() {
    $.post('../database', {query: 'DROP', measurement: $('.databases')[0].value, batchsize: 0}).done(function(data){
        console.log(data);
    });
    getDatabases();
}

function Call(thing) {
    var Class = thing[0].className;
    if (thing.val() == '') {
        if (Class == 'filename') {
            check[0] = false;
        } else if (Class == 'serial') {
            check[1] = false;
        } else if (Class == 'purpose') {
            check[2] = false;
        }
    } else {
        if (Class == 'filename') {
            check[0] = true;
        } else if (Class == 'serial') {
            check[1] = true;
        } else if (Class == 'purpose') {
            check[2] = true;
        }
    }
    disableButton();
}

function disableButton(){
    if (true == check[0] && check[1] == true && check[2] == true) {
        $('.startConsole').prop('disabled', false);
    } else {
        $('.startConsole').prop('disabled', true);
    }
}

function startConsole(){
    var purpose = $('.purpose').val();
    var model = $('.model').val();
    var serial = $('.serial').val();
    var filename = $('.filename').val();
    $.post("../start", {Purpose: purpose, Model: model, Serial: serial, Filename: filename})
        .done(function(data) {
            console.log( "Data Loaded: " + data );
        });
}