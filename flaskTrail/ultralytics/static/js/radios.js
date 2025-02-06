const radioButtons = document.querySelectorAll('input[name="camera"]');

radioButtons.forEach(radio => {
    radio.addEventListener('change', (event) => {
        const selectedCamera = event.target.id;
        console.log(`Selected camera: ${selectedCamera}`);
        fetch('/update_cam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ camera: selectedCamera })
        }).then(response => {
            if (response.ok) {
                console.log('Camera updated successfully to', selectedCamera);
            } else
                console.error('Failed to update camera');
        })
    });
});
