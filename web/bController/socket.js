const THRESHOLD = 6400;

function setup(){
    let ws = new WebSocket("ws://"+ document.location.hostname + ":5678");
    let pitch = document.getElementById("pitch");
    let roll = document.getElementById("roll");
    let cpu_temp = document.getElementById("cpu_temp");
    let out_temp = document.getElementById("out_temp");
    ws.onopen = function(e){
        console.log("Connected.");
    };
    ws.onmessage = function(e){
        console.log(e);
        pitch.innerHTML = JSON.parse(e.data)["pitch"];
        roll.innerHTML = JSON.parse(e.data)["roll"];
        cpu_temp.innerHTML = JSON.parse(e.data)["cpu_temp"];
        out_temp.innerHTML = JSON.parse(e.data)["out_temp"];
    };

    document.getElementById("defaults_button").onclick = setDefaults;

}

function sendInclinationData(){
    let pitchAngle = document.getElementById("pitch_input").value;
    let rollAngle = document.getElementById("roll_input").value;
    if(pitchAngle === "" || rollAngle === ""){
        alert("Pitch or Roll angle should not be empty.")
    }
    else{
        let inclinationJSON = {
            "pitch_angle":pitchAngle,
            "roll_angle":rollAngle
        };
        console.log(inclinationJSON)
    }
}

function setDefaults(){
    document.getElementById("pitch_input").value = 0;
    document.getElementById("roll_input").value = 0;
    sendInclinationData();
}

setup();