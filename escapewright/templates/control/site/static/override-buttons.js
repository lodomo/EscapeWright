window.onload = function() {
    var buttons = document.getElementsByClassName('override-btn');
    var maxHeight = 0;

    // Find the maximum height
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].offsetHeight > maxHeight) {
            maxHeight = buttons[i].offsetHeight;
        }
    }

    // Set all buttons to the maximum height
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.height = maxHeight + 'px';
    }
};

document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('.override-btn');
    var override_modal = document.getElementById('override-modal');
    var override_bubble = document.getElementById('override-bubble');
    var override_text = document.getElementById('override-text');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var link = this.getAttribute('data-link');
            var text = this.getAttribute('id');

            fetch('http://' + link, { mode: 'no-cors' })
                .then(() => {
                    console.log('Request sent to:', link);
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            // Reset modal and bubble classes to initial state
            override_modal.style.display = 'block';
            override_modal.classList.remove('over-fade-out');
            override_modal.classList.add('over-fade-in');

            override_bubble.classList.remove('bubble-out');
            override_bubble.classList.add('bubble-in');

            override_text.innerHTML = "Sent Request to:<br>" + text; 
        });
    });

    // Close the modal when the user clicks anywhere
    window.onclick = function(event) {
        if (event.target == override_modal) {
            override_bubble.classList.remove('bubble-in');
            override_bubble.classList.add('bubble-out');
            override_modal.classList.remove('over-fade-in');
            override_modal.classList.add('over-fade-out');
            setTimeout(function() {
                override_modal.style.display = 'none';
            }, 500); // 500ms should match the length of your fade-out animation
        }
    }
});
