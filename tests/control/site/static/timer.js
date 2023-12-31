// document.addEventListener('DOMContentLoaded', function() {
//     // Set the initial countdown time to 1 hour (3600 seconds)
//     var countdownTime = 3600; // 1 hour in seconds
//     var fifteenLeft = 900; // 15 minutes in seconds
//     var fiveLeft = 300; // 5 minutes in seconds

//     var timerDiv = document.getElementById('timer');
//     var startButton = document.getElementById('startTimer');

//     startButton.addEventListener('click', function () {
//         document.getElementById('timer').textContent = "BEGIN!";
//         timerDiv.classList.remove('ready');
//         timerDiv.classList.add('mtquart');

//         // Update the countdown every second
//         var timerInterval = setInterval(function () {
//             countdownTime--;
//             var hours = Math.floor(countdownTime / 3600);
//             var minutes = Math.floor((countdownTime % 3600) / 60);
//             var seconds = countdownTime % 60;

//             // Format the time as HH:MM:SS
//             var formattedTime =
//                 (hours < 10 ? "0" : "") + hours + ":" +
//                 (minutes < 10 ? "0" : "") + minutes + ":" +
//                 (seconds < 10 ? "0" : "") + seconds;

//             // Update the timer div
//             document.getElementById('timer').textContent = formattedTime;

//             // When the countdown reaches 0, stop the timer
//             if (countdownTime <= 0) {
//                 clearInterval(timerInterval);
//                 document.getElementById('timer').textContent = "00:00:00";
//             }

//             if (countdownTime == fifteenLeft) {
//                 timerDiv.classList.remove('mtquart');
//                 timerDiv.classList.add('ltquart');
//             }

//             if (countdownTime == fiveLeft) {
//                 timerDiv.classList.remove('ltquart');
//                 timerDiv.classList.add('ltfive');
//             }

//         }, 1000);

//         // Disable the start button
//         this.disabled = true;
//     });
// });


document.addEventListener('DOMContentLoaded', function () {
    // TODO Timer and Start Button. Too Much logic to figure out tonight.
    // Make sure the timer says "READY" when it's ready.
    // "ERROR" when it's not.
    // "BEGIN!" when it's first started
    // "Time while it's running"
    // "TIMES UP!" when it's done.
});