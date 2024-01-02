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

// // Set the toggle button
// document.addEventListener('DOMContentLoaded', function () {
//     // Find the toggle button
//     var toggleButton = document.getElementById('toggleButton');
//     var modal = document.getElementById("info-modal");
//     var closeButton = document.getElementById("info-modal-cancel-btn");
//     var submitButton = document.getElementById("info-modal-submit-btn");

//     // Set the submit button to send a POST request to /start
//     submitButton.onclick = function () {
//         var client = new XMLHttpRequest();
//         var gameGuide = document.getElementById('nameSelect').value;
//         var players = document.getElementById('players').value;
//         var flask_route = '/start/' + gameGuide + '/' + players;
//         client.open("POST", flask_route, true);
//         client.send();
//     }

//     closeButton.onclick = function () {
//         modal.classList.add("slide-out-to-bottom");
//         // When the animation is finished, hide the modal
//         modal.addEventListener("animationend", function () {
//             modal.classList.remove("slide-out-to-bottom");
//             modal.style.display = "none";
//         });
//     }

//     // Add a click event
//     toggleButton.addEventListener('click', function () {
//         var toggleText = toggleButton.textContent;

//         if (toggleText == "START") {
//             // Bring up modal
//             //find the enter name modal


//             // When the user clicks on the button, open the modal
//             modal.style.display = "block";


//         }
//         else {
//             // Send a POST request to /toggle
//             var flask_route = '/toggle';
//             var client = new XMLHttpRequest();
//             client.open("POST", flask_route, true);
//             client.send();
//         }

//     });
// });

document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.getElementById('toggleButton');
    var modal = document.getElementById("info-modal");
    var closeButton = document.getElementById("info-modal-cancel-btn");
    var submitButton = document.getElementById("info-modal-submit-btn");

    // Define the function to hide the modal after animation
    function hideModalAfterAnimation() {
        modal.classList.remove("slide-out-to-bottom");
        modal.style.display = "none";
        modal.removeEventListener("animationend", hideModalAfterAnimation);
    }

    submitButton.onclick = function () {
        var client = new XMLHttpRequest();
        var gameGuide = document.getElementById('nameSelect').value;
        var players = document.getElementById('players').value;
        var flask_route = '/start/' + gameGuide + '/' + players;
        client.open("POST", flask_route, true);
        client.send();
        modal.classList.add("slide-out-to-bottom");
        modal.addEventListener("animationend", hideModalAfterAnimation);
    }

    closeButton.onclick = function () {
        modal.classList.add("slide-out-to-bottom");
        modal.addEventListener("animationend", hideModalAfterAnimation);
    }

    toggleButton.addEventListener('click', function () {
        var toggleText = toggleButton.textContent;

        if (toggleText == "START") {
            modal.style.display = "block";
        } else {
            var flask_route = '/toggle';
            var client = new XMLHttpRequest();
            client.open("POST", flask_route, true);
            client.send();
        }
    });
});