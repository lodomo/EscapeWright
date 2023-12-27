document.getElementById('resetButton').addEventListener('click', function() {
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