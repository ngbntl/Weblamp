// Create WebSocket connection.
const socket = new WebSocket("ws://192.168.1.11:6789");
var ledState;

// Connection opened
socket.addEventListener("open", function (event) {
  console.log("Connected to the WebSocket server");
});

// Listen for messages
socket.addEventListener("message", function (event) {
  console.log("Message from server: ", event.data);
  message = JSON.parse(event.data);

  var checkRed = document.getElementById("checkRed");
  var checkGreen = document.getElementById("checkGreen");
  var checkBlue = document.getElementById("checkBlue");

  var button = message.button;
  if (button) {
    console.log(button);
    if (button == 3) {
      var videoElement = document.getElementById("videoElement");
      videoElement.src = "./video/ThayBa.mp4";
      document.getElementById("btnn").innerText = "Button 3";
      // videoElement.removeAttribute("muted");
      // videoElement.play();
    } else if (button == 2) {
      var videoElement = document.getElementById("videoElement");
      videoElement.src = "./video/SuperIdol.mp4";
      document.getElementById("btnn").innerText = "Button 2";
    } else if (button == 1) {
      var videoElement = document.getElementById("videoElement");
      videoElement.src = "./video/Rickroll.mp4";
      document.getElementById("btnn").innerText = "Button 1";
    }
  } else {
    ledState = message;
    checkRed.checked = !message.red;
    checkGreen.checked = !message.green;
    checkBlue.checked = !message.blue;

    if (checkRed.value) {
      checkRed.value = false;
    } else {
      checkRed.valuee = true;
    }
    if (checkGreen.value) {
      checkGreen.value = false;
    } else {
      checkGreen.value = true;
    }
    if (checkBlue.value) {
      checkBlue.value = false;
    } else {
      checkBlue.value = true;
    }
  }
});

// Send a message to the server
function toggleLed(color) {
  var message = JSON.stringify({
    color: color,
    state: 1 - ledState[color],
  });
  socket.send(message);
}
