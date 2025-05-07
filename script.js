const connection = document.getElementById('connection');
const nameOfTopic = document.getElementById('topic');
const client = mqtt.connect('wss://broker.emqx.io:8084/mqtt');
const broker = "broker.emqx.io"
const topic = 'eps32_3dprinter_13579';

//Connect to mqtt
client.on('connect', function () {
    connection.innerText = `Connected to ${broker}`;
    client.subscribe(topic, function (err) {
        if (!err) {
            nameOfTopic.innerText = topic;
        } else {
            nameOfTopic.innerText = 'Error in subscribed topic\n';
        }
    });
});

//Sending data
client.on('message', function (incomingTopic, message) {
    try {
        const data = JSON.parse(message.toString());
        document.getElementById("status").textContent = data.status.toUpperCase();
        document.getElementById("nozzle").textContent = `${data.nozzle} °C`;
        document.getElementById("base").textContent = `${data.base} °C`;
        document.getElementById("progress").textContent = data.progress;
        document.getElementById('time').textContent = `Last update: ${data.update}`;   
    } catch (e) {
        console.error("JSON parsing error:", e);
    }
});

// Converts time in seconds to a formatted "HH:MM" string
function formatSecondsToTime(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const hh = hrs.toString().padStart(2, "0");
    const mm = mins.toString().padStart(2, "0");
    return `${hh}:${mm}`;
}
