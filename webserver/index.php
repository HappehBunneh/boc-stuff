<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel='stylesheet' href='main.css'>
        <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/dygraph/2.1.0/dygraph.min.js"></script>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/dygraph/2.1.0/dygraph.min.css" />
        <script src="main.js"></script> 
        <title>MaxTerm</title>
    </head>
    <body>
        <div class='output'>Some output over here</div>
        <div class='graphContainer'>
            <div class='graph' id='mainGraph'></div>
        </div>
        <div id='div_g'></div>
        <div class='buttonContainer' style='background-color: blue'>
            <button id='start' onclick='button_click(this.id)'>Start</button>
            <button id='stop' onclick='button_click(this.id)'>Stop</button>
            <button id='clear' onclick='button_click(this.id)'>Clear</button>
        </div>
    </body>
</html>