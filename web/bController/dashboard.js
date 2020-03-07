const THRESHOLD = 6400;

setup();

var ws;

function setup(){
    ws = new WebSocket("ws://"+ document.location.hostname + ":5678");
    let pitch = document.getElementById("pitch");
    let roll = document.getElementById("roll");
    let cpu_temp = document.getElementById("cpu_temp");
    let out_temp = document.getElementById("out_temp");
    ws.onopen = function(e){
        console.log("Connected.");
    };
    ws.onmessage = function(e){
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

function openManualControl(){
    $("li.side-item-dashboard").removeClass("active");
    $("li.side-item-manual").addClass("active");
    $("div.row").replaceWith("<style>\n" +
        ".buttons, .axes {\n" +
        "  padding: 1em;\n" +
        "}\n" +
        "\n" +
        "/*meter*/.axis {\n" +
        "  min-width: 200px;\n" +
        "  margin: 1em;\n" +
        "}\n" +
        "\n" +
        ".button {\n" +
        "  padding: 1em;\n" +
        "  border-radius: 20px;\n" +
        "  border: 1px solid black;\n" +
        "  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAAXNSR0IArs4c6QAAAAxJREFUCNdjYPjPAAACAgEAqiqeJwAAAABJRU5ErkJggg==);\n" +
        "  background-size: 0% 0%;\n" +
        "  background-position: 50% 50%;\n" +
        "  background-repeat: no-repeat;\n" +
        "}\n" +
        "\n" +
        ".pressed {\n" +
        "  border: 1px solid red;\n" +
        "}\n" +
        "</style>\n" +
        "</head>\n" +
        "<body>\n" +
        "<h2 id=\"start\">Press a button on your controller to start</h2>\n" +
        "<div id=\"gamepad_container\"></div>");
}

function openDashboard(){
    location.reload(true)
}

var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;
var controllers = {};
var rAF = window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame ||
  window.requestAnimationFrame;

function connecthandler(e) {
  addgamepad(e.gamepad);
}
function addgamepad(gamepad) {
  controllers[gamepad.index] = gamepad;
  var main_container = document.getElementById("gamepad_container");
  var d = document.createElement("div");
  d.setAttribute("id", "controller" + gamepad.index);
  var t = document.createElement("h1");
  t.appendChild(document.createTextNode("gamepad: " + gamepad.id));
  d.appendChild(t);
  var b = document.createElement("div");
  b.className = "buttons";
  for (var i=0; i<gamepad.buttons.length; i++) {
    var e = document.createElement("span");
    e.className = "button";
    //e.id = "b" + i;
    e.innerHTML = i;
    b.appendChild(e);
  }
  d.appendChild(b);
  var a = document.createElement("div");
  a.className = "axes";
  for (i=0; i<gamepad.axes.length; i++) {
    e = document.createElement("meter");
    e.className = "axis";
    //e.id = "a" + i;
    e.setAttribute("min", "-1");
    e.setAttribute("max", "1");
    e.setAttribute("value", "0");
    e.innerHTML = i;
    a.appendChild(e);
  }
  d.appendChild(a);
  document.getElementById("start").style.display = "none";
  main_container.appendChild(d);
  rAF(updateStatus);
}

function disconnecthandler(e) {
  removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
  var d = document.getElementById("controller" + gamepad.index);
  document.body.removeChild(d);
  delete controllers[gamepad.index];
}

function updateStatus() {
  scangamepads();
  for (j in controllers) {
    var controller = controllers[j];
    var d = document.getElementById("controller" + j);
    var buttons = d.getElementsByClassName("button");
    for (var i=0; i<controller.buttons.length; i++) {
      var b = buttons[i];
      var val = controller.buttons[i];
      var pressed = val == 1.0;
      if (typeof(val) == "object") {
        pressed = val.pressed;
        val = val.value;
      }
      var pct = Math.round(val * 100) + "%";
      b.style.backgroundSize = pct + " " + pct;
      if (pressed) {
        b.className = "button pressed";
      } else {
        b.className = "button";
      }
    }

    var axes = d.getElementsByClassName("axis");
    for (var i=0; i<controller.axes.length; i++) {
      var a = axes[i];
      a.innerHTML = i + ": " + controller.axes[i].toFixed(4);
      a.setAttribute("value", controller.axes[i]);
      let value = controller.axes[i];
      if(value < -0.1 && i === 1){
          console.log(value);
          motorControl(0, 0.016, Math.abs(value * 100), "positive")
      }
      if(value > 0.1 && i === 1){
          console.log(value);
          motorControl(0, 0.016, Math.abs(value * 100), "negative")
      }
      if(value < -0.1 && i === 3){
          console.log(value);
          motorControl(1, 0.016, Math.abs(value * 100), "positive")
      }
      if(value > 0.1 && i === 3){
          console.log(value);
          motorControl(1, 0.016, Math.abs(value * 100), "negative")
      }
      if(Math.abs(value) === 0 && i === 1){
          motorStop()
      }
    }
  }
  rAF(updateStatus);
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {
    if (gamepads[i]) {
      if (!(gamepads[i].index in controllers)) {
        addgamepad(gamepads[i]);
      } else {
        controllers[gamepads[i].index] = gamepads[i];
      }
    }
  }
}

function motorControl(m_index, duration, speed, direction){
    let message = {"title": "motor", "m_index": m_index, "m_duration": duration, "m_direction": direction, "m_speed": speed}
    ws.send(JSON.stringify(message))
}

function motorStop(){
    ws.send(JSON.stringify({"title": "halt"}))
}

if (haveEvents) {
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
  window.addEventListener("webkitgamepadconnected", connecthandler);
  window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
  setInterval(scangamepads, 500);
}

