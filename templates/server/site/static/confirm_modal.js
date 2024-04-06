// This function will run once the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    // Get the modal and the close button elements.
    var modal = document.getElementById('warningModal');
    var span = document.getElementsByClassName("close")[0];

    // Function to hide the modal.
    function hideModal() {
        modal.classList.add('modal-animate-out');

        modal.addEventListener('animationend', function() {
            if (event.animationName === 'slideDownAndFadeOut') {
                modal.style.display = 'none';
                modal.classList.remove('modal-animate-out'); // Remove the class if the modal will be used again
            }
        });
    }

    // Function to show the modal with specific action text.
    function showModal(action) {
        var modalHeader = document.querySelector('.modal-header h2');
        modalHeader.innerHTML = 'ARE YOU SURE <br> YOU WANT TO ' + action.toUpperCase() + '?';
        modal.style.display = "flex";
        modal.classList.add('modal-animate-in'); // Start the animation
    }

    // Attach the event listener to each button with the 'mybtn' class.
    var btns = document.querySelectorAll('.mybtn');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var action = this.getAttribute('data-action');
            showModal(action);
            // Store the action in the confirm button for later.
            var confirmYes = document.getElementById('confirmYes');
            confirmYes.setAttribute('data-action', action);
        });
    });

    // When the user clicks on <span> (x), close the modal.
    span.addEventListener('click', hideModal);

    // When the user clicks on "NO", close the modal.
    document.getElementById('confirmNo').addEventListener('click', hideModal);

    // When the user clicks on "YES", perform the action.
    document.getElementById('confirmYes').addEventListener('click', function() {
        var action = this.getAttribute('data-action');
        console.log('Confirmed action:', action);
        // TODO: Add your action handling logic here based on the 'action' variable.
        hideModal();
    });

    // When the user clicks anywhere outside of the modal, close it.
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            hideModal();
        }
    });
});
