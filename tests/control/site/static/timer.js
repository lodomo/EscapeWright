// Constantly updates the timer, which is a div with id="timer"
document.addEventListener('DOMContentLoaded', function () {
    function timer_updater() {
        console.log("Timer Updater Started");
        var flask_route = '/time_remaining';
        var client = new EventSource(flask_route);
        var timerDiv = document.getElementById('timer');

        client.onmessage = function (event) {
            // Set timerDiv to the time remaining
            timerDiv.textContent = event.data;
        }
        
        client.onerror = function (error) {
            console.error("EventSource failed:", error);
            client.close();
        };
    }
    timer_updater();
});

// Set the proper text for the button
document.addEventListener('DOMContentLoaded', function () {
    function get_initial_status() {
        var flask_route = '/room_status';
        var client = new EventSource(flask_route);
        var toggleButton = document.getElementById('toggleButton');

        client.onmessage = function (event) {
            console.log(event.data);
            // Remove all classes except "control-btn"
            var classes = toggleButton.classList;
            for (var i = 0; i < classes.length; i++) {
                if (classes[i] != "toggle-btn") {
                    toggleButton.classList.remove(classes[i]);
                }
            }

            switch (event.data) {
                case "LOADING":
                    // Set the button to say "Loading" 
                    toggleButton.textContent = "WAIT";
                    toggleButton.classList.add("loading");
                    toggleButton.disabled = true;
                    break;
                case "READY":
                    // Set the button to say "Start"
                    toggleButton.textContent = "START";
                    toggleButton.classList.add("ready");
                    toggleButton.disabled = false;
                    break;
                case "RUNNING":
                    // Set the button to say "Pause"
                    toggleButton.textContent = "PAUSE";
                    toggleButton.classList.add("pause");
                    toggleButton.disabled = false;
                    break;
                case "STOPPED":
                    // Set the button to say "Disabled"
                    toggleButton.textContent = "✖";
                    toggleButton.classList.add("stopped");
                    toggleButton.disabled = true;
                    break;
                case "PAUSED":
                    // Set the button to say "Resume"
                    toggleButton.textContent = "RESUME";
                    toggleButton.classList.add("resume");
                    toggleButton.disabled = false;
                    break;
                default:
                    console.log("Unknown status: " + event.data);
                    toggleButton.textContent = "ERROR";
                    toggleButton.classList.add("error");
                    break;
            }
        }
        
        client.onerror = function (error) {
            console.error("EventSource failed:", error);
            client.close();
        };
    }

    get_initial_status();
});

// Set the toggle button 
document.addEventListener('DOMContentLoaded', function () {
    // Find the toggle button
    var toggleButton = document.getElementById('toggleButton');

    // Add a click event
    toggleButton.addEventListener('click', function () {
        var toggleText = toggleButton.textContent;

        if (toggleText == "START") {
            // Bring up modal
            //find the enter name modal
            var modal = document.getElementById("info-modal");
            var closeButton = document.getElementById("info-modal-close-btn");
            var submitButton = document.getElementById("info-modal-submit-btn");

        }
        else {
            // Send a POST request to /toggle
            var flask_route = '/toggle';
            var client = new XMLHttpRequest();
            client.open("POST", flask_route, true);
            client.send();
        }

    });
});