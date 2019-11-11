const THRESHOLD = 6400;

function setup(){
    let ws = new WebSocket("ws://"+ document.location.hostname + ":5678");
    let output = document.getElementById("value")
    ws.onopen = function(e){
        console.log("Connected.");
    };
    ws.onmessage = function(e){
        console.log(e)
        output.innerHTML = e.data;
    };
}


setup();