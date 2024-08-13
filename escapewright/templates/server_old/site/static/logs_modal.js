// This function will run once the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    // Get the modal and the close button elements.
    var modal = document.getElementById('logs');
    var span = document.getElementsByClassName("close")[0];

    // Function to hide the modal.
    function hideModal() {
        modal.classList.add('logs-modal-animate-out');

        modal.addEventListener('animationend', function() {
            if (event.animationName === 'modalSlideRightOut') {
                modal.style.display = 'none';
                modal.classList.remove('logs-modal-animate-out'); // Remove the class if the modal will be used again
            }
        });
    }

    // Function to show the modal with specific action text.
    function showModal() {
        modal.style.display = "flex";
        modal.classList.add('logs-modal-animate-in'); // Start the animation
    }

    // Attach the event listener to each button with the 'mybtn' class.
    var btns = document.querySelectorAll('.logs');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            showModal();
        });
    });

    // When the user clicks on "NO", close the modal.
    document.getElementById('closeLogs').addEventListener('click', hideModal);
});
