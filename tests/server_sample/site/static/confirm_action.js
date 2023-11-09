function confirmAction(btn, url) {
    var buttonText = btn.textContent || btn.innerText;
    var confirmMessage = 'Are you sure you want to ' + buttonText.toUpperCase() + '?';
    var userConfirmed = confirm(confirmMessage);
    
    if (userConfirmed) {
        window.location.href = url;
    }
}