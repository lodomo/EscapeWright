const updateLoadingBar = async () => {
    try {
        const response = await fetch('/load_status');
        if (response.ok) {
            const data = await response.json();
            const loadingBar = document.getElementById('loading-bar');
            const loadingNumber = document.getElementById('loading-number');

            if (data.status === "READY") {
                loadingBar.style.backgroundColor = "#80D18A"; // green
                loadingBar.style.width = "100%";
                loadingNumber.innerText = "READY";
            } else if (data.status === "ERROR") {
                loadingBar.style.backgroundColor = "#DD3C3C"; // red
                loadingBar.style.width = "100%";
                loadingNumber.innerText = "ERROR";
            } else {
                loadingBar.style.backgroundColor = "#FFF275"; // yellow
                loadingBar.style.width = data.status + "%";
                loadingNumber.innerText = data.status;
            }
        } else {
            console.error('Failed to fetch load status');
        }
    } catch (error) {
        console.error(`Fetch error: ${error}`);
    }
};

setInterval(updateLoadingBar, 1000);
