// This function will run once the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    // Get the modal and the close button elements.
    var modal = document.getElementById('options');
    var span = document.getElementsByClassName("close")[0];

    // Function to hide the modal.
    function hideModal() {
        modal.classList.add('options-modal-animate-out');

        modal.addEventListener('animationend', function() {
            if (event.animationName === 'modalSlideLeftOut') {
                modal.style.display = 'none';
                modal.classList.remove('options-modal-animate-out'); // Remove the class if the modal will be used again
            }
        });
    }

    // Function to show the modal with specific action text.
    function showModal() {
        modal.style.display = "flex";
        modal.classList.add('options-modal-animate-in'); // Start the animation
    }

    // Attach the event listener to each button with the 'mybtn' class.
    var btns = document.querySelectorAll('.options');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            showModal();
        });
    });

    // When the user clicks on <span> (x), close the modal.
    span.addEventListener('click', hideModal);

    // When the user clicks on "NO", close the modal.
    document.getElementById('closeOptions').addEventListener('click', hideModal);

    // When the user clicks anywhere outside of the modal, close it.
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            hideModal();
        }
    });
});
