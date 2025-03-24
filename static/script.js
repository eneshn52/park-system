async function fetchParkingStatus() {
    try {
        const response = await fetch('/get_parking_status');
        if (!response.ok) {
            console.error("Hata: ", response.status);
            return;
        }
        
        const status = await response.json();
        const statusContainer = document.getElementById('status-container');
        statusContainer.innerHTML = '';

        status.forEach((space, index) => {
            const spaceDiv = document.createElement('div');
            spaceDiv.classList.add('parking-space', space);
            spaceDiv.innerText = `Alan ${index + 1}`;
            statusContainer.appendChild(spaceDiv);
        });
    } catch (error) {
        console.error("Park durumu alınırken hata oluştu:", error);
    }
}

setInterval(fetchParkingStatus, 2000);
fetchParkingStatus();
