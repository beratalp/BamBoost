const THRESHOLD = 6400;

function setup(){
    let ws = new WebSocket("ws://localhost:5678");
    output = document.createElement("ul");
    ws.onopen = function(e){
        console.log("Connected.");
    };
    ws.onmessage = function(e){
        var messages = document.getElementsByTagName("ul")[0],
            message = document.createElement("li"),
            content = document.createTextNode(e.data);
        message.appendChild(content);
        messages.appendChild(message);
    };
    document.body.appendChild(messages);
}


setup();