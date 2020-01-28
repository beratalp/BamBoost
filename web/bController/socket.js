const THRESHOLD = 6400;

function setup(){
    let ws = new WebSocket("ws://"+ document.location.hostname + ":5678");
    let pitch = document.getElementById("pitch");
    let roll = document.getElementById("roll")
    ws.onopen = function(e){
        console.log("Connected.");
    };
    ws.onmessage = function(e){
        console.log(e);
        pitch.innerHTML = JSON.parse(e.data)["pitch"];
        roll.innerHTML = JSON.parse(e.data)["roll"]
    };
}

setup();