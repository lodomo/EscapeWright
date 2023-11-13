function confirmAction(btn, url) {
    var buttonText = btn.getAttribute('alt');
    var confirmMessage = 'Are you sure you want to ' + buttonText.toUpperCase() + '?';
    var userConfirmed = confirm(confirmMessage);
    
    if (userConfirmed) {
        window.location.href = url;
    }
}