document.getElementById('threshold').addEventListener('input', function () {
    const thresholdValue = this.value;
    fetch('/update_threshold', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ threshold: thresholdValue })
    }).then(response => {
        if (response.ok) {
            console.log('Threshold updated successfully to', thresholdValue);
        } else {
            console.error('Failed to update threshold');
        }
    });
});

document.getElementById('brightness').addEventListener('input', function () {
    const brightnessValue = this.value;
    fetch('/update_brightness', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ brightness: brightnessValue })
    }).then(response => {
        if (response.ok) {
            console.log('Brightness updated successfully to', brightnessValue);
        } else {
            console.error('Failed to update threshold');
        }
    });
});

