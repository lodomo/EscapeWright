// Select all buttons and divs
// .nav-btn AND .message-btn
const buttons = document.querySelectorAll('.nav-btn');
const moreButtons = document.querySelectorAll('.message-btn');
const divs = document.querySelectorAll('.content');

// Function to handle button click
function handleButtonClick(e) {
    // Prevent default action if it's a submit button
    e.preventDefault();

    // Find the associated div for the clicked button
    const associatedDivId = e.target.getAttribute('data-target');
    const associatedDiv = document.querySelector(`#${associatedDivId}`);

    // Check if the associated div exists
    if (associatedDiv) {
        // Set the associated div to active and adjust size
        associatedDiv.classList.remove('inactive');
        associatedDiv.classList.add('active');

        // Loop over all divs to reset others
        divs.forEach(div => {
            if (div.id !== associatedDivId) {
                div.classList.remove('active');
                div.classList.add('inactive');
            }
        });
    } else {
        console.error(`No div found with ID: ${associatedDivId}`);
    }
}

// Add click event listeners to each button
buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
});

moreButtons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
});