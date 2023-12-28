document.addEventListener('DOMContentLoaded', function () {
    function status_updater() {
        console.log("Status Updater Started");
        var flask_route = '/display_status';
        var client = new EventSource(flask_route);

        client.onmessage = function (event) {
            if (event.data == "NTR") {
                // Do nothing
                return;
            }

            console.log("Received:", event.data);        // Print all the data to update
            let client_data = JSON.parse(event.data);    // Parse the data
            let client_name = client_data['name'];       // Get the client name
            let client_status = client_data['status'];   // Get the client status
            let status_id = client_name + "-status";     // Get the status id
            client_status = client_status.toUpperCase(); // Convert to uppercase
            // Print all the data to update
            console.log("Client Name:", client_name);     // Print all the data to update
            console.log("Client Status:", client_status); // Print all the data to update
            console.log("Status ID:", status_id);         // Print all the data to update   
            // Update the status text
            document.getElementById(status_id).innerHTML = client_status;

            var balloon = document.getElementById(client_name + "-balloon");

            // Remove any class that is not 'status-balloon'
            Array.from(balloon.classList).forEach((className) => {
                if (className !== "status-balloon") {
                    balloon.classList.remove(className);
                }
            });

            // Add the new status class
            balloon.classList.add(client_status.toLowerCase());

        };

        client.onerror = function (error) {
            console.error("EventSource failed:", error);
            client.close();
        };
    }

    status_updater();
});