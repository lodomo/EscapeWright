// Create a function that will update the modal
function updateModal(eventType, eventText) {
    // Find the modal
    var modal = document.getElementById('event-modal');
    // Make the modal visible by displaying block
    modal.style.display = 'block';
    // Find the circle element
    var circle = document.getElementById('event-circle');
    // Add animation "expand" to the circle
    circle.classList.add('expand-circle');
    // Add class to the circle to make it the right color.
    circle.classList.add(eventType);
    // Find the text element
    var text = document.getElementById('event-text');
    // Add class to the text to make it the right color.
    text.classList.add(eventType);
    // Change the text
    text.innerHTML = eventText;
    // add fade-in animation to the text
    text.classList.add('fade-in');
    // Find the close button
    var close = document.getElementById('close-event-modal');
    close.classList.add('fade-in')
    // Add event listener to the close button
    close.addEventListener('click', function () {
        // Link to the url_for index
        window.location.href = '/';
    });
};


document.getElementById('resetButton').addEventListener('click', function () {
    updateModal('reset', 'ROOM RESET<br>IN PROGRESS');

    fetch('/reset', { method: 'POST' })
    .then(response => {
        if (response.ok) {
            console.log('Reset request was sent successfully');
        } else {
            console.error('Reset request failed');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('stopButton').addEventListener('click', function() {
    updateModal('stop', 'ROOM STOPPED');

    fetch('/stop', { method: 'POST' })
    .then(response => {
        if (response.ok) {
            console.log('Stop request was sent successfully');
        } else {
            console.error('Stop request failed');
        }
    })
    .catch(error => console.error('Error:', error));
});